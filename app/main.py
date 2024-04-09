import socket

HOST = socket.gethostbyname(socket.gethostname())  # Standard loopback interface address (localhost)
PORT = 23423  # Port to listen on (non-privileged ports are > 1023)


def check_for_drops(received_seqs, last_checked, highest_seq):
    """Check for dropped packets since the last checked sequence number."""
    dropped_packets = 0
    for expected_seq in range(last_checked + 1, highest_seq + 1):
        if expected_seq not in received_seqs:
            dropped_packets += 1
            print(f"Packet drop detected. Missing packet with sequence: {expected_seq}")
    return dropped_packets

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))

    print(f"UDP server listening on {HOST}:{PORT}")

    received_seqs = set()
    last_checked_seq = 0
    highest_seq_received = 0
    dropped_packets = 0

    try:
        while True:
            data, addr = sock.recvfrom(1024)
            seq = int(data.decode('utf-8').split(":")[0])
            received_seqs.add(seq)

            # print(f"Received packet with sequence: {seq}")  

            if seq > highest_seq_received:
                highest_seq_received = seq

            # If we've received a new "batch" of packets, check for drops
            if len(received_seqs) % 100 == 0:  # Arbitrary check interval
                dropped_packets += check_for_drops(received_seqs, last_checked_seq, highest_seq_received)
                last_checked_seq = highest_seq_received

    except KeyboardInterrupt:
        # Final check for any remaining drops
        dropped_packets += check_for_drops(received_seqs, last_checked_seq, highest_seq_received)
        print(f"Stopped by user. Total dropped packets: {dropped_packets}")
    finally:
        sock.close()

if __name__ == "__main__":
    main()