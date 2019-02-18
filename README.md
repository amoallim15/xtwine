# TWINE: A Lightweight Block Cipher for Multiple Platforms

This repository is an implementation of [TWINE: A Lightweight Block Cipher for Multiple Platforms](TWINE_A_Lightweight_Block_Cipher_for_Multiple_Platforms.pdf) paper introduced by Tomoyasu Suzaki, Kazuhiko Minematsu, Sumio Morioka, and Eita Kobayashi.

** Installation
Simply clone this repository via

	git clone https://github.com/AXJ15/TWINE.git

** Example
To ecnrypt a plaintext sample using a 80 bits size key, run the following command

	python ./twine -p '0123456789ABCDEF' -k '00112233445566778899'

The outputs:

	ciphertext: 7c1f0f80b1df9c28
	encryption key: 00112233445566778899
	key length: 80 bits
	encryption time: 0.01s

** Dependencies
- Python 3

** License
This code is licensed under [[https://www.gnu.org/licenses/gpl-3.0.en.html][GNU GPL v3]].

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
