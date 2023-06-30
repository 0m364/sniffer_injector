#!/bin/bash

if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root"
    exit 1
fi

# Install scapy and tcpdump if not already installed
if ! dpkg -s python3-scapy >/dev/null 2>&1; then
    apt-get update -q
    apt-get -q install python3-scapy -y
fi

if ! dpkg -s tcpdump >/dev/null 2>&1; then
    apt-get update -q
    apt-get -q install tcpdump -y
fi

# Set interface name for packet capture/injection
INTERFACE="eth0"

# Function to capture packets
capture_packets() {
    echo "Starting packet capture..."
    trap 'echo "Packet capture stopped"; exit 1' INT
    tcpdump -i $INTERFACE -s0 -w capture.pcap
    echo "Packet capture completed. Saved as capture.pcap"
}

# Function to inject packets
inject_packets() {
    echo "Injecting packets..."
    # add packet injection commands here
    scapy
    echo "Packets injected successfully"
}

# Prompt user to select an option
echo -e "Select an option:"
echo -e "1. Capture packets"
echo -e "2. Inject packets"
read -p "Enter your choice (1 or 2): " CHOICE

# Perform action based on user choice
case $CHOICE in
    1)
        capture_packets
        ;;
    2)
        inject_packets
        ;;
    *)
        echo "Invalid choice"
        ;;
esac

