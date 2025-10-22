import unittest
from cyberguard.engine import Shell
import pathlib

class TestShell(unittest.TestCase):
    def setUp(self):
        logs_dir = pathlib.Path(__file__).parents[1] / "cyberguard" / "data" / "logs"
        self.sh = Shell(logs_dir)

    def test_cat_missing(self):
        out = self.sh.cat("missing.log")
        self.assertIn("No such file", out)

    def test_ps(self):
        out = self.sh.ps()
        self.assertIn("nginx", out)

    def test_block_ip(self):
        out = self.sh.block_ip("1.2.3.4")
        self.assertIn("blocked", out)

if __name__ == "__main__":
    unittest.main()
