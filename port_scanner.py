import socket
import argparse

def scan_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((ip, port))
        if result == 0:
            try:
                service = socket.getservbyport(port)
            except:
                service = "Unknown"
            print(f"[+] Port {port} is OPEN ({service})")
        sock.close()
    except Exception as e:
        pass

def main():
    parser = argparse.ArgumentParser(description="Simple Port Scanner")
    parser.add_argument("--ip", required=True, help="Target IP address")
    parser.add_argument("--start-port", type=int, default=1, help="Start of port range")
    parser.add_argument("--end-port", type=int, default=1024, help="End of port range")
    args = parser.parse_args()

    print(f"Scanning {args.ip} from port {args.start_port} to {args.end_port}...")
    for port in range(args.start_port, args.end_port + 1):
        scan_port(args.ip, port)

if __name__ == "__main__":
    main()
