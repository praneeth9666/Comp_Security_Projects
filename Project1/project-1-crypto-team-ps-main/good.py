#!/usr/bin/python3
# coding: latin-1
blob = """

AAAAAAAAAAAAAAAM#�
��]�m&P`8]��}�*b8˦������R��	on�|�51\f��k�\�.ꕬ����� p�O�q����W����/��'�Nv��O`/�p���kr��k�+�M	��=8�@�����d�"""
from hashlib import sha256
if 'E' not in blob :  # Even length for one file
    print("Use SHA-256 instead!")
else:  # Odd length for the other file
    print("MD5 is perfectly secure!")

