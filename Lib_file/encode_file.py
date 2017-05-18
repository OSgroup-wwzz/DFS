import os
import Reed_Solomon.rs

def encode_file(filepath,partnum,partsize=1024):
    #read_once_size=32
    partnum=partnum+1
    '''if((partnum+4)*32<255):
        partnum=32
    else:
        partnum='''
    read_once_size=8
    coder=Reed_Solomon.rs.RSCoder((partnum+4)*read_once_size,partnum*read_once_size)
    path=os.path.abspath(filepath)
    name,ext=os.path.splitext(path)
    #blocknum=0
    ec1_path=os.path.join(name+'_'+str(partnum)+ext)
    ec2_path=os.path.join(name+'_'+str(partnum+1)+ext)
    ec3_path=os.path.join(name+'_'+str(partnum+2)+ext)
    ec4_path=os.path.join(name+'_'+str(partnum+3)+ext)
    ec1=open(ec1_path,'wb')
    ec2=open(ec2_path,'wb')
    ec3=open(ec3_path,'wb')
    ec4=open(ec4_path,'wb')
    blocknum=0
    block=[]
    while(blocknum<partnum):
        blockpath=os.path.join(name+'_'+str(blocknum)+ext)
        if(os.path.exists(blockpath)==False):
            break
        blockfile=open(blockpath,'rb')
        block.append(blockfile)
        blocknum=blocknum+1
    
    while(True):
        #read_once_size=32
        blocknum=0
        content=''
        while(blocknum<partnum):
            read_content=block[blocknum].read(read_once_size)
            read_once=len(read_content)
            if(read_once==read_once_size):
                content=content+read_content
            elif(read_once==0 and blocknum<partnum-1):
                break
            elif(read_once>=0):
                content=content+read_content+'\0'*(read_once_size-read_once)
            else:
                break
            blocknum=blocknum+1
        
        if(read_once==0 and blocknum<partnum-1):
            break
        c=coder.encode(content)
        r1=c[partnum*read_once_size:(partnum+1)*read_once_size]
        r2=c[(partnum+1)*read_once_size:(partnum+2)*read_once_size]
        r3=c[(partnum+2)*read_once_size:(partnum+3)*read_once_size]
        r4=c[(partnum+3)*read_once_size:(partnum+4)*read_once_size]
        ec1.write(r1)
        ec2.write(r2)
        ec3.write(r3)
        ec4.write(r4)
    blocknum=0
    while(blocknum<partnum):
        block[blocknum].close()
        blocknum=blocknum+1
    ec1.close()
    ec2.close()
    ec3.close()
    ec4.close()
