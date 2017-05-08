# 0x00

silbul@D.I.E，个人赛形式。

# 0x01 眼见非实

> 看到特征文件头PK，意识到是zip压缩，改后缀后搜索字符串flag即得到答案。

# 0x02 就在其中

> 得到pcapng文件，流量分析导出tcp流中的文件，rsa密钥对，用密钥解密得到答案。

```python
from Crypto import Random
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
from Crypto.PublicKey import RSA

r = Random.new().read

pk = open('test.key','rb').read()
bk = open('pub.key','rb').read()

rk = RSA.importKey(pk)
cipher = Cipher_pkcs1_v1_5.new(rk)
print(cipher.decrypt(open('key.txt','rb').read(),r))
```

# 0x03 Wheel Cipher

> Jefferson disk解密，每一行相当于一个转盘，每个转盘对应位置和密文相同，且圆盘顺序和密钥顺序相同时，其中一列即为答案，最后答案和经典游戏cs相关（游戏不白玩呀）。

```python
t = [
    'ZWAXJGDLUBVIQHKYPNTCRMOSFE',
    'KPBELNACZDTRXMJQOYHGVSFUWI',
    'BDMAIZVRNSJUWFHTEQGYXPLOCK',
    'RPLNDVHGFCUKTEBSXQYIZMJWAO',
    'IHFRLABEUOTSGJVDKCPMNZQWXY',
    'AMKGHIWPNYCJBFZDRUSLOQXVET',
    'GWTHSPYBXIZULVKMRAFDCEONJQ',
    'NOZUTWDCVRJLXKISEFAPMYGHBQ',
    'XPLTDSRFHENYVUBMCQWAOIKZGJ',
    'UDNAJFBOWTGVRSCZQKELMXYIHP',
    'MNBVCXZQWERTPOIUYALSKDJFHG',
    'LVNCMXZPQOWEIURYTASBKJDFHG',
    'JZQAWSXCDERFVBGTYHNUMKILOP']

k = [2, 3, 7, 5, 13, 12, 9, 1, 8, 10, 4, 11, 6]

c = 'NFQKSEVOQOFNP'

for id, i in enumerate(c):
    tmp = t[k[id] - 1]
    print(tmp[tmp.find(i) : ] + tmp[ : tmp.find(i)])
```

# 0x04 你猜猜。。

> 拖到HxD里面看到PK想到zip文件，发现文件残缺，查看zip文件格式详解之后填充，解压发现加密，利用fcrackzip解密得到答案。

```
$ fcrack -b -c1 -u -v output.zip
```

# 0x05 神秘图片

> png搜索iend的时候看到有两个，提取后面一个图片看到共济会密码，解出来即可，注意都是小写。

# 0x06 告诉你个秘密

> 两个十六进制串，base64解密之后，空格隔断每个字符，看键盘包裹的字符即为答案，注意都是大写。

# 0x07 二维码

> 扫描二维码知道要解路由器密码，一脸懵逼。然后看文件名有点意思，密码八位纯数，再次一脸懵逼。之后用binwalk发现存在压缩包，明白了八位纯数密码，用fcrackzip解出压缩包，看到有一个cap和一段文字——前四位是ISCC后四位是大写加数字，明白了解路由器密码的意思，用python做了一个字典，用aircrack-ng破解密码得到答案。

```sh
$ fcrackzip =b -c1 -l8 -u -v output.zip
```

```python
d = open('dict','w')

r = range(ord('0'),ord('9')+1) + range(ord('A'),ord('Z')+1)
for i in r:
    for j in r:
        for k in r:
            for l in r:
                d.write('ISCC'+chr(i)+chr(j)+chr(k)+chr(l)+'\n')
d.close()
```
```sh
$ aircrack-ng -w dict output.cap
```
