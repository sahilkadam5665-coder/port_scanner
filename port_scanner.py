import socket
import argparse
import csv
import json
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, render_template_string
from scapy.all import IP, TCP, sr1

# Store results globally
scan_results = []

def connect_scan(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((ip, port))
        if result == 0:
            try:
                service = socket.getservbyport(port)
            except:
                service = "Unknown"
            # Banner grabbing
            banner = ""
            try:
                sock.send(b"Hello\r\n")
                banner = sock.recv(1024).decode().strip()
            except:
                banner = "N/A"
            print(f"[+] Port {port} is OPEN ({service}) | Banner: {banner}")
            scan_results.append({"port": port, "status": "OPEN", "service": service, "banner": banner})
        sock.close()
    except Exception:
        pass

def stealth_scan(ip, port):
    pkt = IP(dst=ip)/TCP(dport=port, flags="S")
    resp = sr1(pkt, timeout=1, verbose=0)
    if resp and resp.haslayer(TCP):
        if resp[TCP].flags == 0x12:  # SYN-ACK
            print(f"[+] Port {port} is OPEN (stealth)")
            scan_results.append({"port": port, "status": "OPEN", "service": "Unknown", "banner": "N/A"})
        elif resp[TCP].flags == 0x14:  # RST
            scan_results.append({"port": port, "status": "CLOSED", "service": "Unknown", "banner": "N/A"})

def save_results(fmt="csv", filename="scan_results"):
    if fmt == "csv":
        with open(f"{filename}.csv", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["port", "status", "service", "banner"])
            writer.writeheader()
            writer.writerows(scan_results)
    elif fmt == "json":
        with open(f"{filename}.json", "w") as f:
            json.dump(scan_results, f, indent=4)

# Flask dashboard
app = Flask(__name__)

@app.route("/")
def dashboard():
    html = """
    <h2>Port Scanner Dashboard</h2>
    <table border="1">
        <tr><th>Port</th><th>Status</th><th>Service</th><th>Banner</th></tr>
        {% for r in results %}
        <tr><td>{{r.port}}</td><td>{{r.status}}</td><td>{{r.service}}</td><td>{{r.banner}}</td></tr>
        {% endfor %}
    </table>
    <h3>Protocol Distribution</h3>
    <canvas id="chart" width="400" height="200"></canvas>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
    const ctx = document.getElementById('chart').getContext('2d');
    const data = {
        labels: {{ results|map(attribute='service')|list }},
        datasets: [{
            label: 'Open Ports by Service',
            data: {{ results|map(attribute='port')|list }},
            backgroundColor: 'rgba(54, 162, 235, 0.6)'
        }]
    };
    new Chart(ctx, { type: 'bar', data: data });
    </script>
    """
    return render_template_string(html, results=scan_results)

def main():
    parser = argparse.ArgumentParser(description="Advanced Port Scanner")
    parser.add_argument("--ip", required=True, help="Target IP or domain")
    parser.add_argument("--start-port", type=int, default=1, help="Start of port range")
    parser.add_argument("--end-port", type=int, default=1024, help="End of port range")
    parser.add_argument("--mode", choices=["connect", "stealth"], default="connect", help="Scan mode")
    parser.add_argument("--output", choices=["csv", "json"], help="Save results format")
    parser.add_argument("--dashboard", action="store_true", help="Enable Flask dashboard")
    args = parser.parse_args()

    print(f"Scanning {args.ip} from port {args.start_port} to {args.end_port} in {args.mode} mode...")

    # Multithreading
    with ThreadPoolExecutor(max_workers=100) as executor:
        for port in range(args.start_port, args.end_port + 1):
            if args.mode == "connect":
                executor.submit(connect_scan, args.ip, port)
            else:
                executor.submit(stealth_scan, args.ip, port)

    if args.output:
        save_results(args.output)

    if args.dashboard:
        app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    main()
