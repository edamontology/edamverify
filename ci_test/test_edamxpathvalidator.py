import unittest
import logging, sys
import subprocess

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s', stream=sys.stdout)

class TestLogging(unittest.TestCase):

    def setUp(self) -> None:
        logging.info("Logger initialized ! ")

    def test_edamxpathvalidator(self):
        process = subprocess.Popen(['edamxpathvalidator', '../../edamontology/EDAM_dev.owl'])
        output, error = process.communicate()
        if process.returncode != 0:
            self.fail(f'edamxpathvalidator failed with rc {process.returncode}')
    def tearDown(self) -> None:
        logging.info("End of unit test")


if __name__ == '__main__':
    unittest.main()