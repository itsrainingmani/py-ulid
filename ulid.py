r"""ULID objects (universally unique lexicographically sortable identifiers)
according to the ULID spec [https://github.com/ulid/spec]

This module provides immutable ULID objects (class ULID) and the functions
ulid() to generate ulids according to the specifications
"""

import os
import sys


__author__ = "Manikandan Sundararajan <tsmanikandan@protonmail.com>"

# Number of bits each ulid component should have
_time = 50
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

    int = 0

    def __init__(self, int=None):

        if [int].count(None) == 1:
            raise TypeError("The int argument must be given")

        if int is not None:
            if not 0 <= int < 1 << 128:
                raise ValueError("int is out of range (need a 128-bit value")

        self.__dict__["int"] = int

    def __eq__(self, other):
        if isinstance(other, ULID):
            return self.int == other.int
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, ULID):
            return self.int < other.int
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, ULID):
            return self.int > other.int
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, ULID):
            return self.int <= other.int
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, ULID):
            return self.int >= other.int
        return NotImplemented

    def __hash__(self):
        return hash(self.int)

    def __int__(self):
        return self.int

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, str(self))

    def __str__(self):
        ulid_bits = bin(int)[2:]
        ulid_str = ""
        for i in range(0, len(ulid_bits), 5):
            ulid_str += _crockford_base[int(ulid_bits[i : i + 5], base=2)]
        return ulid_str


# Function to generate the ulid
def generate():
    import time

    epoch_bits = format(int(time.time() * 1000), f"0{_time}b")
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
