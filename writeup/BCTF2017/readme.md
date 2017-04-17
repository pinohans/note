## 0x00

参与者silbul@D.I.E，zzm@D.I.E，Guf0r@D.I.E

## 0x01 Hulk

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
> 因此可以通过第一次输入构造`p3`使得最后一位为flag的第1个字符，用相同字符填充`pp1`的前15个字符并枚举最后一个字符，并按照`pp1 ^ iv ^ c2`传入第二次加密，判断`c3 == cc1`即可泄漏flag。

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