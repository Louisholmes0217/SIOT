import csv
import socket

def main():
    print("Initializing HUB...")

def show_nodes():
    nodes = []
    print("Loading in known nodes.")
    with open("/opt/SIOT/hub/nodes.csv") as f:
        reader = csv.DictReader(f)
        for line in reader:
            print(line)
show_nodes()
