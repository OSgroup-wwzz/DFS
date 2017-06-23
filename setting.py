import json

"""
with rclone set up
this program helps user to set up local and external drives
"""

def init():
    locs = {}
    locs["here"] = input("The name of your local drive:")
    server = []
    try:
        while True:
            server.append(input("Names of your cloud drives(EOF to stop):") + ":")
    except EOFError:
        pass
    locs["servers"] = server
    file = open("config/loc.json", "w")
    file.write(json.dumps(locs))

if __name__ == "__main__":
    init()
