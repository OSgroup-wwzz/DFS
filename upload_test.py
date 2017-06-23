import handler
import sync

for file in handler.read_file_list():
    handler.upload(file)

