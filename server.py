import socket
import threading
from collections import defaultdict

SIZE = 1024
FORMAT = "utf-8"
clients = []
client_usernames = []
rooms = defaultdict(list)


def get_index_client(clients, cur_conn):
    i = 0
    for conn in clients:
        if conn == cur_conn:
            break
        i += 1
    return i

def new_client(conn, addr):
    username = conn.recv(4096).decode('utf-8')
    room_id = conn.recv(4096).decode('utf-8')

    if room_id not in rooms:
        conn.send("New Group is Created".encode('utf-8'))
    else:
        conn.send("Welcome to Chat Room".encode('utf-8'))
    rooms[room_id].append(conn)
    for i in rooms:
        print(i)

    msg = "Welcome " + username + ". Use 'exit' to quit"
    conn.send(msg.encode('utf-8'))
    client_usernames.append(username)
    
    while True:
        msg = conn.recv(4096).decode('utf-8')
        print(msg)
        if not msg or msg == "exit": 
            break
        idx = get_index_client(clients, conn)
        sender_username = client_usernames[idx]
        broadcast_msg(msg, conn, room_id)

    idx = get_index_client(clients, conn)
    del clients[idx]
    del client_usernames[idx]
    conn.close()

def broadcast_msg(msg, conn, room_id):
    for c in rooms[room_id]:
            if c != conn:
                c.send(msg.encode('utf-8'))


def main():
    s = socket.socket()
    print('Socket Created')
    s.bind(('localhost', 12345))
    s.listen(3)
    print('waiting for connections')

    while True:
        c, addr = s.accept()
        clients.append(c)
        #print(len(clients))
        thread = threading.Thread(target = new_client, args = (c, addr))
        thread.start()


if __name__ == "__main__":
    main()