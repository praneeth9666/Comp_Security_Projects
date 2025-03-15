#!/usr/bin/python3

import requests
import sys

MAC_msg = 'Decrypted message must contain a correct MAC'
Valid_msg = 'The ciphertext is valid'


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("usage: %s ORACLE_URL CIPHERTEXT_HEX" % (sys.argv[0]), file=sys.stderr)
        sys.exit(-1)
    oracle_url = sys.argv[1]
    cipher_text = sys.argv[2]
    
    plain_text_hex=bytearray()
    blocks=[]       
    for i in range(0,len(cipher_text),32):      #breaking the cipher into blocks to decrypt
        blocks.append(cipher_text[i:i+32])
    pad_len=0                                   #variable acts like a flag for padding length
    for i in range(1,len(blocks)):
        curr_block = bytearray.fromhex(blocks[-i])              #choosing blocks to decrypt
        prev_block = bytearray.fromhex(blocks[-(i+1)])
        decoded_bytes = bytearray()
        pre_attack_cipher = ''.join(blocks[0:-(i+1)])
        post_attack_cipher = blocks[-i]
        for padding_value in range(1,len(curr_block)+1):  
            xor_byte = prev_block[-padding_value]
            for i in range(256):
                prev_block[-1*padding_value] = i
                final_attack_cipher = prev_block.hex() + curr_block.hex()
                r = requests.get("%s?message=%s" % (oracle_url, final_attack_cipher))               #GET request to oracle
                r.raise_for_status()
                obj = r.json()
                if (obj['message'] == MAC_msg or (obj['message'] == Valid_msg and len(plain_text_hex)>1)):      #Verifying the message 
                    dcode_byte = padding_value ^ prev_block[-padding_value]                                
                    final_byte = dcode_byte ^ xor_byte                                                      
                    if pad_len == 0:
                        if final_byte == 1:
                            continue
                        else:
                            pad_len = final_byte
                    decoded_bytes.append(padding_value ^ prev_block[-padding_value])
                    plain_text_hex.append(decoded_bytes[padding_value-1] ^ xor_byte)
                    for i in range(padding_value):
                        prev_block[-(i+1)] = decoded_bytes[i] ^ (padding_value + 1)                 #adding padding
                    break
                if i==255:
                   sys.exit(-1)
    #print(plain_text_hex)
    message = bytes.fromhex(plain_text_hex[pad_len + 32:].hex())                    #decoding from hex by removing the padding
    print(message.decode('ascii')[::-1])