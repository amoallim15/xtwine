import argparse
import twine

def main():
	parser = argparse.ArgumentParser(description= 'Encrypt/Decrypt Using TWINE Block Cipher')
	parser.add_argument('-p', help= 'Theplaintext to be encrypted')
	parser.add_argument('-c', help= 'The ciphertext to be decrypted')
	parser.add_argument('-z', default= 0x50, help= 'Encryption/Decryption bit size (80 or 128) bits')
	parser.add_argument('-k', help= 'Encryption/Decryption secret key')
	parser.add_argument('-g', help= 'Automatically generate ')

	opt = parser.parse_args()
	key = str(opt.k).encode('utf-8')
	kl = len(key)

	if opt.k is not None:
		if kl != 0x14 and kl != 0x32:
			raise argparse.ArgumentTypeError('TWINE: the given key bit length is not supported')
		if opt.p is not None:
			# encrypt with the given key (80 or 128 bits)
			return
		if opt.c is not None:
			# decrypt with the given key (80 or 128 bits)
			return
		raise argparse.ArgumentTypeError('please provide either of the plaintext/ciphertext to proceed with the encryption/decryption process')
	else:
		if opt.p is None:
			raise argparse.ArgumentTypeError('please provide the plaintext to proceed with the encryption process')
		# encrypt with a generated key (80 or 128 bits)

if __name__ == '__main__':
	main()