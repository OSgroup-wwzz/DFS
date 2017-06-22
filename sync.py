import os
import subprocess
import json
from multiprocessing import Process,Lock

"""
Upload and download, API handling services provided by rclone.org

VERY IMPORTANT:
it reads config from a JSON file: config.json

drawback: no exception catching

Example:

from:**here**:/home/exampleuser/examplerfolder  
to:**there**:
filename(type EOF to stop):myfile

**here** is the name of the local drive you created in the rclone
**there** is another drive 

"""
config = json.load(open('config/sync.json'))      

class CopyTask:
    def __init__(self, filename, frompath, topath):
        self.filename = filename
        self.frompath = self.frompath
        self.topath = self.topath

"""
return a nonzero value for success
needs revision
"""
def copy(copytask):
    status = subprocess.call(["rclone", "copy", f"{copytask.frompath}/{copytask.filename}", f"{topath}"])
    if status < 0:
        print(f"Copy process terminated abnormally(status {status})")
        return 0
    else:
        print(f"Copy from {copytask.frompath}/{copytask.filename} to {copytask.topath}/{copytask.filename} completed successfully")
        return 1


"""
Concurrently manage copy processes which run in parallel
Remove it?
"""
def batch_copy(file_list):
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
