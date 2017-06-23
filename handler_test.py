from handler import *

gen_file_list()

list1 = read_file_list()

for f in list1:
    gen_block_list(f)

for f in list1:
    print(read_block_list(f))
