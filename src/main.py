import os
import shutil
from web_copy import copy_items
from gen_content import generate_page

source_dir = "./static"

dest_dir = "./public"

from_path = "./content/index.md"
template_path = "./template.html"
dest_path = "./public/index.html"

def main():
    print("Deleting public directory...")
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    copy_items(source_dir, dest_dir)
    generate_page(from_path, template_path, dest_path)

if __name__ == "__main__":
    main()
