from filesystem import *
import unittest


class TestFileSystem(unittest.TestCase):

    def setUp(self):
        self.replace_file = "./tests/files/replace_file.txt"
        self.new_file = "./tests/files/new_file.txt"

    def test_replace_file(self):
        tuples = [
            ("cool", "gaaf"),
            ("de bom", "de bob")
        ]

        replace_in_file(self.replace_file, self.new_file, tuples)
        expected_lines =[
            "ik ben gaaf\n",
            "gaaf ben ik\n",
            "toch ben ik de bob",
        ]
        with open(self.new_file, "r") as f:
            lines = [l for l in f.readlines()]
            self.assertEqual(lines, expected_lines)



