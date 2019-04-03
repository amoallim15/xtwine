import argparse
import twine

def main():
	parser = argparse.ArgumentParser(description= 'Encrypt/Decrypt Using TWINE Block Cipher')
	parser.add_argument('-p', help= 'The plaintext to be encrypted')
	parser.add_argument('-c', help= 'The ciphertext to be decrypted')
	parser.add_argument('-z', default= 0x50, help= 'Encryption/Decryption bit size (80 or 128) bits')
	parser.add_argument('-k', help= 'Encryption/Decryption secret key')
	parser.add_argument('-g', help= 'Automatically generate ')

	opt = parser.parse_args()

	if opt.k is not None:
		if twine.check_key(opt.k) is not True:
			print(opt.k, opt.p)
			raise Exception('TWINE: the given key bit length is not supported')
			print('----------------------------------')
		if opt.p is not None:
			RK = twine.generate_RK(opt.k)
			cipher_blocks = twine.twine_enc(opt.p, RK)
			print('cipher blocks: {0}'.format(cipher_blocks))
			print('encryption key: {0}'.format(opt.k))
			return
		if opt.c is not None and len(opt.c) > 0:
			RK = twine.generate_RK(opt.k)
			plaintext = twine.twine_dec(opt.c, RK)
			print('plain text: {0}'.format(plaintext))
			print('decryption key: {0}'.format(opt.k))
			return
		raise Exception('please provide either of the plaintext/ciphertext to proceed with the encryption/decryption process')
	else:
		if opt.p is None:
			raise Exception('please provide the plaintext to proceed with the encryption process')
		key = twine.generate_key(int(opt.z))
		RK = twine.generate_RK(key)
		cipher_blocks = twine.twine_enc(opt.p, RK)
		print('cipher blocks: {0}'.format(cipher_blocks))
		print('encryption key: {0}'.format(key))
		# encrypt with a generated key (80 or 128 bits)

if __name__ == '__main__':
	main()
