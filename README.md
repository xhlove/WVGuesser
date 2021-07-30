# WVGuesser

`WVGuesser`是[widevine-l3-guesser](https://github.com/Satsuoni/widevine-l3-guesser)的python实现

# 使用

## 插件安装

解压`WVGuesser-plugin.zip`，然后`加载已解压的扩展程序`

打开使用widevine的网站，播放视频后会自动下载一个配置文件

即`offline_config.json`，把它复制到`wvguesser`目录下即可

如果只是测试，可以跳过这一步，已经内置了一个配置文件了

## 本地破解

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

# 推荐更好的方案

~~不太会C++所以就用了python~~

- 使用C++完成调用，多线程加快速度