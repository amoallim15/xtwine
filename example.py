


KEY_80 = 0x00112233445566778899
KEY_128 = 0x00112233445566778899AABBCCDDEEFF

P = 0x0123456789ABCDEF
RK_80 =  _key_schedule_80(KEY_80)
RK_128 =  _key_schedule_128(KEY_128)

C_80 = _encrypt(P, RK_80)
C_128 = _encrypt(P, RK_128)

P_dec_80 = _decrypt(C_80, RK_80)
P_dec_128 = _decrypt(C_128, RK_128)

print('key 80 bits: 0x{0:x}\n'.format(KEY_80))
print('key 128 bits: 0x{0:x}\n'.format(KEY_128))

print('plaintext: 0x{0:x}\n'.format(P))
#print('RK: 0x{0:x}\n'.format(RK))

print('ciphertext 80 bits: 0x{0:x}\n'.format(C_80))
print('ciphertext 128 bits: 0x{0:x}\n'.format(C_128))

print('decryptedtext by 80 bits: 0x{0:x}\n'.format(P_dec_80))
print('decryptedtext by 128 bits: 0x{0:x}\n'.format(P_dec_128))

