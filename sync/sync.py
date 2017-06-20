import os
import subprocess
import json
from multiprocessing import Process

"""
Upload and download, API handling services provided by rclone.org
it reads config from a JSON file: config/config.json
drawback: no exception catching
"""
 
def upload(filename, localpath, cloudpath):
    status = subprocess.call(["rclone", "copy", f"{localpath}/{filename}", f"{cloudpath}/{filename}"])
    if status < 0:
        print(f"Upload process terminated abnormally(status {status})")


def download(filename, cloudpath, localpath):
    status = subprocess.call(["rclone", "copy", f"{cloudpath}/{filename}", f"{localpath}/{filename}"])
    if status < 0:
        print(f"Download process terminated abnormally(status {status})")


"""
Concurrently manage upload processes which run in parallel
"""
def batch_upload(file_list, localpath, cloudpath):
    count = 0
    proc_list = [None] * MAX_PROCESSES
    while count < len(file_list):
        for i in range(MAX_PROCESSES):
            try:
                # Maybe here will be a TypeError or something
                if not proc_list[i] or not proc_list[i].is_alive():
                    continue
                else:
                    proc_list[i].join(0)
                    count += 1
                    if count < len(file_list)
                        proc_list[i] = Process(target=upload, args=(file_list[i], localpath, cloudpath))
                        proc_list[i].start()
            except Exception:
                    if count < len(file_list)
                        proc_list[i] = Process(target=upload, args=(file_list[i], localpath, cloudpath))
                        proc_list[i].start()
    print("Upload complete")

