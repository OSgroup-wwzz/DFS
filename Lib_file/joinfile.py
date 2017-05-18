# !/usr/bin/env python
# coding: utf-8
import os
def joinfile(filepath,partnum,last_part_size,partsize=1024):
#filepath:the collected blocks path, raw filepath needed
#partsize:the default blocks size
#join the blocks into a integral file
    path=os.path.abspath(filepath)
    #if(os.path.exists(path)==True):
    #    print("File already exists!")
    fileobj=open(path,'wb')
    name,ext=os.path.splitext(path)
    blocknum=0

    while(blocknum<=partnum):
        blockpath=os.path.join(name+'_'+str(blocknum)+'d'+ext) #assume the block is already downloaded from cloud disk to local disk
        if(os.path.exists(blockpath)==False):
            break
        blockfile=open(blockpath,'rb')
        once_read_size=1024
        read_content_total=0
        if(blocknum==partnum):
            partsize=last_part_size
        while(read_content_total<partsize):
            read_once=0
            if(read_content_total+once_read_size>partsize):
                once_read_size=partsize-read_content_total
            read_content=blockfile.read(once_read_size)
            read_once=len(read_content)
            #if(read_once>0 and blocknum==partnum-1):
            #    fileobj.write(read_content[:last_part_size])
            if(read_once>0):
                fileobj.write(read_content)
            else:
                break
            
            read_content_total+=read_once
        blockfile.close()
        blocknum=blocknum+1
    fileobj.close()



#test
#if __name__=='__main__':
#    files=[r"D:\HAPPY\baikejun\OSH\DFS-feasibility-report-master\Feasibility_0",r"D:\HAPPY\baikejun\OSH\DFS-feasibility-report-master\Feasibility_1",r"D:\HAPPY\baikejun\OSH\DFS-feasibility-report-master\Feasibility_2"]
#    joinfile(files)
          
            
            
        
        
