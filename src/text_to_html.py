from textnode import TextNode, TextType
from text_regex import extract_markdown_images, extract_markdown_links

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



