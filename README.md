# WVGuesser

`WVGuesser`是[widevine-l3-guesser](https://github.com/Satsuoni/widevine-l3-guesser)的python实现

# 使用

首先安装[`wasmer-python`](https://github.com/wasmerio/wasmer-python)

```bash
pip install pycryptodome
pip install wasmer==1.0.0
pip install wasmer_compiler_cranelift==1.0.0
```

浏览器端拦截`licenseResponse.session_key`，替换本地`main.py`文件中的内容

执行下面的命令开始破解

- `python -m wvguesser.main`

# 补充

**当前完成部分实现**

- **当前仅实现求解session_key部分**
- **当前是单线程版本**
- **解密license.key还没有完成**

# TODO

- 多线程
- 完整实现，需要`licenseResponse.session_key`和`license.key`

# 推荐更好的方案

~~不太会C++所以就用了python~~

- 使用C++完成调用，多线程加快速度