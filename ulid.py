r"""ULID objects (universally unique lexicographically sortable identifiers)
according to the ULID spec [https://github.com/ulid/spec]

This module provides immutable ULID objects (class ULID) and the functions
ulid() to generate ulids according to the specifications
"""

import os
import sys
import time
import secrets


__author__ = "Manikandan Sundararajan <tsmanikandan@protonmail.com>"

# Number of bits each ulid component should have
__time = 50
__randomness = 80

# 32 Symbol notation
__crockford_base = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"

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
    curr_time_stamp = 0
    curr_ulid_bits = '0'

    def __init__(self, int=None):

        # if [int].count(None) == 1:
        #     raise TypeError("The int argument must be given")

        if int is not None:
            if int < 0 or int >= (1 << 128):
                raise ValueError("int is out of range (need a 128-bit value")
            self.__dict__["int"] = int
        else:
            self.__dict__["int"] = 0

    def __hash__(self):
        return hash(self.int)

    def __int__(self):
        return self.int

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, str(self))

    def __str__(self):
        ulid_bits = format(self.int, f"0{__time+__randomness}b")[2:]
        ulid_str = ""
        for i in range(0, len(ulid_bits), 5):
            ulid_str += __crockford_base[int(ulid_bits[i : i + 5], base=2)]
        return ulid_str

    # Function to generate the ulid
    def generate(self):

        epoch_bits = format(int(time.time() * 1000), f"0{__time}b")
        # logging.info(f"EPOCH BITS  {epoch_bits}")S

        rand_num_bits = ""

        #Generate the randomness bits using the secrets modules
        rand_num_bits = bin(secrets.randbits(__randomness))[2:]

        # Get the randomness bits
        # rand_num_bits = bin(int.from_bytes(rand_bytes, byteorder="big"))[2:]

        ulid_bits = epoch_bits + rand_num_bits
        return self.__from_bits_to_ulidstr(ulid_bits)

    def __from_bits_to_ulidstr(self, ulid_bits):
        ulid_str = ""
        for i in range(0, len(ulid_bits), 5):
            ulid_str += __crockford_base[int(ulid_bits[i : i + 5], base=2)]
        return ulid_str
