# 0x00

不知道说些什么好，对windows了解太少了，需要补充的东西太多了。

# 0x01 WMI

成功测试了一下WMI。

> 环境

python2.7.12，[pywin32-build221-x64](https://downloads.sourceforge.net/project/pywin32/pywin32/Build%20221/pywin32-221.win-amd64-py2.7.exe?r=https%3A%2F%2Fsourceforge.net%2Fprojects%2Fpywin32%2Ffiles%2Fpywin32%2FBuild%2520221%2F&ts=1491400781&use_mirror=iweb)。

> 注意

配置权限`控制面板->系统和安全->管理工具->计算机管理->服务和应用程序->WMI控件->属性->安全`。

> 测试工具

`win+r->wbemtest->连接（命名空间=\\<ip>\<namespace>，用户=username，密码=password）->连接`。

> python脚本

```python
#输出远程服务器进程id及进程名
import wmi
c = wmi.WMI(computer='172.24.71.62',user='pc',password='`',namespace='/root/cimv2')
for p in c.Win32_Process():
	print p.ProcessID, process.Name
```

# 0x02 DCOM编程

> 资料

[Python Programming on Win32](https://pan.baidu.com/s/1kV2tdHl)，vf6e。

> WMI

[API](https://msdn.microsoft.com/en-us/library/windows/desktop/aa394582(v=vs.85).aspx)。