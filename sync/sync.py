import os
import subprocess
import json
from multiprocessing import Process,Lock

"""
Upload and download, API handling services provided by rclone.org

VERY IMPORTANT:
it reads config from a JSON file: config.json

drawback: no exception catching
"""
config = json.load(open('config.json'))      

class CopyTask:
    def __init__(self, filename, frompath, topath):
        self.filename = filename
        self.frompath = self.frompath
        self.topath = self.topath
 

def copy(copytask):
    status = subprocess.call(["rclone", "copy", f"{copytask.frompath}/{copytask.filename}", f"{topath}"])
    if status < 0:
        print(f"Copy process terminated abnormally(status {status})")
    else:
        print(f"Copy from {copytask.frompath}/{copytask.filename} to {copytask.topath}/{copytask.filename} completed successfully")


"""
Concurrently manage copy processes which run in parallel
"""
def batch_copy(copytasklist):
    count = 0
    count_lock = Lock()
    # alive indicates if any process is alive
    alive = False
    proc_list = [None] * config["MAX_PROCESSES"]
    while count < len(file_list) or alive:
        alive = False
        for i in range(config["MAX_PROCESSES"]):
            try:
                # Maybe here will be a TypeError or something
                if proc_list[i] and proc_list[i].is_alive():
                    alive = True
                    continue
                else:
                    proc_list[i].join(0)
                    count_lock.acquire()
                    if count < len(file_list):
                        proc_list[i] = Process(target=copy, args=(file_list[count]))
                        proc_list[i].start()
                        alive = True
                        count += 1
                    count_lock.release()
            except Exception:
                    count_lock.acquire()
                    if count < len(file_list):
                        proc_list[i] = Process(target=copy, args=(file_list[count]))
                        alive = True
                        count += 1
                        proc_list[i].start()
                    count_lock.release()
    print("Batch copy complete")

if __name__=="__main__":
    frompath = input("from:")
    topath = input("to:")
    filelist = []
    try:
        filename = input("filename(type EOF to stop):")
        if filename:
            filelist.append(CopyTask(filename, frompath, topath))
    except EOFError:
        pass
    batch_copy(filelist)
