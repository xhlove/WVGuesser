# WVGuesser

`WVGuesser`是[widevine-l3-guesser](https://github.com/Satsuoni/widevine-l3-guesser)的python实现

# 使用

## 插件安装

解压`WVGuesser-plugin.zip`，然后`加载已解压的扩展程序`

打开使用widevine的网站，播放视频后会自动下载一个配置文件

即`offline_config.json`，把它放到当前目录下即可

如果只是测试，可以跳过这一步，已经内置了一个配置文件了

## 本地破解

如果是exe版本，直接将`offline_config.json`拖到`wvguesser_v1.0.0.exe`上即可

首先安装[`wasmer-python`](https://github.com/wasmerio/wasmer-python)

```bash
pip install pycryptodome
pip install wasmer==1.0.0
pip install wasmer_compiler_cranelift==1.0.0
```

运行程序，等待解密

- `python -m wvguesser.main`

调用exe的版本，相对更快

- `python -m wvguesser.mainv2`

根据现有算法，只能是单线程

演示

![](/images/oCam_2021_07_30_20_58_41_915.gif)

# main.exe

使用mingw64编译

```bash
g++ -o main -pthread -std=gnu++0x main.cpp misc.cpp codelift.cpp algebra.cpp allocate.cpp integer.cpp
```

# 打包

```bash
pyinstaller -n wvguesser_v1.0.0 -F wvguesser\__main__.py
```

# 推荐更好的方案

~~不太会C++所以就用了python~~

- 纯C++完成调用