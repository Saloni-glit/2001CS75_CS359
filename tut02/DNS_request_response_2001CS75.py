from scapy.all import *

# Create DNS request packet
dns_request = DNS(rd=1, qd=DNSQR(qname="www.mail.ru"))

# Create IP and UDP packets for DNS request
ip = IP(dst="172.16.1.3")
udp = UDP(dport=53)

# Combine packets to form DNS request message
dns_request_msg = ip/udp/dns_request

# Send DNS request and capture response
dns_response = sr1(dns_request_msg)

# Create a list of packets to write to the pcap file
packets = [dns_request_msg, dns_response]

# Write packets to pcap file
wrpcap("DNS_request_response_2001CS75.pcap", packets)

# Print the DNS response
print(dns_response[DNS].summary())