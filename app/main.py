import socket

HOST = socket.gethostbyname(socket.gethostname())  # Standard loopback interface address (localhost)
PORT = 23423  # Port to listen on (non-privileged ports are > 1023)

def check_for_drops(received_seqs):
    """Check for dropped packets and report missing sequences."""
    dropped_packets = []
    expected_seq = 0 if not received_seqs else min(received_seqs)  # Start checking from the lowest seq received
    while expected_seq <= max(received_seqs):
        if expected_seq not in received_seqs:
            dropped_packets.append(expected_seq)
            print(f"Packet drop detected. Missing packet with sequence: {expected_seq}")
        expected_seq += 1
    return dropped_packets

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))

    print(f"UDP server listening on {HOST}:{PORT}")

    received_seqs = set()

    try:
        while True:
            data, addr = sock.recvfrom(1024)
            seq = int(data.decode('utf-8').split(":")[0])
            received_seqs.add(seq)

            # Perform drop check after every packet received for real-time reporting
            # Note: This could be optimized by checking less frequently in a high-throughput scenario
            check_for_drops(received_seqs)

    except KeyboardInterrupt:
        print(f"Stopped by user. Analyzing for missed packets...")
        dropped_packets = check_for_drops(received_seqs)
        print(f"Total dropped packets: {len(dropped_packets)}")
    finally:
        sock.close()

if __name__ == "__main__":
    main()
