# WVGuesser

`WVGuesser` is a python implementation of [widevine-l3-guesser](https://github.com/Satsuoni/widevine-l3-guesser)

# Use

## Plugin installation

Unzip `WVGuesser-plugin.zip`, then `load the unzipped extension`

Open the website that uses widevine, and after playing the video, it will automatically download a configuration file

that is `offline_config.json`, put it into the current directory

If you are just testing, you can skip this step, there is already a built-in configuration file

## local crack

If it is the exe version, directly drag `offline_config.json` to `wvguesser_v1.0.0.exe` can be

First install [`wasmer-python`](https://github.com/wasmerio/wasmer-python)

```bash
pip install pycryptodome
pip install wasmer==1.0.0
pip install wasmer_compiler_cranelift==1.0.0
```

Run the program and wait for decryption

- `python -m wvguesser.main`

Call the exe version, which is relatively faster

- ``python -m wvguesser.mainv2``

According to the existing algorithm, it can only be single-threaded

# Packages

```bash
pyinstaller -n wvguesser_v1.0.0 -F wvguesser\__main__.py
```

# Suggest a better solution

~~ Not very good at C++ so I used python~~

- Use C++ to complete the call, multi-threaded to speed up
