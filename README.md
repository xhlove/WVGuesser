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

![](https://i.imgur.com/T1Px1T9.png)

# Configuration file

Default Config:

```json
{
	"thread": 5,
	"notif": "True",
	"json": "True",
	"main_number": 5,
	"version": "1.3.2"
}
```


# Warning

Do not change anything in the configuration file unless you know what you are doing.


# Build

```bash
pyinstaller -n wvguesser_v1.3.1 -F wvguesser\__main__.py
```

# Changes done

Removal of excessive prints, addition of a notification system (to be specified in the build, activated by default), English translation & "BruteForce" results sent in Json.

# Suggest a better solution

~~Not very good at C++ so I used python~~

- Pure C++ completion call
