
import numpy as np

def stringtobits(s):
    bits = []
    for letter in s:
        for shift in reversed(range(8)):
            bits.append((ord(letter) >> shift) & 1)
    return bits


def Pack32Bits(bits):
    assert bits.shape[0] % 32 == 0
    words = bits.reshape(int(bits.shape[0]/32), 32)
    packed = np.zeros(int(words.shape[0]), dtype=np.uint32)
    for widx, word in enumerate(words):
        value = 0
        for idx, bit in enumerate(reversed(word)):
            value += bit << idx
        packed[widx] = value
    return packed


def preprocess(m):
    # L + 1 + filler + 64
    inputlength = len(m) * 8
    fillerlength = 512 - ((inputlength+1+64) % 512)
    filler = ['0']*(fillerlength+1)
    filler[0] = 1
    size = [(inputlength >> shift) & 1 for shift in reversed(range(64))]
    message = np.array(stringtobits(m)+filler+size,dtype=np.uint8)
    return Pack32Bits(message)


def rightshift(w,n):
    return (w >> n) % 2**32


def leftshift(w,n):
    return (w << n) % 2**32


def rightrotate(w,n):
    return (w >> n) | ((2**n-1) & w) << (32-n)


def leftrotate(w,n):
    return ((w << n) % 2**32) | 2**(n+1)-1


def SHA256(message):


    H = np.array([0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19],dtype=np.uintc)
    k = np.array([0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
                0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
                0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
                0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
                0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
                0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
                0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
                0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2],dtype=np.uintc)


    m = preprocess(message)
    m = m.reshape(int(m.shape[0]/16), 16)
    for block in m:
        w = np.zeros(64,dtype=np.uint32)
        for idx, x in enumerate(block):
            w[idx] = x
        for r in range(16, 64):
            s0 = rightrotate(w[r-15], 7) ^ rightrotate(w[r-15], 18) ^ rightshift(w[r-15], 3)
            s1 = rightrotate(w[r-2], 17) ^ rightrotate(w[r-2], 19) ^ rightshift(w[r-2], 10)
            w[r] = (w[r-16] + s0 + w[r-7] + s1) % 2**32

        a = H[0]
        b = H[1]
        c = H[2]
        d = H[3]
        e = H[4]
        f = H[5]
        g = H[6]
        h = H[7]

        for i in range(64):
            
            S1 = rightrotate(e, 6) ^ rightrotate(e, 11) ^ rightrotate(e, 25)
            ch = (e & f) ^ ((~e) & g)
            S0 = rightrotate(a, 2) ^ rightrotate(a, 13) ^ rightrotate(a, 22)
            maj = (a & b) ^ (a & c) ^ (b & c)

            temp1 = (h + S1 + ch + k[i] + w[i]) % 2**32
            temp2 = (S0 + maj) % 2**32

            h = g
            g = f
            f = e
            e = (d + temp1) % 2**32
            d = c
            c = b
            b = a
            a = (temp1 + temp2) % 2**32

        H[0] = (H[0] + a) % 2**32
        H[1] += b
        H[2] += c
        H[3] += d
        H[4] += e
        H[5] += f
        H[6] += g
        H[7] += h

    result = [format(x,'x') for x in H]
    
    return ''.join(result)

if __name__ == '__main__':

    # with open('SHAIMPORT.py','r') as f:
    #     content = f.read()
    # print(SHA256(content))
    data = 'Cesar Garcia'
    print(f'Data: \"{data}\"')
    print(f'Bits in data: {len(data)*8}')
    hash = SHA256(data)
    print(f'Hash: \"{hash}\"')
