import os
import shutil
from web_copy import copy_items

source_dir = "./static"

dest_dir = "./public"

def main():
    print("Deleting public directory...")
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    copy_items(source_dir, dest_dir)

if __name__ == "__main__":
    main()
