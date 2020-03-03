# Misuse of subset annotation property

**Problem:** The specified EDAM subset for a concept is wrong because the value: 1) mismatches the subontology (non-deprecated concepts) or 2) is misstated (deprecated concepts) or 3) is otherwise not supported.

**Solution:** Change the subset to the correct value.

**Further information:**

Concept subset is defined by ```oboInOwl:inSubset``` annotation property and must have an applicable value from ```oboInOwl:SubsetProperty```. See [EDAM technical details](https://edamontologydocs.readthedocs.io/en/latest/developers_guide.html#mandatory-attributes) and [deprecation rules](https://edamontologydocs.readthedocs.io/en/latest/developers_guide.html#deprecating-concepts).


**Query:** [subsetMisuse.sparql](https://github.com/edamontology/edamverify/blob/master/queries/subsetMisuse.sparql)

```sparql
PREFIX obo: <http://purl.obolibrary.org/obo/>
PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ... <todo>
```