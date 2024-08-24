import shutil
import time
import logging
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

sourcedir = "C:/Users/User/Downloads"
dest_dir_sfx = "C:/Users/User/sounds"
dest_dir_music = "C:/Users/User/Music"
dest_dir_video = "C:/Users/User/Videos"
dest_dir_image = "C:/Users/User/Pictures"

def makeUnique(path):
    return path 

def move(dest, entry, name):
    file_exists = os.path.exists(dest + "/" + name)
    if file_exists:
        unique_name = makeUnique(name)
        os.rename(entry.path, unique_name)
    shutil.move(entry.path, dest)
    print(f"Moved {name} to {dest}")
class MoverHandler(FileSystemEventHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_modified_time = time.time()

    def on_modified(self, event):
        print(f"Detected modification in {sourcedir}") 
        self.last_modified_time = time.time()
        with os.scandir(sourcedir) as entries:
            for entry in entries:
                name = entry.name
                dest = sourcedir  
                if name.endswith(".wav") or name.endswith(".mp3"):
                    if entry.stat().st_size < 25000000 or "SFX" in name:
                        dest = dest_dir_sfx
                    else:
                        dest = dest_dir_music
                    move(dest, entry, name)
                        
                elif name.endswith(".mov") or name.endswith(".mp4"):
                    dest = dest_dir_video
                    move(dest, entry, name)
                    
                elif name.endswith(".jpg") or name.endswith(".jpeg") or name.endswith(".png") or name.endswith(".gif"):
                    dest = dest_dir_image
                    move(dest, entry, name)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    
    path = sourcedir
    print(f"Monitoring {path}...")  
    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(10)
            print("Watching for changes...")  
            
            if time.time() - event_handler.last_modified_time > 30:
                print("No new files detected for 30 seconds, stopping the script.")
                break
    except KeyboardInterrupt:
        observer.stop()
    observer.stop()
    observer.join()
