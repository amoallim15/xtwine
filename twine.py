from collections import defaultdict as ddict
from os import urandom as rnd

sbox = {
	0x0: 0xC, 0x1: 0x0, 0x2: 0xF, 0x3: 0xA, 
	0x4: 0x2, 0x5: 0xB, 0x6: 0x9, 0x7: 0x5, 
	0x8: 0x8, 0x9: 0x3, 0xA: 0xD, 0xB: 0x7, 
	0xC: 0x1, 0xD: 0xE, 0xE: 0x6, 0xF: 0x4
}

permutationENC = { 
	0x0: 0x5, 0x1: 0x0, 0x2: 0x1, 0x3: 0x4, 
	0x4: 0x7, 0x5: 0xC, 0x6: 0x3, 0x7: 0x8, 
	0x8: 0xD, 0x9: 0x6, 0xA: 0x9, 0xB: 0x2, 
	0xC: 0xF, 0xD: 0xA, 0xE: 0xB, 0xF: 0xE
}

permutationDEC = { 
	0x0: 0x1, 0x1: 0x2, 0x2: 0xB, 0x3: 0x6, 
	0x4: 0x3, 0x5: 0x0, 0x6: 0x9, 0x7: 0x4, 
	0x8: 0x7, 0x9: 0xA, 0xA: 0xD, 0xB: 0xE, 
	0xC: 0x5, 0xD: 0x8, 0xE: 0xF, 0xF: 0xC
}

con = { 
	0x01: 0x01, 0x02: 0x02, 0x03: 0x04, 0x04: 0x08, 0x05: 0x10, 
	0x06: 0x20, 0x07: 0x03, 0x08: 0x06, 0x09: 0x0C, 0x0A: 0x18, 
	0x0B: 0x30, 0x0C: 0x23, 0x0D: 0x05, 0x0E: 0x0A, 0x0F: 0x14, 
	0x10: 0x28, 0x11: 0x13, 0x12: 0x26, 0x13: 0x0F, 0x14: 0x1E, 
	0x15: 0x3C, 0x16: 0x3B, 0x17: 0x35, 0x18: 0x29, 0x19: 0x11, 
	0x1A: 0x22, 0x1B: 0x07, 0x1C: 0x0E, 0x1D: 0x1C, 0x1E: 0x38, 
	0x1F: 0x33, 0x20: 0x25, 0x21: 0x09, 0x22: 0x12, 0x23: 0x24
}

def _S(i):
	return sbox[i]

def _CON_L(r):
	return con[r] & 0b111

def _CON_H(r):
	return con[r] >> 3 & 0b111
	
def _Rot4(bits):
	return bits[1:] + bits[:1]

def _Rot16(bits):
	return bits[4:] + bits[:4]

def _get_4_bits(source, pos):
	return source >> pos * 4 & 0xF

def _append_4_bits(source, bits):
	return source << 4 | bits

def _key_schedule_80(key):
	RK_32, WK_80 = ddict(ddict), []
	for i in range(20):
		WK_80.append(_get_4_bits(key, 20 - 1 - i))
	for r in range(1, 36):
		RK_32[r][0], RK_32[r][1], RK_32[r][2], RK_32[r][3], RK_32[r][4], RK_32[r][5], RK_32[r][6], RK_32[r][7] = WK_80[1], WK_80[3], WK_80[4], WK_80[6], WK_80[13], WK_80[14], WK_80[15], WK_80[16]
		WK_80[1] = WK_80[1] ^ _S(WK_80[0])
		WK_80[4] = WK_80[4] ^ _S(WK_80[16])
		WK_80[7] = WK_80[7] ^ _CON_H(r)
		WK_80[19] = WK_80[19] ^ _CON_L(r)
		WK0_to_WK3_16 = _Rot4(WK_80[:4])
		for j in range(len(WK0_to_WK3_16)):
			WK_80[j] = WK0_to_WK3_16[j]
		WK0_to_WK19_80 = _Rot16(WK_80[:20])
		for k in range(len(WK0_to_WK19_80)):
			WK_80[k] = WK0_to_WK19_80[k]
	RK_32[36][0], RK_32[36][1], RK_32[36][2], RK_32[36][3], RK_32[36][4], RK_32[36][5], RK_32[36][6], RK_32[36][7] = WK_80[1], WK_80[3], WK_80[4], WK_80[6], WK_80[13], WK_80[14], WK_80[15], WK_80[16]
	return RK_32

def _key_schedule_128(key):
	RK_32, WK_128 = ddict(ddict), []
	for i in range(32):
		WK_128.append(_get_4_bits(key, 32 - 1 - i))
	for r in range(1, 36):
		RK_32[r][0], RK_32[r][1], RK_32[r][2], RK_32[r][3], RK_32[r][4], RK_32[r][5], RK_32[r][6], RK_32[r][7] = WK_128[2], WK_128[3], WK_128[12], WK_128[15], WK_128[17], WK_128[18], WK_128[28], WK_128[31]
		WK_128[1] = WK_128[1] ^ _S(WK_128[0])
		WK_128[4] = WK_128[4] ^ _S(WK_128[16])
		WK_128[23] = WK_128[23] ^ _S(WK_128[30])
		WK_128[7] = WK_128[7] ^ _CON_H(r)
		WK_128[19] = WK_128[19] ^ _CON_L(r)
		WK0_to_WK3_16 = _Rot4(WK_128[:4])
		for j in range(len(WK0_to_WK3_16)):
			WK_128[j] = WK0_to_WK3_16[j]
		WK0_to_WK31_128 = _Rot16(WK_128[:32])
		for k in range(len(WK0_to_WK31_128)):
			WK_128[k] = WK0_to_WK31_128[k]
	RK_32[36][0], RK_32[36][1], RK_32[36][2], RK_32[36][3], RK_32[36][4], RK_32[36][5], RK_32[36][6], RK_32[36][7] = WK_128[2], WK_128[3], WK_128[12], WK_128[15], WK_128[17], WK_128[18], WK_128[28], WK_128[31]
	return RK_32

def _encrypt(P, RK):
	RK_32, X_16, C = dict(RK), ddict(lambda: ddict(int)), 0x0 
	for i in range(16):
		X_16[1][i] = _get_4_bits(P, 16 - 1 - i)
	for i in range(1, 36):
		for j in range(0, 8):
			X_16[i][2 * j + 1] = _S(X_16[i][2 * j] ^ RK_32[i][j]) ^ X_16[i][2 * j + 1]
		for h in range(0, 16):
			X_16[i + 1][permutationENC[h]] = X_16[i][h]
	for j in range(0, 8):
		X_16[36][2 * j + 1] = _S(X_16[36][2 * j] ^ RK_32[36][j]) ^ X_16[36][2 * j + 1]
	for i in range(16):
		C = _append_4_bits(C, X_16[36][i])
	return C

def _decrypt(C, RK):
	RK_32, X_16, P = dict(RK), ddict(lambda: ddict(int)), 0x0 
	for i in range(16):
		X_16[36][i] = _get_4_bits(C, 16 - 1 - i)
	for i in range(36, 1, -1):
		for j in range(0, 8):
			X_16[i][2 * j + 1] = _S(X_16[i][2 * j] ^ RK_32[i][j]) ^ X_16[i][2 * j + 1]
		for h in range(0, 16):
			X_16[i - 1][permutationDEC[h]] = X_16[i][h]
	for j in range(0, 8):
		X_16[1][2 * j + 1] = _S(X_16[1][2 * j] ^ RK_32[1][j]) ^ X_16[1][2 * j + 1]
	for i in range(16):
		P = _append_4_bits(P, X_16[1][i])
	return P


def parse_text(plaintext):
	plaintext = plaintext.uncode('utf-8').hex()
	#TODO:
	pass


