import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from pipeline import run


class PipelineTest(unittest.TestCase):
    def test_cpu_pipeline_is_deterministic(self):
        first, second = run(1000, "cpu"), run(1000, "cpu")
        self.assertEqual(first["checksum"], second["checksum"])
        self.assertEqual(first["groups"], 16)

    def test_validates_input(self):
        with self.assertRaises(ValueError):
            run(0)


if __name__ == "__main__":
    unittest.main()
