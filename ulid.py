# Python Implementation of the ULID spec

import os
import sys
import logging

# Number of bits each ulid component should have
TIMESTAMP = 50
RANDOMNESS = 80

# 32 Symbol notation
CROCKFORDS_BASE32 = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"

# Function to generate the ulid
def generate():
    import time

    epoch_bits = format(int(time.time() * 1000), f"0{TIMESTAMP}b")
    # logging.info(f"EPOCH BITS  {epoch_bits}")

    rand_num_bits = ""
    try:
        rand_bytes = os.urandom(RANDOMNESS // 8)
    except NotImplementedError:
        raise NotImplementedError(
            "The /dev/urandom device is not available or readable"
        )

    # Get the randomness bits
    rand_num_bits = bin(int.from_bytes(rand_bytes, byteorder="big"))[2:]

    ulid_bits = epoch_bits + rand_num_bits
    ulid_str = ""
    for i in range(0, len(ulid_bits), 5):
        ulid_str += CROCKFORDS_BASE32[int(ulid_bits[i : i + 5], base=2)]
    return ulid_str


def encode(bits):
    if len(bits) != 128:
        raise ValueError("The argument has to be 128 bits in length")
    ulid_str = ""
    for i in range(0, len(bits), 5):
        ulid_str += CROCKFORDS_BASE32[int(bits[i : i + 5], base=2)]
    return ulid_str


if __name__ == "__main__":
    new_ulid = generate()
    print(new_ulid)

    import random

    print(encode(bin(random.getrandbits(127))[2:]))
