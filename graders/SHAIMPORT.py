import sys
from functools import reduce


H = ["6a09e667",
     "bb67ae85",
     "3c6ef372",
     "a54ff53a",
     "510e527f",
     "9b05688c",
     "1f83d9ab",
     "5be0cd19",
     ]


K = ["428a2f98", "71374491", "b5c0fbcf", "e9b5dba5", "3956c25b", "59f111f1",
     "923f82a4", "ab1c5ed5", "d807aa98", "12835b01", "243185be", "550c7dc3",
     "72be5d74", "80deb1fe", "9bdc06a7", "c19bf174", "e49b69c1", "efbe4786",
     "0fc19dc6", "240ca1cc", "2de92c6f", "4a7484aa", "5cb0a9dc", "76f988da",
     "983e5152", "a831c66d", "b00327c8", "bf597fc7", "c6e00bf3", "d5a79147",
     "06ca6351", "14292967", "27b70a85", "2e1b2138", "4d2c6dfc", "53380d13",
     "650a7354", "766a0abb", "81c2c92e", "92722c85", "a2bfe8a1", "a81a664b",
     "c24b8b70", "c76c51a3", "d192e819", "d6990624", "f40e3585", "106aa070",
     "19a4c116", "1e376c08", "2748774c", "34b0bcb5", "391c0cb3", "4ed8aa4a",
     "5b9cca4f", "682e6ff3", "748f82ee", "78a5636f", "84c87814", "8cc70208",
     "90befffa", "a4506ceb", "bef9a3f7", "c67178f2"]


def BEx_to_LEx(hex_str):
    byte_hex = bytearray.fromhex(hex_str)
    byte_hex.reverse()
    return byte_hex.hex()


def hex_to_bin32(hex_str):
    result = "{:032b}".format(int(hex_str, 16))
    assert len(result) == 32
    return result


def BEx_to_LEb32(hex_str):
    xLE = BEx_to_LEx(hex_str)
    return hex_to_bin32(xLE)


def ror(bits, shift):
    result = bits[-shift:]+bits[:-shift]
    assert len(result) == len(bits)
    return result


def rol(bits, shift):
    result = bits[shift:]+bits[:shift]
    assert len(result) == len(bits)
    return result


def r_shift(bits, shift):
    result = ("0"*shift)+(bits[:-shift])
    assert len(result) == len(bits)
    return result


def xor_2(a, b):
    if not len(a) == len(b):
        raise Exception("lengths doesn't match")
    return "".join([str(int(a[i] != b[i])) for i in range(len(a))])


def xor(*args):
    result = reduce(lambda x, y: xor_2(x, y), args)
    assert len(result) == len(args[0])
    return result


def bin_and32(a, b):
    int_a = int(a, 2)
    int_b = int(b, 2)
    return "{:032b}".format(int_a & int_b)


def bin_neg(a):
    return "".join(['1' if i == '0' else '0' for i in a])


def add_mod32(*args):
    int_args = list(map(lambda x: int(x, 2), args))
    added_int = sum(int_args)
    return "{:032b}".format(added_int % (2**32))


def bin_to_hex(bits):
    return hex(int(bits, 2))


def str_to_bin(string):
    return "".join(["{:08b}".format(ord(i)) for i in string])


def padding(bin_msg):
    L = len(bin_msg)
    k_ = 512 - ((L + 1 + 64) % 512)
    M = bin_msg + "1" + (k_ * "0") + "{:064b}".format(L)
    assert len(M) % 512 == 0, "Error in padding"
    return M


def split512(msg):
    if not len(msg) % 512 == 0:
        raise Exception("Received msg with length not a multiple of 512")

    return [msg[i:i+512] for i in range(0, len(msg), 512)]


def generate_msg_schedule(chunk_b512):
    if not len(chunk_b512) == 512:
        raise Exception("Recieved chunk with length not equal to 512")

    chunk_split32 = [chunk_b512[i:i+32] for i in range(0, len(chunk_b512), 32)]

    words = [""] * 64

    for i in range(0, 16):
        words[i] = chunk_split32[i]

    for i in range(16, 64):
        s0 = xor(ror(words[i-15], 7), ror(words[i-15], 18), r_shift(words[i-15], 3))
        s1 = xor(ror(words[i-2], 17), ror(words[i-2], 19), r_shift(words[i-2], 10))
        words[i] = add_mod32(words[i-16], s0, words[i-7], s1)

    return words


H_LE = list(map(BEx_to_LEb32, H))
K_LE = list(map(BEx_to_LEb32, K))

H_BE = list(map(hex_to_bin32, H))
K_BE = list(map(hex_to_bin32, K))


def round(a, b, c, d, e, f, g, h, i, words, endian="little"):
    if endian == "little":
        K = K_LE
    else:
        K = K_BE
    s1 = xor(ror(e, 6), ror(e, 11), ror(e, 25))
    ch = xor(bin_and32(e, f), bin_and32(bin_neg(e), g))
    temp1 = add_mod32(h, s1, ch, K[i], words[i])

    s0 = xor(ror(a, 2), ror(a, 13), ror(a, 22))
    maj = xor(bin_and32(a, b), bin_and32(a, c), bin_and32(b, c))
    temp2 = add_mod32(s0, maj)

    h = g
    g = f
    f = e
    e = add_mod32(d, temp1)
    d = c
    c = b
    b = a
    a = add_mod32(temp1, temp2)

    return a, b, c, d, e, f, g, h


def SHA256(data):
    bin_message = str_to_bin(data)
    padded_msg = padding(bin_message)
    msg_chunks = split512(padded_msg)


    endian = 'big'

    if endian == 'little':
        H = H_LE.copy()
    else:
        H = H_BE.copy()

    h0, h1, h2, h3, h4, h5, h6, h7 = H[0], H[1], H[2], H[3], H[4], H[5], H[6], H[7]

    for chunk in msg_chunks:
        words = generate_msg_schedule(chunk)

        a, b, c, d, e, f, g, h = h0, h1, h2, h3, h4, h5, h6, h7
        for i in range(64):
            a, b, c, d, e, f, g, h = round(a, b, c, d, e, f, g, h, i, words, endian=endian)

        h0 = add_mod32(h0, a)
        h1 = add_mod32(h1, b)
        h2 = add_mod32(h2, c)
        h3 = add_mod32(h3, d)
        h4 = add_mod32(h4, e)
        h5 = add_mod32(h5, f)
        h6 = add_mod32(h6, g)
        h7 = add_mod32(h7, h)

    sha_bin = "".join([h0, h1, h2, h3, h4, h5, h6, h7])
    result = bin_to_hex(sha_bin)
    return result


if __name__ == '__main__':
    if(len(sys.argv) > 1):
        data = sys.argv[1]
    else:
        data = 'CPSC-570 Blockchain and Crypto Technologies'

    print(f'Data: \"{data}\"')
    print(f'Bits in data: {len(data)*8}')
    hash = SHA256(data)
    print(f'Hash: \"{hash}\"')
