import os
import rs

def decode_file(filepath,partnum,partsize=1024):
    read_once_size=8
    partnum=partnum+1
    #print read_once_size, partnum, (partnum+4)*read_once_size,partnum*read_once_size##
    coder=rs.RSCoder((partnum+4)*read_once_size,partnum*read_once_size)
    path=os.path.abspath(filepath)
    name,ext=os.path.splitext(path)
    blocknum=0
    block=[]
    d_block=[]
    while(blocknum<partnum+4):
        blockpath=os.path.join(name+'_'+str(blocknum)+ext)
        if(os.path.exists(blockpath)==False):
            break
        if(blocknum<partnum):
            d_blockpath=os.path.join(name+'_'+str(blocknum)+'d'+ext)
            d_blockfile=open(d_blockpath,'wb')
            d_block.append(d_blockfile)
        blockfile=open(blockpath,'rb')
        block.append(blockfile)
        blocknum=blocknum+1
    while(True):
        blocknum=0
        content=''
        while(blocknum<partnum+4):
            read_content=block[blocknum].read(read_once_size)
            read_once=len(read_content)
            if(read_once==read_once_size):
                content=content+read_content
            elif(read_once==0 and blocknum<(partnum-1)):
                break
            elif(read_once>=0):
                content=content+read_content+'\0'*(read_once_size-read_once)
            else:
                break
            blocknum=blocknum+1
        if(read_once==0 and blocknum<(partnum-1)):
            break
        #origin_content=content[:partnum*read_once_size]
        decode_content=coder.decode(content)
        '''if(origin_content!=decode_content):
            blocknum=0
            while(blocknum<partnum):
                if(origin_content[blocknum*partnum:(blocknum+1)*partnum]!=decode_content[blocknum*partnum:(blocknum+1)*partnum]):
                    block[blocknum].write(decode_content[blocknum*partnum:(blocknum+1)*partnum])
                blocknum=blocknum+1'''
        blocknum=0
        while(blocknum<partnum):
            d_block[blocknum].write(decode_content[blocknum*read_once_size:(blocknum+1)*read_once_size])
            blocknum=blocknum+1
    blocknum=0
    while(blocknum<partnum+4):
        block[blocknum].close()
        if(blocknum<partnum):
            d_block[blocknum].close()
        blocknum=blocknum+1
