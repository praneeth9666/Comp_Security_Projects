#!/usr/bin/python3

# import dependancies 
import  sys, urllib, urllib.parse
from pymd5 import md5, padding

url = sys.argv[1]

# find the base of url, token and message
base = url[:url.find("=")+1] # everything up to and including =
token1 = url[url.find("=")+1:url.find("&")] # extract the token from between the = and & characters 
msg = url[url.find("&")+1:]

#print(f"base: {base}")
#print(f"token: {token1}")
#print(f"message: {msg}")

# find the padding
numbits = ((len(msg)+8) + len(padding((len(msg)+8) *8)))*8

# create the new hash
h = md5(state=bytes.fromhex(token1), count=numbits)

# define the new command and update the hash
newcmd = "&command=UnlockSafes"
h.update(newcmd)

# find the new token and build new url
token2 = h.hexdigest()
#print(f"New token: {new_token}")
new_url = base + token2 + "&" + msg + urllib.parse.quote(padding((len(msg)+8)*8)) + newcmd

# output the modified URL now including the length extension attack
print(new_url)
