import time
import sys
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

class CustomEventHandler(LoggingEventHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_modified_time = time.time()

    def on_modified(self, event):
        super().on_modified(event)
        self.last_modified_time = time.time()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = CustomEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
            # Check if no file has been modified for 30 seconds
            if time.time() - event_handler.last_modified_time > 30:
                print("No new files detected for 30 seconds, stopping the script.")
                break
    except KeyboardInterrupt:
        observer.stop()
    observer.stop()
    observer.join()
