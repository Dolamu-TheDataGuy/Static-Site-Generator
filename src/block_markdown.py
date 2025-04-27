import re
import os
from htmlnode import ParentNode, HTMLNode, LeafNode
from inline_md import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks


def block_to_block_type(markdown):
    if markdown.startswith("#"):
        pattern = r"^#{1,6} .+"
        if re.match(pattern, markdown):
            return BlockType.HEADING
    elif markdown.startswith("```") and markdown.endswith("```"):
        return BlockType.CODE
    elif markdown.startswith(">"):
        lines = markdown.split("\n")
        bool_list = []
        for line in lines:
            if line:
                bool_list.append(line.startswith(">"))
        if all(bool_list):
            return BlockType.QUOTE
    elif markdown.startswith("- "):
        lines = markdown.split("\n")
        bool_list = []
        for line in lines:
            bool_list.append(line.startswith("- "))
        if all(bool_list):
            return BlockType.UNORDERED_LIST
    elif markdown.startswith("1. "):
        lines = markdown.split("\n")
        num_check = []
        for i, line in enumerate(lines, 1):
            if line.strip().startswith(f"{i}. "):
                num_check.append(True)
            else:
                num_check.append(False)
        if all(num_check):
            return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def block_create_html_node(block_type, markdown: str):
    if block_type == BlockType.HEADING:
        return header(markdown)
    if block_type == BlockType.PARAGRAPH:
        return paragragh(markdown)
    if block_type == BlockType.UNORDERED_LIST:
        return ParentNode(tag="ul", children=unordered_list_to_children(markdown))
    if block_type == BlockType.ORDERED_LIST:
        return ParentNode(tag="ol", children=ordered_list(markdown))
    if block_type == BlockType.QUOTE:
        return quote_block(markdown)
    if block_type == BlockType.CODE:
        return ParentNode(tag="pre", children=code_block(markdown))
    raise ValueError(f"Unknown block type: {block_type}")   


def text_to_children(text: str):
    # First convert raw markdown text to TextNode then convert each TextNode to HTMLNode
    # return a list of TextNodes
    text_nodes = text_to_textnodes(text)
    # return HTMLNodes for each TextNode
    htmlnodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
    return htmlnodes


def paragragh(text):
    check_newline = text.split("\n")
    if check_newline:
        new_text = " ".join(check_newline)
        node = text_to_children(new_text)
        parent_node = ParentNode(tag="p", children=node)
        return parent_node
    parent_node = ParentNode(tag="p", children=text_to_children(text))
    return parent_node


def unordered_list_to_children(text):
    new_list = text.split("\n")
    text_list = [sentence.strip("- ") for sentence in new_list]
    unordered_list = []
    for text in text_list:
        node = text_to_children(text)
        parent_node = ParentNode(tag="li", children=node)
        unordered_list.append(parent_node)
    return unordered_list


def header(text):
    harsh_number = harsh_num(text)
    strip_code = ("#" * harsh_number) + " "
    tag_text = text.strip(strip_code)
    return ParentNode(tag=f"h{harsh_number}", children=text_to_children(tag_text))


def quote_block(text):
    lines = text.split("\n")
    # print(new_text)
    text_list = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        text_list.append(line.lstrip(">").strip())
    content = " ".join(text_list)
    children = text_to_children(content)
    return ParentNode(tag="blockquote", children=children)


def code_block(text):
    if not text.startswith("```") or not text.endswith("```"):
        raise ValueError("Invalid code block")
    ntext = text[4:-3]
    NewTextNode = TextNode(ntext, TextType.CODE)
    code_leaf_node = text_node_to_html_node(NewTextNode)
    return [code_leaf_node]


def ordered_list(text):
    new_list = text.split("\n")
    text_list = [sentence.strip(f"{num}. ") for num, sentence in enumerate(new_list, 1)]
    ordered_list = []
    for text in text_list:
        node = text_to_children(text)
        parent_node = ParentNode(tag="li", children=node)
        ordered_list.append(parent_node)
    return ordered_list


def harsh_num(text):
    split_harsh = text.split(" ", 1)
    return int(len(split_harsh[0]))


def markdown_to_html_node(markdown):
    markdowns = markdown_to_blocks(markdown)

    all_section = []
    for mkd_section in markdowns:
        block_type = block_to_block_type(mkd_section)
        html_node = block_create_html_node(block_type, mkd_section)
        all_section.append(html_node)
    body_node = ParentNode(tag="div", children=all_section)
    return body_node

