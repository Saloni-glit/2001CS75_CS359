from scapy.all import *

# Set the destination IP and port
dst_ip = "128.232.132.8"
dst_port = 80

# Construct the SYN packet
syn_packet = IP(dst=dst_ip)/TCP(dport=dst_port, flags="S")

# Send the SYN packet and capture the response
syn_response = sr1(syn_packet)

# Extract the sequence number and acknowledgment number from the SYN-ACK response
seq_num = syn_response[TCP].ack
ack_num = syn_response[TCP].seq + 1

# Construct the ACK packet to complete the 3-way handshake
ack_packet = IP(dst=dst_ip)/TCP(dport=dst_port, flags="A", seq=seq_num, ack=ack_num)

# Save the packets into a pcap file
wrpcap("tcp_handshake.pcap", [syn_packet, syn_response, ack_packet])

# Send the ACK packet to establish the connection
send(ack_packet)
