from scapy.all import *

sport = 10000
dport = 80
pkt = IP(src="10.25.4.69", dst="23.211.217.109")

SYN = pkt/TCP(sport=sport, dport=dport, flags="S")
SYNACK = sr1(SYN)
ACK = pkt/TCP(sport=sport, dport=dport, flags="A", seq=SYNACK.ack, ack=SYNACK.seq + 1)
send(ACK)

# ...

FIN = pkt/TCP(sport=sport, dport=dport, flags="FA", seq=SYNACK.ack, ack=SYNACK.seq + 1)
FINACK = sr1(FIN)
LASTACK = pkt/TCP(sport=sport, dport=dport, flags="A", seq=FINACK.ack, ack=FINACK.seq + 1)
send(LASTACK)

# save the packets in a pcap file
packets = [ FIN, FINACK, LASTACK]
wrpcap('TCP_handshake_close_2001CS75.pcap', packets)
