# 0x00

感谢[pwnable.kr](http://pwnable.kr)提供的wargame平台，[stackoverflow.com](http://stackoverflow.com)提供问答平台。

# 0x01 input

题目不难理解，我打算采用python脚本。

> Stage 1 Popen参数为string在python中是对象类型，转为shell相当于后面添一个'\x00'的字符数组，因此'\x00'参数直接填''。参考这篇[stackoveflow](http://stackoverflow.com/questions/41007643/typeerror-execv-arg-2-must-contain-only-strings)。

> Stage 2 向子进程标准输入及标准错误输出写入。参考这篇[stackoveflow](http://stackoverflow.com/questions/43189160/how-do-i-write-to-a-python-subprocess-stderr)。

> Stage 3 调用子进程时提供环境变量。参考这篇[python](https://docs.python.org/2/library/subprocess.html)。

> Stage 4 文件读写比较简单。

> Stage 5 socket读写。参考这篇[python](https://docs.python.org/2.7/library/socket.html)

```python
import sys
import os
from subprocess import *
from socket import *
from time import *

#Stage 1
a = ['./input']
a += ['a' for i in range(ord('A')-1)]
a += ['']
a += ['\x20\x0a\x0d']
a += ['15003']
a += ['a' for i in range(100-ord('D'))]

#Stage 4
f = open('\x0a','wb')
f.write('\x00\x00\x00\x00')
f.close()

r, w = os.pipe()

#Stage 3
p = Popen(a,stdin=PIPE,stderr=r,env={'\xde\xad\xbe\xef':'\xca\xfe\xba\xbe'})

#Stage 2
p.stdin.write('\x00\x0a\x00\xff')
p.stdin.flush()
os.close(r)
os.write(w,'\x00\x0a\x02\xff')
os.close(w)

#Stage 5
sleep(5)
s = socket(AF_INET,SOCK_STREAM)
s.connect(('127.0.0.1',15003))
s.sendall('\xde\xad\xbe\xef')
```

