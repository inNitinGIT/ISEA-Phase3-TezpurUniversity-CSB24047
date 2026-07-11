import socket
import threading

SERVER_IP = "10.0.0.1"
PORT = 5000


def receive_messages(sock):
    while True:
        try:
            data = sock.recv(4096)

            if not data:
                print("\nDisconnected from server.")
                break

            print("\n" + data.decode('utf-8'))
        except:
            print("\nConnection closed.")
            break


def main():

    username = input("Enter username: ")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect((SERVER_IP, PORT))
    except Exception as e:
        print(f"Unable to connect: {e}")
        return

    sock.sendall(username.encode('utf-8'))

    receiver = threading.Thread(
        target=receive_messages,
        args=(sock,),
        daemon=True
    )
    receiver.start()

    print("\n========== CHAT COMMANDS ==========")
    print("Normal Message : Hello everyone")
    print("Private Message: /msg <username> <message>")
    print("Online Users   : /list")
    print("Exit           : exit")
    print("===================================\n")

    while True:

        try:
            message = input()

            if message.lower() == "exit":
                break

            if message.strip() == "":
                continue

            sock.sendall(message.encode('utf-8'))

        except KeyboardInterrupt:
            break
        except:
            break

    sock.close()


if __name__ == "__main__":
    main()