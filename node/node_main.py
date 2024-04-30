# Main program that runs on startup of a node
import socket
import subprocess
import csv
import pickle
HEADER_LENGTH = 10
def main():
    start_server()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
def start_server():
    s.bind(("127.0.0.1", 5555))
    s.listen(5)
    while True:
        conn, ip = s.accept()
        print(f"[CONNECTION ESTABLISHED] with host: {ip}")
        msg_len = conn.recv(4)
        if len(msg_len) <= 0:
            continue
        msg_len = int.from_bytes(msg_len, byteorder="big")
        msg = conn.recv(msg_len)
        full_msg = pickle.loads(msg)
        match full_msg[0]:
            case 1:
                run_call(full_msg[1])
            case 2:
                add_call(full_msg[1], full_msg[2])
            case 3:
                delete_calls()
            case 4:
                calls = get_calls()
                calls = pickle.dumps(calls)
                conn.sendall((len(calls)).to_bytes(4, byteorder="big"))
                conn.sendall(calls)
            case 5:
                delete_call(full_msg[1])

def add_call(command, description):
    with open("/opt/SIOT/node/node.csv", "r") as fr:
        tag = ""
        for line in fr.readlines():
            if line != "":
                tag = (line.split(","))[0]
        if tag == "tag":
            tag = "0"
    print("TAG = ", tag, "OF TYPE", type(tag))
    tag = int(tag)
    tag += 1
    tag = str(tag)
    with open("/opt/SIOT/node/node.csv", "a") as fw:
        fw.write(f"{tag},{command},{description}\n")

def get_calls():
    with open("/opt/SIOT/node/node.csv") as f:
        new_lines = []
        for line in f.readlines():
            new_line = []
            line = line.split(",")
            new_line.append(line[0])
            new_line.append(line[1])
            line.pop(0)
            line.pop(0)
            line = ",".join(line)
            new_line.append(line)
            new_lines.append(new_line)
    return new_lines

def delete_calls():
    with open("/opt/SIOT/node/node.csv", "w") as f:
        f.write("tag,command,description\n")

def delete_call(tag):
    with open("/opt/SIOT/node/node.csv", "r") as f:
        if not tag.isnumeric():
            return None
            raise Exception("Not a valid tag")
        new_lines = []
        for line in f.readlines():
            if line.split(",")[0] != tag:
                new_lines.append(line)
                print(f"Adding line {line}")
    with open("/opt/SIOT/node/node.csv", "w") as f:
        counter = 0
        for line in new_lines:
            f.write(str(counter)+",")
            l_line = line.split(",")
            if l_line[0] == "tag":
                line = ",".join(l_line)
                f.write(line)
                continue
            l_line.pop(0)
            line = ",".join(l_line)
            f.write(line)
            counter += 1
            

def run_call(tag):
    with open("/opt/SIOT/node/node.csv", "r") as f:
        reader = csv.DictReader(f)
        for line in reader:
            if line["tag"] == tag:
                subprocess.call(line["command"], shell=True)

start_server()
