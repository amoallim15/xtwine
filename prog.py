from math import ceil
import datetime

sbox = {
	0x0: 0xC,
	0x1: 0x0,
	0x2: 0xF,
	0x3: 0xA,
	0x4: 0x2,
	0x5: 0xB,
	0x6: 0x9,
	0x7: 0x5,
	0x8: 0x8,
	0x9: 0x3,
	0xA: 0xD,
	0xB: 0x7,
	0xC: 0x1,
	0xD: 0xE,
	0xE: 0x6,
	0xF: 0x4
}

permutationENC = {
	0: 5,
	1: 0,
	2: 1,
	3: 4,
	4: 7,
	5: 12,
	6: 3,
	7: 8,
	8: 13,
	9: 6,
	10: 9,
	11: 2,
	12: 15,
	13: 10,
	14: 11,
	15: 14
}

permutationDEC = {
	0: 1,
	1: 2,
	2: 11,
	3: 6,
	4: 3,
	5: 0,
	6: 9,
	7: 4,
	8: 7,
	9: 10,
	10: 13,
	11: 14,
	12: 5,
	13: 8,
	14: 15,
	15: 12
}

con = {
	1: 0x01,
	2: 0x02,
	3: 0x04,
	4: 0x08,
	5: 0x10,
	6: 0x20,
	7: 0x03,
	8: 0x06,
	9: 0x0C,
	10: 0x18,
	11: 0x30,
	12: 0x23,
	13: 0x05,
	14: 0x0A,
	15: 0x14,
	16: 0x28,
	17: 0x13,
	18: 0x26,
	19: 0x0F,
	20: 0x1E,
	21: 0x3C,
	22: 0x3B,
	23: 0x35,
	24: 0x29,
	25: 0x11,
	26: 0x22,
	27: 0x07,
	28: 0x0E,
	29: 0x1C,
	30: 0x38,
	31: 0x33,
	32: 0x25,
	33: 0x09,
	34: 0x12,
	35: 0x24
}

def get4Bits(num, pos):
	return num >> 4 * pos & 0xF

def get32Bits(num, pos):
	return num >> 32 * pos & 0xFFFFFFFFFFFFFFFFFFFF		# 0xFFFF FFFF FFFF FFFF FFFF

def concatenate4Bits(*bits4):
	output = 0x0
	for i in range(len(bits4)):
		output = output << 4 | bits4[i]
	return output

def append32Bits(num, bits32):
	return num << 32 | bits32

def conL(i):
	return con[i] & 0b111

def conH(i):
	return con[i] >> 3 & 0b111

def rot4of16Bits(bits):
	shifted = bits >> 12 & 0xF 								# 16 - 4 = 12
	return (bits << 4 & 0xFFFF) | shifted						# 0xFFFF

def rot16of80Bits(bits):
	shifted = bits >> 64 & 0xFFFF 							# 80 - 16 = 64
	return (bits << 16 & 0xFFFFFFFFFFFFFFFFFFFF) | shifted	# 0xFFFF FFFF FFFF FFFF FFFF

def initXiBag():
	bag = {}
	for i in range(16):
		bag[i] = 0
	return bag

def initXBag():
	bag = {}
	for i in range(1, 37):
		bag[i] = initXiBag()
	return bag

def keySchedule80(key):
	RK = 0x0
# line 01
	WK = {
		0: get4Bits(key, 19),
		1: get4Bits(key, 18),
		2: get4Bits(key, 17),
		3: get4Bits(key, 16),
		4: get4Bits(key, 15),
		5: get4Bits(key, 14),
		6: get4Bits(key, 13),
		7: get4Bits(key, 12),
		8: get4Bits(key, 11),
		9: get4Bits(key, 10),
		10: get4Bits(key, 9),
		11: get4Bits(key, 8),
		12: get4Bits(key, 7),
		13: get4Bits(key, 6),
		14: get4Bits(key, 5),
		15: get4Bits(key, 4),
		16: get4Bits(key, 3),
		17: get4Bits(key, 2),
		18: get4Bits(key, 1),
		19: get4Bits(key, 0)
	}
# line 02
	for r in range(1, 36):
# line 03 & 11
		RKr = concatenate4Bits(WK[1], WK[3], WK[4], WK[6], WK[13], WK[14], WK[15], WK[16])
		print('RK{0} {1:x}'.format(r, RKr))
		RK = append32Bits(RK, RKr)
# line 04
		WK[1] = WK[1] ^ sbox[WK[0]]
# line 05
		WK[4] = WK[4] ^ sbox[WK[16]]
# line 06
		WK[7] = WK[7] ^ conH(r)
# line 07
		WK[19] = WK[19] ^ conL(r)
# line 08
		WK00ToWK03 = concatenate4Bits(WK[0], WK[1], WK[2], WK[3])
		WK00ToWK03 = rot4of16Bits(WK00ToWK03)
		WK[0] = get4Bits(WK00ToWK03, 3)
		WK[1] = get4Bits(WK00ToWK03, 2)
		WK[2] = get4Bits(WK00ToWK03, 1)
		WK[3] = get4Bits(WK00ToWK03, 0)
# line 09
		WK00ToWK19 = concatenate4Bits(
			WK[0], WK[1], WK[2], WK[3], 
			WK[4], WK[5], WK[6], WK[7], 
			WK[8], WK[9], WK[10], WK[11], 
			WK[12], WK[13], WK[14], WK[15], 
			WK[16], WK[17], WK[18], WK[19]
		)
		WK00ToWK19 = rot16of80Bits(WK00ToWK19)
		WK[0] = get4Bits(WK00ToWK19, 19)
		WK[1] = get4Bits(WK00ToWK19, 18)
		WK[2] = get4Bits(WK00ToWK19, 17)
		WK[3] = get4Bits(WK00ToWK19, 16)
		WK[4] = get4Bits(WK00ToWK19, 15)
		WK[5] = get4Bits(WK00ToWK19, 14)
		WK[6] = get4Bits(WK00ToWK19, 13)
		WK[7] = get4Bits(WK00ToWK19, 12)
		WK[8] = get4Bits(WK00ToWK19, 11)
		WK[9] = get4Bits(WK00ToWK19, 10)
		WK[10] = get4Bits(WK00ToWK19, 9)
		WK[11] = get4Bits(WK00ToWK19, 8)
		WK[12] = get4Bits(WK00ToWK19, 7)
		WK[13] = get4Bits(WK00ToWK19, 6)
		WK[14] = get4Bits(WK00ToWK19, 5)
		WK[15] = get4Bits(WK00ToWK19, 4)
		WK[16] = get4Bits(WK00ToWK19, 3)
		WK[17] = get4Bits(WK00ToWK19, 2)
		WK[18] = get4Bits(WK00ToWK19, 1)
		WK[19] = get4Bits(WK00ToWK19, 0)
# line 10 & 11
	RK36 = concatenate4Bits(WK[1], WK[3], WK[4], WK[6], WK[13], WK[14], WK[15], WK[16])
	print('RK36 {0:x}'.format(RK36))
	RK = append32Bits(RK, RK36)
	return RK

def TWINE_Dec(C, RK):
	XBag = initXBag()
# line 01
	XBag[36] = {
		0: get4Bits(C, 15),
		1: get4Bits(C, 14),
		2: get4Bits(C, 13),
		3: get4Bits(C, 12),
		4: get4Bits(C, 11),
		5: get4Bits(C, 10),
		6: get4Bits(C, 9),
		7: get4Bits(C, 8),
		8: get4Bits(C, 7),
		9: get4Bits(C, 6),
		10: get4Bits(C, 5),
		11: get4Bits(C, 4),
		12: get4Bits(C, 3),
		13: get4Bits(C, 2),
		14: get4Bits(C, 1),
		15: get4Bits(C, 0)
	}
# line 02
	RKBag = {
		1: get32Bits(RK, 35),
		2: get32Bits(RK, 34),
		3: get32Bits(RK, 33),
		4: get32Bits(RK, 32),
		5: get32Bits(RK, 31),
		6: get32Bits(RK, 30),
		7: get32Bits(RK, 29),
		8: get32Bits(RK, 28),
		9: get32Bits(RK, 27),
		10: get32Bits(RK, 26),
		11: get32Bits(RK, 25),
		12: get32Bits(RK, 24),
		13: get32Bits(RK, 23),
		14: get32Bits(RK, 22),
		15: get32Bits(RK, 21),
		16: get32Bits(RK, 20),
		17: get32Bits(RK, 19),
		18: get32Bits(RK, 18),
		19: get32Bits(RK, 17),
		20: get32Bits(RK, 16),
		21: get32Bits(RK, 15),
		22: get32Bits(RK, 14),
		23: get32Bits(RK, 13),
		24: get32Bits(RK, 12),
		25: get32Bits(RK, 11),
		26: get32Bits(RK, 10),
		27: get32Bits(RK, 9),
		28: get32Bits(RK, 8),
		29: get32Bits(RK, 7),
		30: get32Bits(RK, 6),
		31: get32Bits(RK, 5),
		32: get32Bits(RK, 4),
		33: get32Bits(RK, 3),
		34: get32Bits(RK, 2),
		35: get32Bits(RK, 1),
		36: get32Bits(RK, 0)
	}
# line 3
	for i in reversed(range(2, 37)):
# line 4
		RKiBag = {
			0: get4Bits(RKBag[i], 7),
			1: get4Bits(RKBag[i], 6),
			2: get4Bits(RKBag[i], 5),
			3: get4Bits(RKBag[i], 4),
			4: get4Bits(RKBag[i], 3),
			5: get4Bits(RKBag[i], 2),
			6: get4Bits(RKBag[i], 1),
			7: get4Bits(RKBag[i], 0)
		}
# line 5
		for j in range(0, 8):
			XBag[i][2 * j + 1] = sbox[XBag[i][2 * j] ^ RKiBag[j]] ^ XBag[i][2 * j + 1]
# line 6
		for h in range(0, 16):
			XBag[i - 1][permutationDEC[h]] = XBag[i][h]
# line 7
	RK1Bag = {
		0: get4Bits(RKBag[1], 7),
		1: get4Bits(RKBag[1], 6),
		2: get4Bits(RKBag[1], 5),
		3: get4Bits(RKBag[1], 4),
		4: get4Bits(RKBag[1], 3),
		5: get4Bits(RKBag[1], 2),
		6: get4Bits(RKBag[1], 1),
		7: get4Bits(RKBag[1], 0)
	}
	for j in range(0, 8):
		XBag[1][2 * j + 1] = sbox[XBag[1][2 * j] ^ RK1Bag[j]] ^ XBag[1][2 * j + 1]
# line 8
	return concatenate4Bits(
		XBag[1][0], XBag[1][1], XBag[1][2], XBag[1][3],
		XBag[1][4], XBag[1][5], XBag[1][6], XBag[1][7], 
		XBag[1][8], XBag[1][9], XBag[1][10], XBag[1][11], 
		XBag[1][12], XBag[1][13], XBag[1][14], XBag[1][15]
	)


def TWINE_Enc(P, RK):
	XBag = initXBag()
# line 01
	XBag[1] = {
		0: get4Bits(P, 15),
		1: get4Bits(P, 14),
		2: get4Bits(P, 13),
		3: get4Bits(P, 12),
		4: get4Bits(P, 11),
		5: get4Bits(P, 10),
		6: get4Bits(P, 9),
		7: get4Bits(P, 8),
		8: get4Bits(P, 7),
		9: get4Bits(P, 6),
		10: get4Bits(P, 5),
		11: get4Bits(P, 4),
		12: get4Bits(P, 3),
		13: get4Bits(P, 2),
		14: get4Bits(P, 1),
		15: get4Bits(P, 0)
	}
# line 02
	RKBag = {
		1: get32Bits(RK, 35),
		2: get32Bits(RK, 34),
		3: get32Bits(RK, 33),
		4: get32Bits(RK, 32),
		5: get32Bits(RK, 31),
		6: get32Bits(RK, 30),
		7: get32Bits(RK, 29),
		8: get32Bits(RK, 28),
		9: get32Bits(RK, 27),
		10: get32Bits(RK, 26),
		11: get32Bits(RK, 25),
		12: get32Bits(RK, 24),
		13: get32Bits(RK, 23),
		14: get32Bits(RK, 22),
		15: get32Bits(RK, 21),
		16: get32Bits(RK, 20),
		17: get32Bits(RK, 19),
		18: get32Bits(RK, 18),
		19: get32Bits(RK, 17),
		20: get32Bits(RK, 16),
		21: get32Bits(RK, 15),
		22: get32Bits(RK, 14),
		23: get32Bits(RK, 13),
		24: get32Bits(RK, 12),
		25: get32Bits(RK, 11),
		26: get32Bits(RK, 10),
		27: get32Bits(RK, 9),
		28: get32Bits(RK, 8),
		29: get32Bits(RK, 7),
		30: get32Bits(RK, 6),
		31: get32Bits(RK, 5),
		32: get32Bits(RK, 4),
		33: get32Bits(RK, 3),
		34: get32Bits(RK, 2),
		35: get32Bits(RK, 1),
		36: get32Bits(RK, 0)
	}
# line 3
	for i in range(1, 36):
# line 4
		RKiBag = {
			0: get4Bits(RKBag[i], 7),
			1: get4Bits(RKBag[i], 6),
			2: get4Bits(RKBag[i], 5),
			3: get4Bits(RKBag[i], 4),
			4: get4Bits(RKBag[i], 3),
			5: get4Bits(RKBag[i], 2),
			6: get4Bits(RKBag[i], 1),
			7: get4Bits(RKBag[i], 0)
		}
# line 5
		for j in range(0, 8):
			XBag[i][2 * j + 1] = sbox[XBag[i][2 * j] ^ RKiBag[j]] ^ XBag[i][2 * j + 1]
# line 6
		for h in range(0, 16):
			XBag[i + 1][permutationENC[h]] = XBag[i][h]
# line 7
	RK36Bag = {
		0: get4Bits(RKBag[36], 7),
		1: get4Bits(RKBag[36], 6),
		2: get4Bits(RKBag[36], 5),
		3: get4Bits(RKBag[36], 4),
		4: get4Bits(RKBag[36], 3),
		5: get4Bits(RKBag[36], 2),
		6: get4Bits(RKBag[36], 1),
		7: get4Bits(RKBag[36], 0)
	}
	for j in range(0, 8):
		XBag[36][2 * j + 1] = sbox[XBag[36][2 * j] ^ RK36Bag[j]] ^ XBag[36][2 * j + 1]
# line 8
	print(XBag[36])
	return concatenate4Bits(
		XBag[36][0], XBag[36][1], XBag[36][2], XBag[36][3],
		XBag[36][4], XBag[36][5], XBag[36][6], XBag[36][7], 
		XBag[36][8], XBag[36][9], XBag[36][10], XBag[36][11], 
		XBag[36][12], XBag[36][13], XBag[36][14], XBag[36][15]
	)


KEY = 0x00112233445566778899
P = 0x0123456789ABCDEF

start = datetime.datetime.now()

RK = keySchedule80(KEY)
C = TWINE_Enc(P, RK)

end = datetime.datetime.now()

time_span = end - start

print('\n')

print('encryption time span: {0}'.format(time_span))

P_dec = TWINE_Dec(C, RK)

print('\n')
print('key: 0x{0:x}\n'.format(KEY))
print('plaintext: 0x{0:x}\n'.format(P))
print('RK: 0x{0:x}\n'.format(RK))
print('ciphertext: 0x{0:x}\n'.format(C))
print('decryptedtext: 0x{0:x}\n'.format(P_dec))



def encryptTEXT(text):
	textHex = text.encode("utf-8").hex()
	textEncrypted = ''
	for i in range(int(ceil(len(textHex) / float(16)))):
		textToEnc = ''
		if i == 0:
			textToEnc = textHex[-16*(i + 1):]
		else:
			textToEnc = textHex[-16*(i + 1): -16*i]
		textEncrypted += str(TWINE_Enc(int(textToEnc, 16), RK))
	return hex(int(textEncrypted))

hello_world_enc = encryptTEXT('hello world')
print('encryption of \'Hello World\': {0:s}\n'.format(hello_world_enc))



