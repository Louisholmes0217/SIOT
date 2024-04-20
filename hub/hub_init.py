"""
    Run this program on your "hub" device, this is where devices will 
    be managed and monitored. This init file will install and configure
    the hub. The main application will run as the actual management terminal.
"""
import os

# Creating directories
def makedirs():
    try:
        os.mkdir("/opt/SIOT")
        os.mkdir("/opt/SIOT/hub")
    except PermissionError:
        print("Insufficient permissions, cannot create directories \n'run me as root'")
    except FileExistsError:
        print("Files already exist")

def settings_config():
    while True:
        print("Please enter the local IP: for the server")
        ip = input()
        if len(ip.split(".")) == 4:
            for segment in ip:
                if segment.isnumeric():
                    continue
                else:
                    print("Invalid IP format, try again.")
                    break
        else:
            print("Invalid IP format, try again.")
        
            
settings_config()

#def set_network_settings():
#    with open("/opt/SIOT/settings.json", "w"):
        