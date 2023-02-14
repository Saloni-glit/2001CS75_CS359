from scapy.all import *

# Create DNS request packet
dns_request = DNS(rd=1, qd=DNSQR(qname="www.goibibo.com"))

# Create IP and UDP packets for DNS request
ip = IP(dst="128.232.132.8")
udp = UDP(dport=53)

# Combine packets to form DNS request message
dns_request_msg = ip/udp/dns_request

# Send DNS request and capture response
dns_response = sr1(dns_request_msg)

# Create a list of packets to write to the pcap file
packets = [dns_request_msg, dns_response]

# Write packets to pcap file
wrpcap("dns_request_response.pcap", packets)

# Print the DNS response
print(dns_response[DNS].summary())
