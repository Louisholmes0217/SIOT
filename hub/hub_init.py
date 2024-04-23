"""
    Run this program on your "hub" device, this is where devices will 
    be managed and monitored. This init file will install and configure
    the hub. The main application will run as the actual management terminal.
"""
import os
import subprocess
import socket
import csv      
import threading

# Creating directories
def make_dirs():
    try:
        os.mkdir("/opt/SIOT")
        os.mkdir("/opt/SIOT/hub")
    except PermissionError:
        print("Insufficient permissions, cannot create directories \n'run me as root'")
    except FileExistsError:
        print("Files already exist")

def settings_config():
    while True:
        # Config IP addresses with format validation
        print("Please enter the local IP for the server (default = 127.0.0.1): ", end="")
        ip = input()
        if ip == "":
            ip = "127.0.0.1"
            break
        else:
            if len(ip.split(".")) == 4:
                for segment in ip.split("."):
                    if segment.isnumeric():
                        continue
                    else:
                        print("Invalid IP format, try again.")
                        break
                break
            else:
                print("Invalid IP format, try again.")
    while True:
        print("Please enter the port to run the server on (default = 5671): ", end="")
        port = input()
        if port == "":
            port = 5671
            break
        elif port.isnumeric() and int(port) < 65555 and int(port) > 0:
            port = int(port)
            break
        
    # Checking if IP exists on local FS
    ip_config = str(subprocess.check_output("ip a", shell=True))
    if ip in ip_config:
        with open("/opt/SIOT/hub/hub_settings.csv", "w") as f:
            f.write(f"ip,port\n{ip},{port}\n")
    
    # Creating nodes list
    with open("/opt/SIOT/hub/nodes.csv", "w") as f:
        f.write("id,ip,name,desc\n")

def test_startup():
    with open("/opt/SIOT/hub/hub_settings.csv", "r") as f:
        # Reading 
        reader = csv.reader(f)
        reader.__next__()

make_dirs()
settings_config()