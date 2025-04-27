import os
import shutil
from web_copy import copy_items
from gen_content import generate_pages_recursively

source_dir = "./static/images"

dest_dir = "./public/images"

from_path = "./content"
template_path = "./template.html"
dest_path = "./public"

def main():
    print("Deleting public directory...")
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    copy_items(source_dir, dest_dir)
    generate_pages_recursively(from_path, template_path, dest_path)

if __name__ == "__main__":
    main()
