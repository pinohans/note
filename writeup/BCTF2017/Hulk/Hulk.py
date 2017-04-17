#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Unbuffered(object):
   def __init__(self, stream):
       self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
   def __getattr__(self, attr):
       return getattr(self.stream, attr)

import sys
sys.stdout = Unbuffered(sys.stdout)
import random
import binascii
import re
from mycryptolib import *

def hex2charlist(hexstr):
    charlist = []
    length = len(hexstr)
    if length % 2 != 0:
        hexstr = '0' + hexstr
        length += 1
    for i in range(0, length, 2):
        charlist.append(chr(int(hexstr[i]+hexstr[i+1], 16)))
    return charlist

if __name__ == '__main__':
    pattern = '\A[0-9a-fA-F]+\Z'
    request1 = raw_input('Give me the first hex vaule to encrypt: 0x').strip()
    if len(request1) > 96 or not re.match(pattern, request1):
        print 'invalid input, bye!'
        exit(0)
    plaintext1 = "".join(item for item in hex2charlist(request1)) + flag
    ciphertext1 = encrypt(plaintext1, refresh_key = True)
    plaintext1_str = request1+'|flag'
    ciphertext1_str = ciphertext1.encode('hex')
    print 'plaintext: 0x%s\nciphertext: 0x%s' % (plaintext1_str, ciphertext1_str)

    request2 = raw_input('Give me the second hex vaule to encrypt: 0x').strip()
    if len(request2) > 96 or not re.match(pattern, request2):
        print 'invalid input, bye!'
        exit(0)
    plaintext2 = "".join(item for item in hex2charlist(request2))
    ciphertext2 = encrypt(plaintext2, iv_p = str(ciphertext1[-16:]), refresh_key = False)
    plaintext2_str = request2
    ciphertext2_str = ciphertext2.encode('hex')
    print 'plaintext: 0x%s\nciphertext: 0x%s' % (plaintext2_str, ciphertext2_str)

# 7ca2c8df4a67c9205dadf4218358178d171a7fecb83aad105e4a6d8160588c19c50bd3ec92d74ab6621732444c5d2af1
# 6e0c9f29cbbde7a54f653d72c8e01924


# 00000000000000000000000000000000
# 836e304eeae2ff44a4c3d4a14e5d4092
# e0c058057ce7aa8fb4273a3eb88b2cce72655b1955d9a911522d10ebaf9d198f62d2f253aa522aecb8c02328a2694419836e304eeae2ff44a4c3d4a14e5d4092
# 9a2fa0a97f235ba3ab499a473f8d8422ca711bc1a538faf16c0979561dfff47b



# 00000000000000000000000000000000
# fd07804879207e288648f0850348df8b
# da74368f0c4c6613b5f94a02dd2e705c1f90ea3a059475afa5c5bf11716c0d21108ab420822b104ea61438cd8602b8cbfd07804879207e288648f0850348df8b
# 0488cda843842433564064de21bd6fe9f5ae914283559850bd6e1b098150cd62

bctf{3c1fffb76f1

bctf{3c1
bctf{3c1fffb76f147d420f984ac651
bctf{3c1fffb76f147d420f984ac651505905}
626374667b336331