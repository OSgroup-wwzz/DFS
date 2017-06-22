import os
from Crypto.Hash import SHA256
import cipher.crypt as crypt
from sync.sync import copy,batch_copy

"""

"""

class utils:

    storage_count = 1
    block_size = 1024

    class File:
        def __init__(self, path = None, sha256 = None):
            self.path = path
            if self.path: 
                if os.path.isfile(path):
                    tmp_hash = SHA256.new()
                    tmp_hash.update(open(path).read())
                    self.sha256 = tmp_hash.digest()
                else:
                    self.sha256 = sha256

    @classmethod
    def update(cls):
        files = utils.get_file_list()
        for file in files:
            if not exist(file.path):
                utils.download(file)
                continue
            localfile = utils.File(path = file.path)
            if localfile.sha256 != file.sha256:
                if localfile.last_modified >= file.last_modified:
                    utils.upload(localfile)
                else:
                    utils.download(file)
    
    @classmethod
    def get_block_list(cls, file):
        n = 0
        while True:
            blockname = file + "_{}".format(n)
            if not os.path.exists(blockname):
                break
            else:
                self.append(blockname)
                n = n + 1
        

    @classmethod
    def get_file_list(cls):
        dir = './uploads'
        files = os.listdir(dir)
        for name in files:
            fullname=os.path.join(dir,name)
            self.append(fullname)

    @classmethod
    def download(cls, file):
        files = utils.get_block_list(file)
        # TO-DO: communicate with server to get the file
        
        

    @classmethod
    def upload(cls, file):
        #调用前先调用split(cls, filepath)
        files = utils.get_block_list(file)
        topath = './test_drive'  #test
        batch_copy(files, './uploads', topath)
        


    @classmethod
    def filename_gen(cls, filename):
        n = 0
        while True:
            yield filename + "_{}".format(n)
            n = n + 1


    """
    input filename
    generate filename_0, filename_1 ...
    """
    @classmethod
    def split(cls, filepath, partsize=block_size):
        filedir,name = os.path.split(filepath)
        stream=open(filepath,'rb');
        for partname in cls.filename_gen(name):
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
    @classmethod
    def merge(cls, filename, filepath, partsize=block_size):
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

