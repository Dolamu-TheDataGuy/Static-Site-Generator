import unittest
from gen_content import extract_title

class TestGenContent(unittest.TestCase):
    def test_extract_title_1(self):
        title_text = "# This is a title"
        title = extract_title(title_text)
        self.assertEqual(title, "This is a title")

    def test_extract_title_2(self):
        title_text = "#This is a title"
        with self.assertRaises(Exception):
            title = extract_title(title_text)

    def test_extract_title_3(self):
        title_text = "## This is a boy"
        with self.assertRaises(Exception):
            title = extract_title(title_text)


if __name__ == "__main__":
    unittest.main()
