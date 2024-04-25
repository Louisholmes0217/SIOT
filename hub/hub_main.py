import csv
import socket
import pickle

def main():
    print("Hellooo")   
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

def connect_to_node(node_socket):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(node_socket)
    msg = [1, "1"]
    s_msg = pickle.dumps(msg)
    msg_len = len(s_msg).to_bytes(4, byteorder="big")
    s.sendall(msg_len)
    s.sendall(s_msg)
    s.close()


show_nodes()
connect_to_node(("127.0.0.1", 5555))