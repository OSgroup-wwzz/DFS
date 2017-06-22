import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, LoggingEventHandler
from watchdog.observers.api import ObservedWatch

## upload when on_modified() or on_created() or on_moved()
class MyHandler(FileSystemEventHandler):
    def __init__(self):
        FileSystemEventHandler.__init__(self)
    def on_modified(self, event):
        if event.src_path == "./uploads/":
            print ("uploads dictionary %s changed!" % event.src_path)
    def on_created(self, event):
        if event.src_path == "./uploads/":
            print ("uploads dictionary %s created!" % event.src_path)
    def on_moved(self, event):
         if event.src_path == "./uploads":
             print ("uploads dictionary %s moved!" % event.src_path)


class MyFileMonitor(FileSystemEventHandler):
    def __init__(self):
        super().__init__()

    def on_created(self, event):
        super().on_created(event)
        if not event.is_directory:
            print ("created name:[%s]" % event.src_path)

    def on_modified(self, event):
        super().on_created(event)
        if not event.is_directory:
            print ("modified name:[%s]" % event.src_path)
            

if __name__ == "__main__":
    event_handler1 = MyFileMonitor()
    observer = Observer()
    watch = observer.schedule(event_handler1, path='.', recursive=True)

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    #event_handler2 = LoggingEventHandler()  
    #observer.add_handler_for_watch(event_handler2, watch)      #为watch新添加一个event handler
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
