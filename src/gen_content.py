import os
from block_markdown import markdown_to_html_node


def extract_title(markdown):

    lines = markdown.split("\n")

    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No title found in the markdown")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        md_content = f.read()
    with open(template_path, "r") as f:
        template_content = f.read()

    md_html_content = markdown_to_html_node(md_content).to_html()
    title = extract_title(md_content)
    template_content = template_content.replace("{{ Title }}", title)
    template_content = template_content.replace("{{ Content }}", md_html_content)

    if not os.path.exists(dest_path):
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(template_content)
