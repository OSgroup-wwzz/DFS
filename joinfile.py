# !/usr/bin/env python
# coding: utf-8
import os
def joinfile(filepath,partsize=1024):
#filepath:the collected blocks path, raw filepath needed
#partsize:the default blocks size
#join the blocks into a integral file

    blocknum=len(filepath)
    name,ext=os.path.splitext(filepath[0])
    file_obj_name=os.path.join(name[0:-2]+ext)
    print(file_obj_name)
    fileobj=open(file_obj_name,'wb')
    once_read_size=1024
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
    fileobj.close()
#test
if __name__=='__main__':
    files=[r"D:\HAPPY\baikejun\OSH\DFS-feasibility-report-master\Feasibility_0",r"D:\HAPPY\baikejun\OSH\DFS-feasibility-report-master\Feasibility_1",r"D:\HAPPY\baikejun\OSH\DFS-feasibility-report-master\Feasibility_2"]
    joinfile(files)
          
            
            
        
        