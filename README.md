# TWINE: A Lightweight Block Cipher for Multiple Platforms

This repository is an implementation of [TWINE: A Lightweight Block Cipher for Multiple Platforms](TWINE_A_Lightweight_Block_Cipher_for_Multiple_Platforms.pdf) paper introduced by Tomoyasu Suzaki, Kazuhiko Minematsu, Sumio Morioka, and Eita Kobayashi.

## Installation

Install by pip from PyPI:

```sh
pip3 install twine
```

Or install latest version from github:

```sh
python3 -m pip install -U git+https://github.com/amoallim15/TWINE.git
```

## Usage
This repository contains a command line tool that can be used to ecnrypt plaintext samples using either of the supported 80 bits or 128 bits sized keys.

**Example 1**:

```sh
python3 twine "hello world" -k "<o8~I{?3Uz"
```

The output:

```
Encryption Key: "<o8~I{?3Uz"
abb90d4c0a8f67632cec7c01ee409ea1
```

**Example 2**:

```sh
python3 twine "01bbed92bccc2104b7e12141f1413ad6" -k "4ejqxfDL3#"
```

The output:

```
Decryption Key: "4ejqxfDL3#"
hello world
```

**Example 3**:

```sh
python3 twine "1 plus 1 equals 2"
```

The output:

```
Encryption Key: "8_D]H[!^M*"
0315a70682ac625cdced6a7ff834d629c2b70de4e2d1fc7b
```

**Example 4**:

```sh
python3 twine "1 plus 1 equals 2" -z 128
```

The output:

```
encryption key: "oti,D:H6[5WX|8jS"
7f9c4394decc4c59c94be30b49db5ef66943a2938416382f
```

**Example 5**:

```py
    from twine import Twine

    twine = Twine(key_size=0x50)
    # If the key param is not specified
    # it will generate a key automatically.
    ciphertext = twine.encrypt("Hello Word")
    print(cipertext) # > "abb90d4c0a8f67632cec7c01ee409ea1"
```

## Release History

* 1.0.1
    * read/write from/to stdin/stdout.

## About

[Ali Moallim](mailto:amoallim15@gmail.com)

## Contributing

Bug reports and pull requests are welcome on GitHub at https://github.com/amoallim15/base-emoji.
I'm also available for questions, feel free to get in touch.

## License
This code is licensed under [MIT](https://opensource.org/licenses/MIT).

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
