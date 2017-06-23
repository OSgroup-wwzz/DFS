import handler
import setting
import watchdog.test_watchdog as watch

"""
main.py

put all things together
"""

if __name__ == '__main__':
    init()
    filelist = open(f"files/filelist.blk", "w")
    files = gen_file_list()
    for file in files:
        filelist.write(f"{file.filename}"+"\n")
        gen_block_list(file)
    
    event_handler1 = MyFileMonitor()
    observer = Observer()
    watch = observer.schedule(event_handler1, path='.', recursive=True)

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    observer.start()
    try:
        while True:
            time.sleep(60)
            update()
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    