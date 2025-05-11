# Static-Site-Generator

This an Intelligent system that converts markdown page into an HTML page as a blog

## Architecture of the System

![System Attribute](./content/documentation/NodesEnums.jpg)

## TextNode

Attributes:

* text - The text
* textype - The type of the text, whether a `TEXT`, `BOLD`, `ITALICS`, `CODE`, `LINKS`, `IMAGES`.
* Url - Depending on whether the textype is an image or a link, it would have this attribute or else it is `None`.

## HTMLNode

The HTMLNode is the class for HTML tag objects. We have 2 child class of this class which are the ParentNode and LeafNode. This difference between the ParentNode and the LeafNode is that the ParentNode, just like the name has children of HTMLNodes while the LeadNode has no children. We catered for this in our inherited class code.

Attributes:

* tag - the HTML tag of the block, whether a `p`, `b`, `h1` etc.
* value - The content or text in the tag.
* children - This is another HTMLNode, only the ParentNode has childrens.
* props: This is a dictionary of attributes in the HTML tags. Images and links always have this attributes.

## Enums

### TextType

We used sumtypes to cater for cases of text type:

* TEXT - This is when all the content is a text.
* BOLD - This is when we the text is a bolded text (**boy**).
* ITALIC - When the text is in italics (__boy__).
* CODE - When the text is a code (`fn boy()`).
* LINK - When the text is a link (`[bootdev](https://i.imgur.com/zjjcJKZ.png)`).
* IMAGES - When the text is an image (`![image](https://i.imgur.com/zjjcJKZ.png)`).

### BlockType

We used sumtypes here also. For each block in the markdown, they can either be of the following types:

* PARAGRAPHS - A paragraph block
* HEADINGS - In markdown, a paragraph block starts with either one (1) to six(6) hash (#) depending on the six of the header.
* CODE - a code block begins and ends with a tick (``).
* QU0TE - a quote in markdown starts with a arrow character (>).
* UNORDERED LIST - An unordered list in markdown starts with a dash and dot followed by the text (`- boy`).
* ORDERED LIST - An ordered list in markdown starts with a number followed by a . character and a space. The number must start at 1 and increment by 1 for each line.

![inline functions](./content/documentation/Inline_functions.jpg)

* `extract_markdown_images`: This function extracts patterns of images in a markdown text. We implemented the concept of [regex](https://medium.com/towards-data-engineering/regular-expressions-an-art-of-manipulating-strings-642aa5cf94f3) in this function.

* `extract_markdown_links`: This function extracts patterns of links in a markdown text. We implemented the concept of [regex](https://medium.com/towards-data-engineering/regular-expressions-an-art-of-manipulating-strings-642aa5cf94f3) in this function.

* `split_nodes_delimiter`: This functions helps us to seperate textnode that have delimiter characters for either bold, italics or code.

* `split_nodes_link`: This functions helps us to seperate textnode that have link pattern text.

* `split_nodes_image`: This functions helps us to seperate textnode that have image pattern text.

* `text_to_textnode`: In this function, we aggregrate all 3 split functions (`split_nodes_delimiter`,`split_nodes_link`, and `split_nodes_image`) to seamlessly process a text with delimiter, image, and link pattern into seperate textnodes.

```
text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

result = [
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
            ]
```