def rs_hash(key):
    a = 378551
    b = 63689
    hash_value = 0
    for i in range(len(key)):
        hash_value = hash_value * a + ord(key[i])
        a = a * b
    return hash_value


def js_hash(key):
    hash_value = 1315423911
    for i in range(len(key)):
        hash_value ^= ((hash_value << 5) + ord(key[i]) + (hash_value >> 2))
    return hash_value


def pjw_hash(key):
    bits_in_unsigned_int = 4 * 8
    three_quarters = (bits_in_unsigned_int * 3) / 4
    one_eighth = bits_in_unsigned_int / 8
    high_bits = 0xFFFFFFFF << int(bits_in_unsigned_int - one_eighth)
    hash_value = 0
    test = 0

    for i in range(len(key)):
        hash_value = (hash_value << int(one_eighth)) + ord(key[i])
        test = hash_value & high_bits
    if test != 0:
        hash_value = ((hash_value ^ (test >> int(three_quarters))) & (~high_bits))
    return hash_value & 0x7FFFFFFF


def elf_hash(key):
    hash_value = 0
    for i in range(len(key)):
        hash_value = (hash_value << 4) + ord(key[i])
        x = hash_value & 0xF0000000
        if x != 0:
            hash_value ^= (x >> 24)
        hash_value &= ~x
    return hash_value


def bkdr_hash(key):
    seed = 131  # 31 131 1313 13131 131313 etc..
    hash_value = 0
    for i in range(len(key)):
        hash_value = (hash_value * seed) + ord(key[i])
    return hash_value


def sdbm_hash(key):
    hash_value = 0
    for i in range(len(key)):
        hash_value = ord(key[i]) + (hash_value << 6) + (hash_value << 16) - hash_value;
    return hash_value


def djb_hash(key):
    hash_value = 5381
    for i in range(len(key)):
        hash_value = ((hash_value << 5) + hash_value) + ord(key[i])
    return hash_value


def dek_hash(key):
    hash_value = len(key)
    for i in range(len(key)):
        hash_value = ((hash_value << 5) ^ (hash_value >> 27)) ^ ord(key[i])
    return hash_value


def bp_hash(key):
    hash_value = 0
    for i in range(len(key)):
        hash_value = hash_value << 7 ^ ord(key[i])
    return hash_value


def fnv_hash(key):
    fnv_prime = 0x811C9DC5
    hash_value = 0
    for i in range(len(key)):
        hash_value *= fnv_prime
        hash_value ^= ord(key[i])
    return hash_value


def ap_hash(key):
    hash_value = 0xAAAAAAAA
    for i in range(len(key)):
        if (i & 1) == 0:
            hash_value ^= ((hash_value << 7) ^ ord(key[i]) * (hash_value >> 3))
        else:
            hash_value ^= (~((hash_value << 11) + ord(key[i]) ^ (hash_value >> 5)))
    return hash_value