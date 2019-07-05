import os, sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import argparse

    
class FolderChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        num_of_renames = 0
        for file in os.listdir(args.path):
            if os.path.abspath(file) == os.path.abspath(__file__):  # skip this very file
                continue     
            if os.path.isdir(file):          # skip if it's a folder
                continue
            if args.old in file:
                new_name = file.replace(args.old, args.new)
                print("renaming: {}  -->  {}".format(file, new_name))
                os.rename(args.path+'/'+file, args.path+'/'+new_name)
                num_of_renames += 1
        if num_of_renames:
            print("Done. Num of renamed files: {}".format(num_of_renames))
    

    
if __name__ == "__main__":    
    #input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--path',
        help='directory path to watch for changes',
        default ='.'
    )
    parser.add_argument(
        '--old',
        help='part of the filename to be replaced',
        required=True
    )
    parser.add_argument(
        '--new',
        help='what should be put in place of --old',
        required=True
    )
    args = parser.parse_args()
    


    
    event_handler = FolderChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, args.path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()