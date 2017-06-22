from os import *
from Crypto.Hash import SHA256
import cipher.crypt as crypt
import sync
import json


loc = json.load("config/loc.json")
block_size = 8192


class File:
    def __init__(self, path = None, sha256 = None, last_modified = 0):
        self.path = path
        self.last_modified = self.last_modified
        if self.path: 
            if os.path.isfile(path):
                tmp_hash = SHA256.new()
                tmp_hash.update(open(path).read())
                self.sha256 = tmp_hash.digest()
            else:
                self.sha256 = sha256


class Block:
    def __init__(self, name, frompath):
        self.name = name
        self.frompath = frompath


def read_file_list():
    get_file_list()
    files = []
    list_file = open(f"files/filelist.blk", "r")
    lines = list_file.readlines
    for line in lines:
        files.append(File(filename=line))
    return files


def read_block_list(file):
    get_block_list()
    list_file = open(f"files/{file.filename}.blk", 'r')
    lines = list_file.readlines
    try:
        file.last_modified = int(lines[0])
        file.sha256 = lines[1]
    # to do process paths with spaces
        for i in lines[2:]:
            blocks.append(i.split(" "))      
    except IndexError:
        print(f"Error processing file {filename}")
    return blocks


def get_file_list():
    print("Fetching file list")
    for server in loc["servers"]:
        if sync.copy("filelist.blk", server, loc["here"]):
            print("Successfully downloaded file list")
     #  if the file is ok
            return
    print("Error downloading file list")


def get_block_list(filelist, file):
    for server in loc["servers"]:
        sync.copy(f"{file.filename}", server, loc["here"])


def update():
    files = get_file_list()
    for file in files:
        if not exist(file.path):
            download(file)
            continue
        localfile = File(path = file.path)
        if localfile.sha256 != file.sha256:
            if localfile.last_modified >= file.last_modified:
                upload(localfile)
            else:
                download(file)


def download_block(block):
    for i in block.frompath:
        if sync.copy(sync.CopyTask(block.name, block.frompath, loc["here"])):
           break
        print(f"Downloading from {block.frompath} failed...")
    print(f"Error cannot download {block.name}")


def upload_block(block):
    for i in block.frompath:
        if not sync.copy(sync.CopyTask(block.name, loc["here"], frompath)):
            print(f"Uploading to {block.frompath} failed...\
                    Remove the entry from the block list afterwards")


def download(file):
    blocks = read_block_list(file)
    with Pool(sync.MAX_PROCESSES) as p:
        p.map(download_block, blocks)
        

def upload(file):
    blocks = read_block_list(file)
    with Pool(sync.MAX_PROCESSES) as p:
        p.map(upload_block, blocks)    


def filename_gen(filename):
    n = 0
    while True:
        yield filename + "_{}".format(n)
        n = n + 1


"""
input filename
generate filename_0, filename_1 ...
"""
def split(filepath,partsize=block_size):
    filedir,name=os.path.split(filepath)
    stream=open(filepath,'rb');
    for partname in filename_gen(name):
        part_stream=open(partname,'wb')
        read_size=1024
        read_part_total=0
        read_once_length=0
        #write for part of the block
        while(read_part_total < partsize):
            read_content=stream.read(read_size)
            
            read_once_length=len(read_content)
            if(read_once_length>0):
                part_stream.write(read_content)
            else:
                break
            read_part_total+=read_once_length
        part_stream.close()
        if(read_once_length==0):
            break
    print('Done')
                

"""
input file name, cluster name
gernerate {filename} from {clustername_0, clustername_1, ...}
"""
def merge(filename, filepath, partsize=block_size):
    fileobj = open(filename,'wb')
    once_read_size = 1024
    try:
        for filepart in filepath:
            partstream=open(filepart,'rb')
            read_content_total=0
            while(read_content_total<partsize):
                read_once=0
                read_content=partstream.read(once_read_size)
                read_once=len(read_content)
                if(read_once>0):
                    fileobj.write(read_content)
                else:
                    break
                
                read_content_total+=read_once
            partstream.close()
    except FileNotFoundError:
        fileobj.close()
