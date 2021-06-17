import threading
import socket

def recieve_msg_server(conn):
    while True:
        try:
            msg = conn.recv(4096)
            if not msg:
                break
            print(msg)
        except:
            print("Error")
            break
    conn.close()

def send_message(conn, user_name):
    while True:
        msg = f'{user_name}: {input("")}'
        conn.send(msg.encode('utf-8'))

def main():
    c = socket.socket()
    c.connect(('localhost', 12345))
    user_name = input("Enter UserName")
    c.send(user_name.encode('utf-8'))
    room_id = input("Enter Room ID")
    c.send(room_id.encode('utf-8'))
    receive_thread = threading.Thread(target = recieve_msg_server, args = (c, ))
    receive_thread.start()

    send_thread = threading.Thread(target = send_message, args=(c, user_name))
    send_thread.start()

if __name__ == "__main__":
    main()