import unittest
import os
import sys
import json
from pprint import PrettyPrinter
from unittest.mock import patch, MagicMock
from benchmarks.ml_bench.ml_bench_benchmark import MLBenchBenchmark


# Add the parent directory to the path to import code_comparer
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from .code_comparer import CodeComparer


class TestCodeComparer(unittest.TestCase):
        
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Mock the environment variable for testing
        self.comparer = CodeComparer()
        self.model = MLBenchBenchmark()
        self.pp = PrettyPrinter(indent=4)
    
    def test_initialization_code_comparer_initialization(self):
        """Test that CodeComparer initializes correctly."""
        self.assertIsNotNone(self.comparer.client)

    def test_compare_equivalent_python_code1(self):
        """Test comparison of equivalent Python code."""
        code1 = 'result = 5 + 3'
        code2 = 'result = 3 + 5'
        
        result = self.comparer.compare(code1, code2, 'Python code')
#        self.pp.pprint("Test code 1 ------------------------------------------------------------------->")
#        self.pp.pprint(f"code1: {code1}")
#        self.pp.pprint(f"code2: {code2}")
#        self.pp.pprint(f"result: {result}")
        
        self.assertIn("sameResult", result)
        self.assertIn("reason", result)
        self.assertIsInstance(result["reason"], str)
        self.assertTrue(result["sameResult"])


    def test_compare_equivalent_python_code2(self):
        """Test comparison of equivalent Python code."""
        code1 = self.model.get_task("0043").data["output"]
        code2 = '\nimport torch\nimport esm\nimport biotite.structure.io as bsio\n\n# Load the ESMFold model\nmodel = esm.pretrained.esm_msa1b_t12_100M_UR50S()\nmodel = model.eval().cuda()\n\n# Set the input sequence\nsequence = \"MKTVRQERLKSIVRILERSKEPV\"\n\n# Perform structure prediction\nwith torch.no_grad():\n    output = model.infer_pdb(sequence)\n\n# Save the output structure to a PDB file\nwith open(\"output.pdb\", \"w\") as f:\n    f.write(output)\n'
        
        result = self.comparer.compare(code1, code2, 'Python code')
 #       self.pp.pprint("Test code 2 ------------------------------------------------------------------->")
 #       self.pp.pprint(f"code1: {code1}")
 #       self.pp.pprint(f"code2: {code2}")
 #       self.pp.pprint(f"result: {result}")
        
        self.assertIn("sameResult", result)
        self.assertIn("reason", result)
        self.assertIsInstance(result["reason"], str)
        self.assertTrue(result["sameResult"])
        
    def test_compare_different_python_code3(self):
        """Test comparison of equivalent Python code."""
        code1 = self.model.get_task("0091").data["output"]
        code2 = '\nimport torch\nimport esm\nimport biotite.structure.io as bsio\n\n# Load the ESMFold model\nmodel = esm.pretrained.esm_msa1b_t12_100M_UR50S()\nmodel = model.eval().cuda()\n\n# Set the input sequence\nsequence = \"MKTVRQERLKSIVRILERSKEPV\"\n\n# Perform structure prediction\nwith torch.no_grad():\n    output = model.infer_pdb(sequence)\n\n# Save the output structure to a PDB file\nwith open(\"output.pdb\", \"w\") as f:\n    f.write(output)\n'
        
        result = self.comparer.compare(code1, code2, 'Python code')
#        self.pp.pprint("Test code 2 ------------------------------------------------------------------->")
#        self.pp.pprint(f"code1: {code1}")
#        self.pp.pprint(f"code2: {code2}")
#        self.pp.pprint(f"result: {result}")
        
        self.assertIn("sameResult", result)
        self.assertIn("reason", result)
        self.assertIsInstance(result["reason"], str)
        self.assertFalse(result["sameResult"])
        

    def test_compare_equivalent_cli_commands1(self):
        """Test comparison of equivalent CLI commands."""
        cmd1 = "pip install torch==1.9.0 --user"
        cmd2 = "pip install --user torch==1.9.0"
        
        result = self.comparer.compare(cmd1, cmd2, 'Bash script')
#        self.pp.pprint("Test equivalent cli commands 1 ------------------------------------------------------------------->")
#        self.pp.pprint(f"cmd1: {cmd1}")
#        self.pp.pprint(f"cmd2: {cmd2}")
#        self.pp.pprint(f"result: {result}")
        
        self.assertIn("sameResult", result)
        self.assertIn("reason", result)
        self.assertIsInstance(result["reason"], str)
        self.assertTrue(result["sameResult"])

    def test_compare_different_cli_commands1(self):
        """Test comparison of equivalent CLI commands."""
        cmd1 = "pip install torch==1.9.0 --user"
        cmd2 = "pip install --user torch==0.9.0"
        
        result = self.comparer.compare(cmd1, cmd2, 'Bash script')
#        self.pp.pprint("Test different cli commands 1 ------------------------------------------------------------------->")
#        self.pp.pprint(f"cmd1: {cmd1}")
#        self.pp.pprint(f"cmd2: {cmd2}")
#        self.pp.pprint(f"result: {result}")
        
        self.assertIn("sameResult", result)
        self.assertIn("reason", result)
        self.assertIsInstance(result["reason"], str)
        self.assertFalse(result["sameResult"])


if __name__ == '__main__':
    unittest.main() 