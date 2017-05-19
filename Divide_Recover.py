import os
import sys
from Lib_file.divide import splitfile
from Lib_file.joinfile import joinfile
from Lib_file.encode_file import encode_file
from Lib_file.decode_file import decode_file
#partnum should be no more than 21 !!!!
#the encode/decode procedure might be very slow
#use 4 additionsl files as redundancy
#use erasure code (reed-solomon code)
#allow 2 blocks (at most) damaged at one time

def divide_file(filepath,partsize=1024):
    (partnum,last_part_size)=splitfile(filepath,partsize)
    encode_file(filepath,partnum,partsize)
    return (partnum,last_part_size)

def recover_file(filepath,partnum,last_part_size,partsize=1024):
    decode_file(filepath,partnum,partsize)
    joinfile(filepath,partnum,last_part_size,partsize)

def del_temp_files(filepath,partnum):
    path=os.path.abspath(filepath)
    name,ext=os.path.splitext(path)
    blocknum=0
    while(blocknum<=partnum+4):
        blockpath=os.path.join(name+'_'+str(blocknum)+ext)
        os.remove(blockpath)
        if(blocknum<=partnum):
            blockpath=os.path.join(name+'_'+str(blocknum)+'d'+ext)
            os.remove(blockpath)
        blocknum=blocknum+1

#test
if __name__=='__main__':
    filepath='./server.py'
    (partnum,last_part_size)=divide_file(filepath)
    print 'divide file done!'
    print partnum+1,last_part_size
    os.rename(filepath,'./server_temp.py')
    print 'rename "./server.py" -> "./server_temp.py"'
    recover_file(filepath,partnum,last_part_size)
    print 'recover file done!'
    del_temp_files(filepath,partnum)
    print 'delete all temp files'
    #joinfile(filepath,partnum)
