import socket

HOST = socket.gethostbyname(socket.gethostname())  # Standard loopback interface address (localhost)
PORT = 23423  # Port to listen on (non-privileged ports are > 1023)


def printTofile(data):
    with open("output.txt", "a+") as f:
        f.write(data + "\n")

def check_for_drops(seq_list):
    """Check for dropped packets since the last checked sequence number."""
    dropped_packets = 0
    seq_list.sort()
    for i in range(1, len(seq_list)):
        if seq_list[i] - seq_list[i - 1] > 1:
            dropped_packets += seq_list[i] - seq_list[i - 1] - 1
            print(i, seq_list[i], seq_list[i - 1])
            printTofile(f"Packet dropped between {seq_list[i - 1]} and {seq_list[i]}")
    return dropped_packets

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))

    print(f"UDP server listening on {HOST}:{PORT}")

    
    cnt = 0
    seq_list = []
    try:
        while True:
            data, addr = sock.recvfrom(1024)
            seq = int(data.decode('utf-8').split(":")[0])
            seq_list.append(seq)
            cnt += 1

            if cnt % 1000 == 0:
                dropped_packets = check_for_drops(seq_list)
                print(f"Received {cnt} packets. Dropped packets: {dropped_packets}")
                printTofile(f"Received {cnt} packets. Dropped packets: {dropped_packets}")
                seq_list = []
                cnt = 0
        
            

            
    except KeyboardInterrupt:
        # Final check for any remaining drops
        dropped_packets = check_for_drops(seq_list)
        print(f"Stopped by user. Total dropped packets: {dropped_packets}")

    finally:
        sock.close()

if __name__ == "__main__":
    main()


