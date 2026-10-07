# 🔍 Advanced Port Scanner
# 📖 Overview
The Advanced Port Scanner is a Python-based security auditing tool that scans a target IP or domain for open ports, identifies services, grabs banners, and visualizes results in real time. It supports both connect scans and stealth SYN scans, and now includes critical port alerts, protocol filtering, and service fingerprinting for deeper analysis.

# ✨ Features
- Multithreaded Scanning: Fast scanning across large port ranges.
- Dual Scan Modes:
      -Connect Scan (full TCP handshake).
      -Stealth SYN Scan (half-open, harder to detect).
- Service Detection: Identifies common services (HTTP, FTP, SSH, etc.).
- Banner Grabbing & Fingerprinting: Reads service banners to fingerprint applications.
- Critical Port Alerts: Flags sensitive ports like SSH (22), RDP (3389), SMB (445), SQL (1433), MySQL (3306).
- Advanced Protocol Filtering: Focus scans on specific protocols (HTTP, DNS, ICMP).
- Logging: Export results to CSV or JSON.
- Flask Dashboard: Real-time web interface with tables and charts (Chart.js).

# 🛠️ Tech Stack
- Language: Python 3
- Libraries: socket, argparse, csv, json, flask, scapy, concurrent.futures

# ⚙️ Installation
- Clone the repository and navigate into the project folder:
bash:
# git clone https://github.com/your-username/advanced-port-scanner.git
cd advanced-port-scanner

-Install dependencies:
bash:
# pip install scapy flask

# 🚀 Usage
- Basic connect scan
bash:
# python advanced_port_scanner.py --ip example.com

- Stealth SYN scan
 bash:
# sudo python advanced_port_scanner.py --ip example.com --mode stealth

- Save results to JSON
bash:
# python advanced_port_scanner.py --ip example.com --output json

- Enable dashboard visualization
bash:
# python advanced_port_scanner.py --ip example.com --dashboard

- Open your browser at:
Code:
# http://localhost:5000

# 📂 Project Structure
- Code
advanced-port-scanner/

│── advanced_port_scanner.py   # Main script

│── README.md                  # Documentation

│── scan_results.csv           # Example CSV output

│── scan_results.json          # Example JSON output

# 🔮 Future Enhancements
- Integrate with SQLite for persistent storage.
- Advanced filtering for application-layer protocols (HTTP headers, DNS queries).
- More detailed service fingerprinting using known banner signatures.
- Dashboard upgrades with traffic graphs and pie charts.

# ⚠️ Disclaimer
This tool is for educational and security research purposes only.
Do not use it against systems or networks without explicit permission. Unauthorized scanning may be illegal.
