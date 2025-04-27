import os
from block_markdown import markdown_to_html_node


def extract_title(markdown):

    lines = markdown.split("\n")

    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No title found in the markdown")


def generate_page(from_path, template_path, dest_path, base_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        md_content = f.read()
    with open(template_path, "r") as f:
        template_content = f.read()

    md_html_content = markdown_to_html_node(md_content).to_html()
    title = extract_title(md_content)
    template_content = template_content.replace("{{ Title }}", title)
    template_content = template_content.replace("{{ Content }}", md_html_content)
    template_content = template_content.replace('href="/', f'href="{base_path}')
    template_content = template_content.replace('src="/', f'src="{base_path}')
    if not os.path.exists(dest_path):
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(template_content)


def generate_pages_recursively(dir_path_content, template_path, dest_dir_path, base_path):
    folder_content = os.listdir(dir_path_content)
    
    for item in folder_content:
        item_path = os.path.join(dir_path_content, item)
        
        # Recursive case: if item is a directory
        if os.path.isdir(item_path):
            print(f"Found a directory: {item}")
            new_dest_dir_path = os.path.join(dest_dir_path, item)
            os.makedirs(new_dest_dir_path, exist_ok=True)
            generate_pages_recursively(item_path, template_path, new_dest_dir_path, base_path)
        
        # Base case: if item is a file or markdown file    
        elif item.endswith(".md"):
            print(f"Found a markdown file: Generating page for {item}")
            new_dest_path = os.path.join(dest_dir_path, item.replace(".md", ".html"))
            generate_page(item_path, template_path, new_dest_path, base_path)
            print(f"Generated page: {new_dest_path}")
