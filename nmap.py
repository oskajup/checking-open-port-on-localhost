import socket
import errno
import sys
import requests # if you want to integrate discord to send you a message if any port from list is open
from datetime import datetime

TIMEOUT = 2
PORTS_TO_WATCH = [21, 22, 23, 80, 443, 8080, 3389] 
WEBHOOK_URL = "https://discord.com/api/webhooks/Your_Webhoock" # paste your discord WEBHOOK 

def scan_port(target, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(TIMEOUT)
    try:
        result = s.connect_ex((target, port))
        return "OPEN" if result == 0 else "CLOSED"
    except Exception:
        return "ERROR"
    finally:
        s.close()

def send_alert(target, open_ports):
    if not WEBHOOK_URL or "Your_WEBHOOK" in WEBHOOK_URL: # paste your discord WEBHOOK 
        return
    
    payload = {
        "content":
                   f"Open ports detected on host **{target}** \n"
                   f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                   f"Open ports: `{open_ports}`"
    }
    try:
        requests.post(WEBHOOK_URL, json=payload, timeout=5)
    except Exception as e:
        print(f"[-] Failed to send alert: {e}")

def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    open_detected = []

    for port in PORTS_TO_WATCH:
        state = scan_port(target, port)
        if state == "OPEN":
            open_detected.append(port)

    if open_detected:
        print(f"[!] Open ports detected: {open_detected}! sending an alert...")
        send_alert(target, open_detected)
    else:
        print("[+] All monitored ports are secure (closed).")

if __name__ == "__main__":
    main()
