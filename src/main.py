import os
import sys
import shutil
from web_copy import copy_items
from gen_content import generate_pages_recursively

source_dir = "./static/images"

dest_dir = "./docs/images"

from_path = "./content"
template_path = "./template.html"
dest_path = "./docs"
default_base_path = "/"


def main():
    base_path = default_base_path
    if len(sys.argv) > 1:
        base_path = sys.argv[1]

    if os.path.exists(dest_dir):
        print("Deleting destination directory because it exists in your repo...")
        shutil.rmtree(dest_dir)
    copy_items(source_dir, dest_dir)
    generate_pages_recursively(from_path, template_path, dest_path, base_path)

if __name__ == "__main__":
    main()
