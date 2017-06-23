import os
from os import path
from Crypto.Hash import SHA256
import cipher.crypt as crypt
import sync
import json
import math
import secrets


loc = json.load("config/loc.json")
block_size = 8192
copy_count = 1

class File:
    def __init__(self, path = None, sha256 = None, last_modified = 0):
        self.path = path
        self.last_modified = self.last_modified
        if self.path: 
            if os.path.isfile(path):
                self.sha256 = get_sha256(path)
            else:
                self.sha256 = sha256

class Block:
    def __init__(self, name, frompath):
        self.name = name
        self.frompath = frompath

def get_sha256(path):
    if os.path.isfile(path):
         tmp_hash = SHA256.new()
         tmp_hash.update(open(path).read())
         return tmp_hash.digest()
    else:
        return None
 

def gen_file_list():
    files = [i for i in os.scandir("files/") if path.isfile(i)]
    return files

def gen_block_list(file):
    print(f"generating block list for {file.filename}")
    timestamp = int(os.stat(join("files", file.filename)).st_ctime)
    if file.sha256:
        sha256 = file.sha256
    else:
        sha256 = get_sha256(os.path.join("files", file.filename))
    lines = []
    lines.append(str(timestamp))
    lines.append(str(sha256))
    block_file = open(f"files/{file.filename}.blk", "w")
    block_count = math.ceil(float(os.getsize(join("files", file.filename))) / block_size)
    for i in range(block_count):
        frompath = []
        for j in range(copy_count):
            randserver = secrets.choice(loc["servers"])
            if not randserver in frompath:
                frompath.append(randserver)
        lines.append(frompath.join(" "))
    block_file.writelines(lines)
    print(f"block list successfully generated")
        
        

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
        

"""
undone: get_block_list
        get_file_list
"""

def get_block_list(cls, file):
    n = 0
    while True:
        blockname = file + "_{}".format(n)
        if not os.path.exists(blockname):
            break
        else:
            self.append(blockname)
            n = n + 1
        

    
def get_file_list(cls):
    dir = './files'
    myfile = open('./files/filelist.blk','w')
    list = os.listdir(dir)
    for line in list:
        filepath = os.path.join(dir,line)
        myfile.write(''+line +'\n')
    myfile.close()

def block_list_addr(filename):
    #get the block list addr of given file 
    filelist=open('./filelist','r')
    i=0;
    while True:
        line1=filelist.readline().strip('\n')
        line2=filelist.readline().strip('\n')
        if len(line2)==0:
            print('No such file!\n')
            break;
        if filename==line1:
            addr=int(line2);#assume that block list addr is a number
            break;
        i=i+1
    filelist.close();
    return addr    


def block_list_map(file):
#give the file name,  find the addr of blocklist of the file, and give a list of block map
#e.g. [[1,2,3],[2,3],[1,2]]
    addr=block_list_addr(file)
    #assume that bl of a file is file+'_bl'
    #Download is waiting for implemented...
    Download(file+'_bl',addr)
    bl=open(file+'_bl','r')
    bl.readline();
    bl.readline();
    line=bl.readline();
    blocknum=int([x for x in line.split(' ')][1])
    blockmap=[]
    for i in range(blocknum):
        line=bl.readline().strip('\n')
        blockmap.append([int(x) for x in line.split(' ')])#assume that block list addr is a number
    bl.close()
    return blockmap

