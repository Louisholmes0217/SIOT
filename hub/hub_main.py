import csv
import socket
import pickle

def main():
    print("Hellooo")   
    print("Initializing HUB...")
    print("Welcome to SIOT, please select an option:")
    while True:
        print("[1] add node:\n[2] delete nodes\n[3] view nodes\n[4] interact with node, (run call, add calls etc.)\n[5] Exit")
        choice = input(":    ")
        match choice:
            case "1":
                print("Please enter the IP address of the node you wish to add")
                ip = input(":    ")
                print("Please enter the name for your node")
                name = input(":    ")
                print("Please enter a brief description for your node")
                desc = input(":    ")
                add_node(ip, name, desc)

            case "2":
                print("Deleting all nodes.")
                delete_nodes()

            case "3":
                nodes = get_nodes()
                for node in nodes:
                    print(f"{node[0]:10}{node[1]:10}{node[2]:10}{node[3]}", end="")
            case "4":
                while True:
                    nodes = get_nodes()
                    for node in nodes:
                        print(f"{node[0]:10}{node[1]:10}{node[2]:10}{node[3]}", end="")
                    print("Please select the ID of the node you wish to interact with")
                    node_choice = input(":    ")
                    for node in nodes:
                        if node_choice == node[0]:
                            node_socket = (node[1], 5555)
                            break
                    print(f"Node: {choice} has been selected, please select one of the following actions")
                    break
                while True:
                    print("Please select one of the following options:")
                    print(f"[1] Show calls\n[2] Delete calls\n[3] Delete call\n[4] Add call\n[5] Run call\n[6] Exit")
                    choice = input(":    ")
                    match choice:
                        case "1":
                            print("Showing all calls available on the node:")
                            try:
                                calls = get_calls(node_socket)
                            except ConnectionRefusedError:
                                print("Node not available")
                                break
                            for call in calls:
                                print(f"{call[0]:10}{call[1]:10}{call[2]}", end="")
                        case "2":
                            print("Deleting all calls in node:")
                            try:
                                delete_calls(node_socket)
                            except ConnectionRefusedError:
                                print("Node not available")
                                break
                        case "3":
                            print("Please enter the tag of the call you wish to delete:")
                            try:
                                calls = get_calls(node_socket)
                            except ConnectionRefusedError:
                                print("Node not available")
                                break
                            for call in calls:
                                print(f"{call[0]:10}{call[1]:10}{call[2]:10}", end="")
                            deleted_tag = input(":    ")
                            delete_call(node_socket, deleted_tag)
                            print(f"Call deleted\n")
                        case "4":
                            print(f"Please enter the command for the call you wish to add,\n(HINT: pass the path to an executable file you wish to run on the target such as '/opt/flash_led.sh')")
                            command = input(":    ")
                            print(f"Please enter the description for the call")
                            desc = input(":    ")
                            try:   
                                add_call(node_socket, command, desc)
                            except ConnectionRefusedError:
                                print("Node not available")
                                break
                            print("Call added")
                        case "5":
                            print("Please enter the tag for the call you wish to run:")
                            print("Showing all calls available on the node:")
                            try:
                                calls = get_calls(node_socket)
                            except ConnectionRefusedError:
                                print("Node not available")
                                break
                            for call in calls:
                                print(f"{call[0]:10}{call[1]:10}{call[2]}", end="")
                            tag = input(":    ")
                            run_call(node_socket, tag)
                        case "6":
                            break
            case "5":
                print("Exiting program...")
                exit()
                 
def get_nodes():
    print("Loading in known nodes...")
    with open("/opt/SIOT/hub/nodes.csv", "r") as f:
        lines = f.readlines()
        new_lines = []
        for line in lines:
            new_line = []
            line = line.split(",")
            new_line.append(line[0])
            new_line.append(line[1])
            new_line.append(line[2])
            line.pop(0)
            line.pop(0)
            line.pop(0)
            line = ",".join(line)
            new_line.append(line)
            new_lines.append(new_line)
        return new_lines

def add_node(ip, name, desc):
    id = "0"
    with open("/opt/SIOT/hub/nodes.csv", "r") as f:
        for line in f.readlines():
            if line != "":
                id = line.split(",")[0]
                if id == "id":
                    id = 0
                    print(f"ID = {id}")
            else:
                try:
                    id = int(id)
                    print(f"ID = {id}")
                except ValueError:
                    print("Invalid ID, not a number, try again")
    with open("/opt/SIOT/hub/nodes.csv", "a") as f:
        print(f"ID = {id}, and the type is {type(id)}")
        id = int(id)
        id += 1
        id = str(id)
        f.write(f"{id},{ip},{name},{desc}\n")

def delete_nodes():
    with open("/opt/SIOT/hub/nodes.csv", "w") as f:
        f.write(f"id,ip,name,desc\n")

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

main()