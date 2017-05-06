# !/usr/bin/env python
# coding: utf-8
import os
def splitfile(filepath,partsize=1024):
#filepath:the file path to be divided
#partsize:the default blocks size
#divide the file into blocks   
    filedir,name=os.path.split(filepath)
    #ex:divide '/usr/aaa' into '/usr' and 'aaa'
    name,extname=os.path.splitext(name)
    
    stream=open(filepath,'rb');
    partnum=0
    
    while(True):
        partname= os.path.join(filedir+'\\'+name+'_'+str(partnum)+extname)
        print(partname)
        part_stream=open(partname,'wb')
        print('Completed',partnum)
        read_size=1024
        read_part_total=0
        read_once_length=0
        #write for part of the block
        while(read_part_total<partsize):
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
        partnum+=1
    print('Done')
#just for test
if __name__=='__main__':
    splitfile(r"D:\HAPPY\baikejun\OSH\DFS-feasibility-report-master\Feasibility")#raw string
                
                
        