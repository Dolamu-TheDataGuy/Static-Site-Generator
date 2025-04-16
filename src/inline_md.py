import re
from textnode import TextNode, TextType

def split_nodes_delimiter(nodes, delimiter, text_type):
    result = []

    for node in nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue

        splitted_text = node.text.split(delimiter)

        # if no split occured, just add the original node
        if len(splitted_text) == 1:
            result.append(node)
            continue

        # if we have an even number of split, it means we have unmatched delimiters
        if len(splitted_text) % 2 == 0:
            raise Exception("Unmatched delimiters")

        for i in range(len(splitted_text)):
            if splitted_text[i] == "":
                continue

            # Even indices are regular text
            if i % 2 == 0:
                result.append(TextNode(splitted_text[i], TextType.TEXT))
            else:  # odd indices are the content between delimiters
                result.append(TextNode(splitted_text[i], text_type))
    return result


def extract_markdown_images(text: str):

    pattern = r"!\[(\D+?)\]\((https\:\/\/[A-Za-z0-9._]*\/[A-Za-z0-9._/@$#]*)\)"

    matches = re.findall(pattern, text)
    if matches:
        return matches
    return []


def extract_markdown_links(text: str):

    patterns = r"(?<!!)\[(\D+?)\]\((https\:\/\/[A-Za-z0-9./@_]*)"

    matches = re.findall(patterns, text)
    if matches:
        return matches
    return []


def split_node_image(nodes):
    result = []
    for node in nodes:
        if node.text_type != TextType.TEXT:
            result.append(TextNode(node.text, node.text_type, node.url))
            continue
        text = node.text
        patterns_in_text = extract_markdown_images(text)

        # Base case
        if len(patterns_in_text) == 0:
            result.append(TextNode(text, TextType.TEXT))
            continue

        if len(patterns_in_text) > 0:
            splitted_text = text.split(
                f"![{patterns_in_text[0][0]}]({patterns_in_text[0][1]})", maxsplit=1
            )
            before = splitted_text[0]
            if before != "":
                result.append(TextNode(before, node.text_type))
            image = TextNode(
                patterns_in_text[0][0], TextType.IMAGE, patterns_in_text[0][1]
            )
            result.append(image)
            after = splitted_text[1]
            if after != "":
                after = split_node_image([TextNode(splitted_text[1], TextType.TEXT)])
            result.extend(after)
    return result


def split_node_link(nodes):
    result = []
    for node in nodes:
        if node.text_type != TextType.TEXT:
            result.append(TextNode(node.text, node.text_type, node.url))
            continue
        text = node.text
        patterns_in_text = extract_markdown_links(text)

        # Base Case
        if len(patterns_in_text) == 0:
            result.append(TextNode(text, TextType.TEXT))
            continue

        if len(patterns_in_text) > 0:
            splitted_text = text.split(
                f"[{patterns_in_text[0][0]}]({patterns_in_text[0][1]})", maxsplit=1
            )
            before = splitted_text[0]
            if before != "":
                result.append(TextNode(before, TextType.TEXT))
            link = TextNode(
                patterns_in_text[0][0], TextType.LINK, patterns_in_text[0][1]
            )
            result.append(link)
            after = splitted_text[1]
            if after != "":
                after = split_node_link([TextNode(splitted_text[1], TextType.TEXT)])
            result.extend(after)
    return result


def text_to_textnodes(all_text):
    node = [TextNode(all_text, TextType.TEXT)]

    # Applying image and link split
    node = split_node_image(node)
    node = split_node_link(node)

    # #Applying delimiter splits
    node = split_nodes_delimiter(node, "**", TextType.BOLD)
    node = split_nodes_delimiter(node, "_", TextType.ITALIC)
    node = split_nodes_delimiter(node, "`", TextType.CODE)

    return node
