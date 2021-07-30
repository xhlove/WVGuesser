![](https://imgur.com/cSwaXxz.png)

`WVGuesser` is an offline version implementation of [widevine-l3-guesser](https://github.com/Satsuoni/widevine-l3-guesser)

# Use

## Plugin installation

Unzip `WVGuesser-plugin.zip` and then `load the unzipped extensions`

Open the website that uses widevine, and after playing the video a configuration file will be downloaded automatically

that is `offline_config.json`, put it into the current directory

If you are just testing, you can skip this step, there is already a built-in configuration file

## Locally decrypted

If it is exe version, directly drag `offline_config.json` to `wvguesser_v1.1.0.exe`.

Run the program and wait for decryption

- `python -m wvguesser.mainv2`

According to the existing algorithm, it can only be single threaded

Demo

![](/images/oCam_2021_07_30_20_58_41_915.gif)


# package

```bash
pyinstaller -n wvguesser_v1.1.0 -F wvguesser\__main__.py
```

# Suggest a better solution

~~Not very good at C++ so I used python~~

- Pure C++ completion call
