## 0x00

参与者silbul@D.I.E，zzm@D.I.E，Guf0r@D.I.E

## 0x01 Checkin

> 直接nc输入token就行

## 0x02 Hulk

> CBC模式对称加密可以得到`iv`时的[一些利用和原理图](https://defuse.ca/cbcmodeiv.htm)
> 
> 题目中是用两位16进制表示字符，设`c`是第一次加密后的串，`p`是第一次加密前的串，`cc`是第二次加密后的串，`pp`是第二次加密前的串。

```python
iv = c[-32:]
ci = c[(i-1)*32:i*32]
pi = p[(i-1)*32:i*32]
cci = cc[(i-1)*32:i*32]
ppi = pp[(i-1)*32:i*32]
```

> 由下图容易得到

![](https://github.com/pinohans/note/blob/master/writeup/BCTF2017/Hulk/1.png?raw=true)

> 在第一次加密中：`encrpt(p3 ^ c2) = c3`
> 
> 在第二次加密中：由于两次加密的key相同，且已知初始`iv = c[-32:]`，
> 
> 此时传入`pp1 ^ iv ^ c2`即得到`encrpt(pp1 ^ iv ^ c2 ^ iv) = encrypt(pp1 ^ c2) = cc1`
> 
> 因此可以通过第一次输入构造`p3`使得最后1个字符为flag的第1个字符，用相同字符填充`pp1`的前15个字符并枚举最后1个字符，并按照`pp1 ^ iv ^ c2`传入第二次加密，判断`c3 == cc1`即可泄漏flag。

```python
from pwn import *
ans = ''
pa = ''
def work(p):
	for i in range(256):
		print i,chr(i)
		io = remote('202.112.51.217',9999)
		io.recvuntil('0x')

		io.sendline(p)
		io.recvline()

		tmp = io.recvline()
		c = tmp[tmp.find('0x')+2:-1]

		c1 = c[:32]
		c2 = c[32:64]
		c3 = c[64:96]
		iv = c[-32:]

		io.recvuntil('0x')

		pp = (p + pa)[-30:] + hex(i)[2:]

		pp = hex(int(pp,16) ^ int(iv,16) ^ int(c2,16))[2:]
		pp = '0'*(32 - len(pp))+pp

		io.sendline(pp)

		io.recvline()

		tmp = io.recvline()

		cc = tmp[tmp.find('0x')+2:-1]
		cc1 = cc[:32]
		print 'ans',ans
		print 'pa',pa
		print 'p',p
		if cc1 == c3:
			io.close()
			return hex(i)[2:]
		io.close()

p = '00'*47
while True:
	tmp = work(p)
	pa += tmp
	ans += chr(int(tmp,16))
	p = p[2:]
```

## 0x03 foolme

> 本来打算看论文，结果随便想了个处理方式试了几次就过了，深度神经网络还是不算很靠谱。
> 
> 第一步中md5碰撞前四位根据抽屉原理暴力即可
> 
> 第二步随机化`s*s`个像素正方形，边长`a < sqrt(w*h*2/256/s/s)`

```python
from PIL import Image
import random
import numpy as np
import math
import base64

from pwn import *

im = Image.open('a.jpg')

w,h = im.size

s = 3

a = int(math.sqrt(w*h*2/256/s/s))

l = (w-a*s)/(s+1)
t = (h-a*s)/(s+1)

def c(x):
	return (random.randint(0,256)+x)%256

for i in range(0,w-(l+a),l+a):
	for j in range(0,h-(t+a),t+a):
		for ii in range(i+l,i+l+a,1):
			for jj in range(j+t,j+t+a,1):
				r,g,b = im.getpixel((ii,jj))
				im.putpixel((ii,jj),(c(r),c(g),c(b)))

im.save('b.jpg')

io = remote('202.112.51.176',9999)
io.recvline()
tmp = io.recvline()

tmppos = tmp.find('"')
salt = tmp[tmppos+1:tmp.find('"',tmppos+1)]
r = tmp[tmp.find('==')+2:tmp.find('==')+2+4]

import hashlib

for i in range(1000000):
	m = hashlib.md5()
	m.update(str(i)+salt)
	if m.hexdigest()[:4] == r:
		io.recvline()
		io.sendline(str(i))

		io.recvline()

		io.sendline('etWiX0mp7BD3jGXNOljijdhdSsdYBbQK')

		io.recvline()
		io.recvline()
		
		image = base64.b64encode(open('b.jpg','rb').read())
		io.sendline(image)
		print io.recv()
		break
```

