import csv
import socket

def main():
    print("Initializing HUB...")

def show_nodes():
    nodes = []
    print("Loading in known nodes...")
    with open("/opt/SIOT/hub/nodes.csv") as f:
        for line in f:
            print(line)

def add_node(id, ip, name):
    with open("/opt/SIOT/hub/nodes.csv", "r") as f:
        print(f.readlines())

show_nodes()
