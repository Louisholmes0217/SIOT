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
        msg_len = int.from_bytes(msg_len)
        msg = conn.recv(msg_len)
        full_msg = pickle.loads(msg)
        match full_msg[0]:
            case 1:
                run_call(full_msg[1])
            case 2:
                add_call(full_msg[1], full_msg[2])
            case 3:
                delete_calls()
        
    """
            header = (header.decode("utf-8")).strip()
            match header:
                # 1 is add_call()
                case "1":
                    cmd_len = s.recv(HEADER_LENGTH)
                    command = s.recv(cmd_len)
                    desc_len = s.recv(HEADER_LENGTH)
                    description = s.recv(desc_len)
                    add_call(command, description)

                # 2 is delete_calls()
                case "2":
                    delete_calls()
                
                # 3 is get_calls()
                case "3":
                    calls = get_calls()
                    call_string = ("")
                    for call in calls:
                        call_string += str(call)
                    calls_len = len(calls.encode("utf-8"))
                    conn.send(f"{calls_len:<10}")
                    conn.send(calls.encode("utf-8"))
    """

def add_call(command, description):
    with open("/opt/SIOT/node/node.csv", "r") as fr:
        tag = ""
        for line in fr.readlines():
            if line != "":
                tag = (line.split(","))[0]
        if tag == "tag":
            tag = 0
    with open("/opt/SIOT/node/node.csv", "a") as fw:
        fw.write(f"{int(tag)+1},{command},{description}\n")

def get_calls():
    lines = []
    with open("/opt/SIOT/node/node.csv") as f:
        for line in f.readlines():
            lines.append(line)
    return lines

def delete_calls():
    with open("/opt/SIOT/node/node.csv", "w") as f:
        f.write("tag,command,description\n")

def run_call(tag):
    with open("/opt/SIOT/node/node.csv", "r") as f:
        reader = csv.DictReader(f)
        for line in reader:
            if line["tag"] == tag:
                subprocess.call(line["command"], shell=True)

start_server()
