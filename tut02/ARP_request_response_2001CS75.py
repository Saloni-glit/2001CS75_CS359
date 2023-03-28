from scapy.all import *

# Set the target IP address to ping
target_ip = "10.25.4.69"

# Send an ARP request to get the MAC address of the target IP
arp_request = Ether(dst="8C-8D-28-97-53-56")/ARP(op=1, pdst=target_ip)
arp_response = srp1(arp_request, timeout=2, verbose=0)

# Use the MAC address in the ARP response to send a ping to the target IP
ping_request = IP(dst=target_ip)/ICMP()

ping_response = sr1(ping_request, timeout=2, verbose=0)


# Print the result of the ping
if ping_response:
    print("Ping successful")
else:
    print("Ping failed")

packets = [arp_request, arp_response, ping_request, ping_response]

# Write the packets to a .pcap file
wrpcap("ARP_request_response_2001CS75.pcap", packets)

print("Packets saved to ping_packets.pcap")
