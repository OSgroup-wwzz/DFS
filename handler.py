from os import *
from Crypto.Hash import SHA256


"""

"""

class Utils:

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
        files = get_file_list()
        for file in files:
            if not exist(file.path):
                download(file)
                continue
            localfile = Utils.File(path = file.path)
            if localfile.sha256 != file.sha256:
                if localfile.last_modified >= file.last_modified:
                    upload(localfile)
                else:
                    download(file)
    
    
    @classmethod
    def download(cls, file):
        files = get_block_list(file)
        # TO-DO

    @classmethod
    def upload(cls, file):
        files = get_block_list(file)
        # TO-DO
            

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
    def split(cls, filepath,partsize=block_size):
        filedir,name=os.path.split(filepath)
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

