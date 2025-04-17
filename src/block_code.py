import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragragh"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


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
            bool_list.append(line.strip().startswith(">"))
        if all(bool_list):
            return BlockType.QUOTE
    elif markdown.startswith("-"):
        lines = markdown.split("\n")
        bool_list = []
        for line in lines:
            bool_list.append(line.strip().startswith("-"))
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
