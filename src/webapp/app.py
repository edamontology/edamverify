import csv
from flask import Flask, redirect, url_for, request, render_template
import random

from rdflib import ConjunctiveGraph, Namespace

app = Flask(__name__)

ns = {"dc": "http://dcterms/",
      "edam": "http://edamontology.org/",
      "owl": "http://www.w3.org/2002/07/owl#"
      }

g = ConjunctiveGraph()
g.load('https://raw.githubusercontent.com/edamontology/edamontology/master/EDAM_dev.owl', format='xml')
g.bind('edam', Namespace('http://edamontology.org/'))
print(str(len(g)) + ' triples in the EDAM triple store')

## Build an index to retrieve term labels 
idx_label = {}
idx_uri = {}
idx_query = """
SELECT ?x ?label WHERE {
    ?x rdf:type owl:Class ; 
       rdfs:label ?label .
}
"""
results = g.query(idx_query)
for r in results :
    #print(f"{r['label']} is identified in EDAM with concept {r['x']}") 
    idx_uri[str(r['x'])] = str(r['label'])
    idx_label[str(r['label'])] = str(r['x'])
 
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/expert_curation')
def expert_curation():
    return render_template('index.html')

@app.route('/edam_stats')
def edam_stats():

    idx_query = """
    SELECT ?x ?label WHERE {
    ?x rdf:type owl:Class ; 
       rdfs:label ?label .
    }
    """
    results = g.query(idx_query)
    for r in results :
        #print(f"{r['label']} is identified in EDAM with concept {r['x']}") 
        idx_uri[str(r['x'])] = str(r['label'])
        idx_label[str(r['label'])] = str(r['x'])

    return render_template('stats.html')
    
@app.route('/edam_validation')
def edam_validation():
    return render_template('index.html')


class EdamTest:
    Number=0
    Level=''
    TestName=''
    Entity=''
    Label=''
    DebugMessage=''

@app.route('/edam_last_report')
def edam_last_report():
    
    # robot report
    
    # edam ci report
    with open("test_data/output_edamci.tsv") as file:
        output_edamci = csv.DictReader(file, delimiter="\t")
        edam_output_list = []
        for row in output_edamci:
            edam_output_list.append(row)
    return render_template('edam_last_report.html', output_edamci=edam_output_list)

@app.route('/quick_curation')
def quick_curation():

    # NO wikipedia
    q_no_wikipedia = """
    SELECT (count(?term) as ?nb_no_wikipedia) WHERE {
        ?c rdfs:subClassOf+ edam:topic_0003 ; 
                    rdfs:label ?term .
        
        FILTER NOT EXISTS {
            ?c rdfs:seeAlso ?seealso .
            FILTER (regex(str(?seealso), "wikipedia.org", "i"))  
        } .
    }
    """
    results = g.query(q_no_wikipedia, initNs=ns)
    count_no_wikipedia = 0
    for r in results:
        count_no_wikipedia = str(r["nb_no_wikipedia"])

    #########
    q_no_publication_entries = """
        SELECT ?c ?term WHERE {
            ?c rdfs:subClassOf+ edam:topic_0003 ; 
                rdfs:label ?term .

            FILTER NOT EXISTS {
                ?c rdfs:seeAlso ?seealso .
                FILTER (regex(str(?seealso), "wikipedia.org", "i"))  
            } .
        }
        """
    results = g.query(q_no_publication_entries, initNs=ns)
    no_wikipedia = []
    for r in results:
        no_wikipedia.append({"term": r["term"], "class": r["c"]})

    if len(no_wikipedia) > 5:
        no_wikipedia = random.sample(no_wikipedia, 5)

    return render_template('quick_curation.html',
                           count_no_wikipedia = count_no_wikipedia,
                           missing_wikipedia = no_wikipedia)


@app.route('/cy')
def cy():
    return render_template('test_cy.html')


if __name__ == "__main__":
    # context = ('myserver-dev.crt', 'myserver-dev.key')
    # app.run(host='0.0.0.0', port=5000, debug=True, ssl_context=context)
    # context = ('myserver-dev.crt', 'myserver-dev.key')
    app.run(host='0.0.0.0', port=5000, debug=True)