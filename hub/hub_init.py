"""
    Run this program on your "hub" device, this is where devices will 
    be managed and monitored. This init file will install and configure
    the hub. The main application will run as the actual management terminal.
"""
import os

with open("devices/test.txt", "w") as file:
    