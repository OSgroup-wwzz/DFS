import os


class Handler:
    storage_count = 1
    block_size = 1024


    def update():
        files = get_file_list()
        for file in files:
            if not exist(file.path):
                download(file)
                continue
            localfile = get_file(file.path)
            if localfile.sha1 != file.sha1:
                if localfile.last_modified >= file.last_modified:
                    upload(localfile)
                else:
                    download(file)
    
    
    def download(file):
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

