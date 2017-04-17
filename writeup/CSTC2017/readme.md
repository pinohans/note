# 0x00

参与者ybin1@D.I.E，silbul@D.I.E及zzm@D.I.E

# 0x01 签到-欢迎来到CSTC2017

> `ZmxhZ3tXZWlTdW9GeXVfQmllTGFuZ30=`base64解码

# 0x02 一维码

> 一看是一维码，直接保存图片，丢到在线的二维码解析器里解析（记得要把图片缩小一下再截图保存），解析得：

![](https://github.com/pinohans/note/blob/master/writeup/CSTC2017/一维码/1.png?raw=true)

> 上网查了一下，hydan是对可执行文件加密的，所以猜到图片中还有东西，看到提示LSB，直接放到StegSolve中，DateExcrate

![](https://github.com/pinohans/note/blob/master/writeup/CSTC2017/一维码/2.png?raw=true)

> 导出可执行文件，在linux下下载hydan并编译，查看README知道使用方法，直接解密，密码是hydan。得到flag

# 0x03 种棵树吧

> 下载下来一看是图片隐写，先放到binwalk里再说，一分析果然有东西，提取出来是一个压缩包，解压的1.gif，但是并不能打开。丢到winhex中，一看是头部坏掉了，修改头部打开，放到StegSolve中逐贞查看，是个中序遍历，再结合在2222.jpg中分析出来的后续遍历，是二叉树无疑。还原二叉树，先序遍历，出来不对。层次遍历，得到flag。

# 0x04 签到题

> 利用原理均在[freebuf](http://www.freebuf.com/articles/web/129607.html)，其中的示例代码1和示例代码2。

# 0x05 抽抽奖

> 脚本在jquery.js里，看到一串JSFuck编码[Decoder-JSFuck](https://enkhee-osiris.github.io/Decoder-JSFuck/)解码后即答案。

# 0x06 继续抽

> 脚本在页面内，首先要理解过程，爆破利用串`token+encode(md5(guess))`，`token`可以通过get访问`token.php`得到，`encode`方法通过观察得到，`guess`枚举int即可。

```python
import requests
import hashlib
import json
h = {
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:52.0) Gecko/20100101 Firefox/52.0',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
	'Accept-Encoding': 'gzip, deflate',
	'Cookie': 'PHPSESSID=v684pb5518cmrpgsgri0uu9s92',
	'Connection': 'keep-alive',
	'Upgrade-Insecure-Requests': '1'
}

def encode(str):
	return ''.join(hex(127-ord(i))[2:] for i in str)

s = requests.session()
i = 0
while True:
	m = hashlib.md5()
	m.update(str(i))
	r = s.get('http://117.34.111.15:81/token.php', headers = h)
	r = s.get("http://117.34.111.15:81/get.php?token="+json.loads(r.text)+"&id="+encode(m.hexdigest()), headers = h)
	print i,json.loads(r.text)['text']
	i += 1
```


