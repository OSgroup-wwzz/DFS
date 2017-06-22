from handler import utils

filename = input()
utils.split(filename)
#Handler.merge(filename+".bk", Handler.filename_gen(filename))
utils.upload(filename)
