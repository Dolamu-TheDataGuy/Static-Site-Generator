import re

def extract_markdown_images(text: str):

    pattern = r"!\[(\D+?)\]\((https\:\/\/[A-Za-z0-9._]*\/[A-Za-z0-9._/@$#]*)\)"

    matches = re.findall(pattern, text)
    if matches:
        return matches
    return None

def extract_markdown_links(text:str):

    patterns = r"\[(\D+?)\]\((https\:\/\/[A-Za-z0-9./@_]*)"

    matches = re.findall(patterns, text)
    if matches:
        return matches
    return None



