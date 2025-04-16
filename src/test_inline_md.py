import unittest
from inline_md import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_node_image,
    split_node_link,
    text_to_textnodes
)

from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )


class TestRegex(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_extract_markdown_links_multiple(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            matches,
        )


class TestSplitNodeImagesLinks(unittest.TestCase):
    def test_split_node_images(self):
        text = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        splitted_text = split_node_image([text])
        self.assertEqual(
            splitted_text,
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
        )

    def test_split_joint_image(self):
        text = [
            TextNode(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
                TextType.TEXT,
            ),
            TextNode("This is text with no images", TextType.TEXT),
        ]
        splitted_text = split_node_image(text)
        self.assertEqual(
            splitted_text,
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode("This is text with no images", TextType.TEXT),
            ],
        )

    def test_split_node_images_no_images(self):
        text = TextNode("This is text with no images", TextType.TEXT)
        splitted_text = split_node_image([text])
        self.assertEqual(
            splitted_text, [TextNode("This is text with no images", TextType.TEXT)]
        )

    def test_split_node_1_image(self):
        text = TextNode("![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        splitted_text = split_node_image([text])
        self.assertEqual(
            splitted_text,
            [TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")],
        )

    def test_split_node_3_images(self):
        text = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) and ![third](https://i.imgur.com/)",
            TextType.TEXT,
        )
        splitted_text = split_node_image([text])
        self.assertEqual(
            splitted_text,
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" and ", TextType.TEXT),
                TextNode("third", TextType.IMAGE, "https://i.imgur.com/"),
            ],
        )

    def test_split_node_link(self):
        text = TextNode(
            "[bootdev](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        splitted_text = split_node_link([text])
        self.assertEqual(
            splitted_text,
            [
                TextNode("bootdev", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
        )

    def test_split_joint_link(self):
        text = [
            TextNode(
                "This is text with an [Scott](https://i.imgur.com/zjjcJKZ.png) and another [Jake](https://i.imgur.com/3elNhQu.png)",
                TextType.TEXT,
            ),
            TextNode("This is text with no images", TextType.TEXT),
        ]

        splitted_text = split_node_link(text)

        self.assertEqual(
            splitted_text,
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("Scott", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("Jake", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
                TextNode("This is text with no images", TextType.TEXT),
            ],
        )

    def test_split_node_images_no_link(self):
        text = TextNode("This is text with no images", TextType.TEXT)
        splitted_text = split_node_link([text])
        self.assertEqual(
            splitted_text, [TextNode("This is text with no images", TextType.TEXT)]
        )

    def test_split_node_1_link(self):
        text = TextNode("[Peace](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        splitted_text = split_node_link([text])
        self.assertEqual(
            splitted_text,
            [TextNode("Peace", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png")],
        )

    def test_split_node_3_link(self):
        text = TextNode(
            "![Moses](https://i.imgur.com/zjjcJKZ.png) and another [Ajalon](https://i.imgur.com/3elNhQu.png) and [David](https://i.imgur.com/)",
            TextType.TEXT,
        )
        splitted_text = split_node_link([text])
        self.assertEqual(
            splitted_text,
            [
                TextNode(
                    "![Moses](https://i.imgur.com/zjjcJKZ.png) and another ",
                    TextType.TEXT,
                ),
                TextNode("Ajalon", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("David", TextType.LINK, "https://i.imgur.com/"),
            ],
        )

    def all_split_1(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        self.assertEqual(
            result,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )


if __name__ == "__main__":
    unittest.main()
