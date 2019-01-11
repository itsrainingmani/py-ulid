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
    # logging.info(len(epoch_bits))
    # logging.info(f"EPOCH BITS  {epoch_bits}")
    rand_num_bits = ""

    # Get the randomness bits
    if sys.version_info > (3, 6, 0):
        logging.info("Can use the secrets module for generation")
        import secrets

        # secrets.randbits returns the random bits in the form of an int
        rand_num_bits = bin(secrets.randbits(80))[2:]
        # logging.info(f"RANDOM BITS {rand_num_bits}")
    else:
        logging.info("Use the os urandom method for generation")

        rand_num_bits = bin(
            int.from_bytes(os.urandom(RANDOMNESS / 8), byteorder="big")
        )[2:]
        # logging.info(f"RANDOM BITS {rand_num_bits}")

    ulid_bits = epoch_bits + rand_num_bits
    ulid_str = ""
    for i in range(0, len(ulid_bits), 5):
        ulid_str += CROCKFORDS_BASE32[int(ulid_bits[i : i + 5], base=2)]
    return ulid_str


if __name__ == "__main__":
    new_ulid = generate()
    print(new_ulid)
