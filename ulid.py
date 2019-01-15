r"""ULID objects (universally unique lexicographically sortable identifiers)
according to the ULID spec [https://github.com/ulid/spec]

This module provides immutable ULID objects (class ULID) and the functions
ulid() to generate ulids according to the specifications
"""

import os
import sys


__author__ = "Manikandan Sundararajan <tsmanikandan@protonmail.com>"

# Number of bits each ulid component should have
_timestamp = 50
_randomness = 80

# 32 Symbol notation
_crockford_base = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"

int_ = int  # The build-in int type
bytes_ = bytes  # The built-in bytes type


class ULID:
    """Instances of the ULID class represent ULIDS as specified in
    [https://github.com/ulid/spec]. ULIDS have 128-bit compatibility
    with UUID, Lexicographically sortable, case insensitive, URL safe
    and have a monotonic sort order (correctly detects and handles the
    same millisecond)
    """

    def __init__(self, bytes=None, int=None):

        if [bytes, int].count(None) != 1:
            raise TypeError("One of the bytes, int arguments must be given")

        if int is not None:
            if not 0 <= int < 1 << 128:
                raise ValueError("int is out of range (need a 128-bit value")

        if bytes is not None:
            if len(bytes) != 16:
                raise ValueError("bytes is not a 16-char string")
            assert isinstance(bytes, bytes_), repr(bytes)
            int = int_.from_bytes(bytes)

    # Function to generate the ulid
    def generate(self):
        import time

        epoch_bits = format(int(time.time() * 1000), f"0{_timestamp}b")
        # logging.info(f"EPOCH BITS  {epoch_bits}")

        rand_num_bits = ""
        try:
            rand_bytes = os.urandom(_randomness // 8)
        except NotImplementedError:
            raise NotImplementedError(
                "The /dev/urandom device is not available or readable"
            )

        # Get the randomness bits
        rand_num_bits = bin(int.from_bytes(rand_bytes, byteorder="big"))[2:]

        ulid_bits = epoch_bits + rand_num_bits
        ulid_str = ""
        for i in range(0, len(ulid_bits), 5):
            ulid_str += _crockford_base[int(ulid_bits[i : i + 5], base=2)]
        return ulid_str


if __name__ == "__main__":
    new_ulid = generate()
    print(new_ulid)
