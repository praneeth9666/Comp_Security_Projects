#!/usr/bin/python3
# coding: latin-1
blob = """

AAAAAAAAAAAAAAAM#�
��]�m&P`8]�4}�*b8˦������R��	on�|��1\f��k�\�.�,����� p�O�q����W����/�'�Nv��O`/�p���kr��k�+M	��=8�@���E�d�"""
from hashlib import sha256
if 'E' not in blob :  # Even length for one file
    print("Use SHA-256 instead!")
else:  # Odd length for the other file
    print("MD5 is perfectly secure!")

