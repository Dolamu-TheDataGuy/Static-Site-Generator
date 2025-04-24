import os
import shutil


def copy_items(source_dir, dest_dir):
    
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        
    
    for item in os.listdir(source_dir):
        source_item = os.path.join(source_dir, item)
        dest_item = os.path.join(dest_dir, item)
        
        # Base case
        if os.path.isfile(source_item):
            print(f"Copying file: {source_item} to {dest_item}")
            shutil.copy2(source_item, dest_item)
            
        # Recursive case    
        else:
            print(f"Copying directory: {source_item} to {dest_item}")
            copy_items(source_item, dest_item)


def main():
    source_dir = "/home/dolzy/workspace/github.com/Dolamu-TheDataGuy/Static_Site_Generator/static"

    dest_dir = "/home/dolzy/workspace/github.com/Dolamu-TheDataGuy/Static_Site_Generator/public"
    
    copy_items(source_dir, dest_dir)

    
if __name__ == "__main__":
    main()
