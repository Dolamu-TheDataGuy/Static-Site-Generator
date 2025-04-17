import unittest
from block_code import block_to_block_type, BlockType


class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph(self):
        text = "This is a simple paragraph."
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

    def test_heading(self):
        # Valid headings (1-6 # followed by space)
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)

        # Invalid headings
        self.assertEqual(block_to_block_type("####### Too many #"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("#No space"), BlockType.PARAGRAPH)

    def test_code(self):
        # Valid code block
        self.assertEqual(block_to_block_type("```\ncode here\n```"), BlockType.CODE)

        # Invalid code blocks
        self.assertEqual(block_to_block_type("```\ncode here"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("code here\n```"), BlockType.PARAGRAPH)

    def test_quote(self):
        # Valid quote blocks
        self.assertEqual(block_to_block_type("> This is a quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("> Line 1\n> Line 2"), BlockType.QUOTE)

        # Invalid quote blocks
        self.assertEqual(block_to_block_type("> Line 1\nLine 2"), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        # Valid unordered lists
        self.assertEqual(
            block_to_block_type("- Item 1\n- Item 2\n - Item 5"),
            BlockType.UNORDERED_LIST,
        )
        self.assertEqual(
            block_to_block_type("- Item 3\n- Item 4"), BlockType.UNORDERED_LIST
        )

        self.assertEqual(block_to_block_type("- Item 1\nItem 2"), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        # Valid ordered lists
        self.assertEqual(
            block_to_block_type("1. Item 1\n2. Item 2\n3. Item 3"),
            BlockType.ORDERED_LIST,
        )
        self.assertEqual(block_to_block_type("1. Item 1\nItem 2"), BlockType.PARAGRAPH)


unittest.main(argv=[""], verbosity=2, exit=False)
