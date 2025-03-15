#!/usr/bin/python3
# coding: latin-1
blob = """

AAAAAAAAAAAAAAAM#ç
ÐÕ]â•m&P`8]°4}ü*b8Ë¦‘þäËÂ÷R–Þ	onÔ|¡µ1\f±Òkø\¹.ê•,ôÑèòõ pÙO§qúõºçW«‰ðÇ/Ž'üNvï£ßO`/Áp ¸„kr—µk¹+M	œ´=8Á@²öEõdª"""
from hashlib import sha256
if 'E' not in blob :  # Even length for one file
    print("Use SHA-256 instead!")
else:  # Odd length for the other file
    print("MD5 is perfectly secure!")

