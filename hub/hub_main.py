import csv
import socket
import pickle

def main():
    print("Hellooo")   
    print("Initializing HUB...")

def show_nodes():
    print("Loading in known nodes...")
    with open("/opt/SIOT/hub/nodes.csv") as f:
        for line in f:
            print(line)

def add_node(ip, name, desc):
    with open("/opt/SIOT/nodes.csv", "a") as f:
        for line in f.readlines():
            if line != "":
                tag = int(line.split[0])
            else:
                f.write(f"{str(tag+1)},{ip},{name},{desc}")

def delete_calls(node_socket):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(node_socket)
    msg = [3]
    s_msg = pickle.dumps(msg)
    msg_len = len(s_msg).to_bytes(4, byteorder="big")
    s.sendall(msg_len)
    s.sendall(s_msg)
    s.close()

def add_call(node_socket, command, desc):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(node_socket)
    msg = [2, command, desc]
    s_msg = pickle.dumps(msg)
    msg_len = len(s_msg).to_bytes(4, byteorder="big")
    s.sendall(msg_len)
    s.sendall(s_msg)
    s.close()

def delete_call(node_socket, tag):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(node_socket)
    msg = [5,tag]
    s_msg = pickle.dumps(msg)
    msg_len = len(s_msg).to_bytes(4, byteorder="big")
    s.sendall(msg_len)
    s.sendall(s_msg)
    s.close()


def run_call(node_socket, tag):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(node_socket)
    msg = [1, tag]
    s_msg = pickle.dumps(msg)
    msg_len = len(s_msg).to_bytes(4, byteorder="big")
    s.sendall(msg_len)
    s.sendall(s_msg)
    s.close()

def get_calls(node_socket):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(node_socket)
    msg = [4]
    s_msg = pickle.dumps(msg)
    msg_len = len(s_msg).to_bytes(4, byteorder="big")
    s.sendall(msg_len)
    s.sendall(s_msg)
    response_len = int.from_bytes(s.recv(4), byteorder="big")
    calls = s.recv(response_len)
    calls = pickle.loads(calls)
    s.close()
    return calls





show_nodes()
delete_calls(("127.0.0.1", 5555))
add_call(("127.0.0.1", 5555), "ls -la", "Lists directories")
run_call(("127.0.0.1", 5555), "1")
add_call(("127.0.0.1", 5555), "touch NEWFILE.txt", "Creates a NEWFILE.txt file")
delete_call(("127.0.0.1", 5555), "2")
calls = get_calls(("127.0.0.1", 5555))
print(calls)