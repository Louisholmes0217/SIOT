import os
# This program initializes the files needed for a SIOT node.
def make_dirs():
    try:
#        os.mkdir("/opt/SIOT")
        os.mkdir("/opt/SIOT/node")
    except PermissionError:
        print("Insufficient permissions, cannot create directories \n'run me as root'")
    except FileExistsError:
        print("Files already exist")

def init_files():
    with open("/opt/SIOT/node/node.csv", "w") as f:
        f.write("tag,command,description\n")

init_files()
