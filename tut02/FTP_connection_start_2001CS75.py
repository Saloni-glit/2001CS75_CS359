from scapy.all import *

# Set the target FTP server IP address and port
server_ip = "23.211.217.109"
server_port = 21

# Create a SYN packet for the FTP connection
syn_packet = IP(dst=server_ip)/TCP(dport=server_port, flags="S")

# Send the SYN packet and receive the SYN-ACK response
syn_ack_packet = sr1(syn_packet, timeout=2)

# Create an ACK packet to complete the TCP three-way handshake
ack_packet = IP(dst=server_ip)/TCP(dport=server_port, flags="A", ack=syn_ack_packet.seq + 1, seq=syn_packet[TCP].ack + 1)

# Send the ACK packet to establish the TCP connection
send(ack_packet)

# Create an empty list to store the packets
packets = []

# Add the SYN and SYN-ACK packets to the list
packets.append(syn_packet)
packets.append(syn_ack_packet)

# Add the ACK packet to the list
packets.append(ack_packet)

# Create a socket to capture the incoming and outgoing packets
sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))

# Set a filter to capture only packets to and from the target server IP address
filter_str = "host " + server_ip
sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1024 * 1024)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_FILTER, str.encode(filter_str))

# Loop to capture and append the packets to the list
while True:
    packet = sock.recv(1024)
    packets.append(packet)
    wrpcap("FTP_connection_start_2001CS75.pcap", packets)

    # Send the packet to the target server
    send(packet)

    # Check if the packet is an FTP response to the last command sent
    # and print it if it is.
    # Note that you'll need to follow the FTP protocol to send valid commands
    # and interpret the responses correctly.
    if FTPResponse in packet:
        print(str(packet[FTPResponse].payload))
    
# Print a confirmation message after the loop ends
print("Packets saved to ftp_packets.pcap")
