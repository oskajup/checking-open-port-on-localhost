#!/bin/bash
set -e

SCRIPT_SRC="./nmap.py"
SCRIPT_DEST="/usr/local/bin/port_scanner.py"
CRON_CONF="/etc/cron.d/port_scanner"

if [ "$EUID" -ne 0 ]; then
  echo "[-] Please run this script as root (sudo)!"
  exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo "[+] Python 3 is not installed. Installing Python 3 and dependencies..."
    apt update && apt install -y python3 python3-requests
fi

echo "[+] Copying script to $SCRIPT_DEST..."
cp "$SCRIPT_SRC" "$SCRIPT_DEST"
chown root:root "$SCRIPT_DEST"
chmod 700 "$SCRIPT_DEST"

echo "[+] Configuring Cron job..."
echo "0 * * * * root python3 $SCRIPT_DEST 127.0.0.1 > /dev/null 2>&1" > "$CRON_CONF"
chmod 644 "$CRON_CONF"

echo "[+] Done! The script will scan ports every hour in the background."