from handler import Handler

filename = input()
Handler.split(filename)
Handler.merge(filename+".bk", Handler.filename_gen(filename))

