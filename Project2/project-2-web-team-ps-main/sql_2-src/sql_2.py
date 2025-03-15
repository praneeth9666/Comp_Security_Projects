import hashlib
import itertools
import string


target_pattern = b"\x27\x3D\x27"  #pattern "'='"


def find_password():
    characters = string.printable  # Includes letters, digits, punctuation, and whitespace

    for length in range(1, 6):  # Try passwords of lengths 1 through 5 to simplify search
        for chars in itertools.product(characters, repeat=length):
            password = ''.join(chars)
            md5_hash = hashlib.md5(password.encode('utf-8')).digest()  # Get binary MD5 hash
            if target_pattern in md5_hash:
                return password, md5_hash
    return None, None

# Find a suitable password
password, md5_hash = find_password()
if not password:
    print("Cannot find Pass")
    exit()

print(f"Password found: {password}")
print(f"MD5 hash (binary): {md5_hash}")

