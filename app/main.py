import socket

def main():
    print("Hello World!")
    print("Hostname: " + socket.gethostname())
    print("IP Address: " + socket.gethostbyname(socket.gethostname()))

if __name__ == "__main__":
    main()
