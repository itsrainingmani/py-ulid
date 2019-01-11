# Python Implementation of the ULID spec

import os
import sys
import logging

# Number of bits each ulid component should have
TIMESTAMP = 48
RANDOMNESS = 80

# 32 Symbol notation
CROCKFORDS_BASE32 = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"

# Function to generate the ulid
def generate():
    import time

    # Get the Unix Time in milliseconds as an int
    epoch = int(time.time() * 1000)
    epoch_bits = format(epoch, f"0{TIMESTAMP}b")
    logging.info(f"EPOCH BITS  {epoch_bits}")
    rand_num = 0
    rand_num_bits = ""

    if sys.version_info > (3, 6, 0):
        logging.info("Can use the secrets module for generation")
        import secrets

        rand_num = secrets.randbits(80)
        rand_num_bits = format(rand_num, f"0{RANDOMNESS}b")
        logging.info(f"RANDOM BITS {rand_num_bits}")
    else:
        logging.info("Use the os urandom method for generation")



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    generate()

