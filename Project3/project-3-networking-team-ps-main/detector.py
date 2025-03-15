from scapy.all import *
import sys

# Complete this function!
def process_pcap(pcap_fname):
    # used to count SYN and SYN ACK's
    syn_counts = {}
    syn_ack_counts = {}

    # loop through packets, filtering IP and TCP layers
    for pkt in PcapReader(pcap_fname):
        # Your code here
        if not pkt.haslayer(IP) or not pkt.haslayer(TCP):
            continue
        # extract tcp and ip layer from each packet
        pkt_ip_layer = pkt[IP]
        pkt_tcp_layer = pkt[TCP]

        # keep track of SYN and SYN ACK's
        if pkt_tcp_layer.flags == 'S': 
            # count the number of SYN
            ip_src = pkt_ip_layer.src
            syn_counts[ip_src] = syn_counts.get(ip_src, 0) + 1
        elif pkt_tcp_layer.flags == 'SA':
            # count the number of SYN ACK
            ip_dst = pkt_ip_layer.dst
            syn_ack_counts[ip_dst] = syn_ack_counts.get(ip_dst, 0) + 1
    
    # identify Ip addresses with 3 times as many SYN as SYN_ACK (suspicious IP's)
    for ip in syn_counts:
        s_count = syn_counts.get(ip, 0)
        sa_count = syn_ack_counts.get(ip, 0)

        if s_count > sa_count * 3:
            print(ip)


        

if __name__=='__main__':
    if len(sys.argv) != 2:
        print('Use: python3 detector.py file.pcap')
        sys.exit(-1)
    process_pcap(sys.argv[1])