r"""ULID objects (universally unique lexicographically sortable identifiers)
according to the ULID spec [https://github.com/ulid/spec]

This module provides immutable ULID objects (class ULID) and the functions 
generate() to generate ulids according to the specifications, encode() to transform a 
given integer to the canonical string representation of an ULID, and decode() to take 
a canonically encoded string and break it down into it's timestamp and randomness 
components
"""

import os
import sys
import time
import secrets
from typing import Any, Tuple
from datetime import datetime, timezone


__author__ = "Manikandan Sundararajan <tsmanikandan@protonmail.com>"

class ULID:
    """Instances of the ULID class represent ULIDS as specified in
    [https://github.com/ulid/spec]. ULIDS have 128-bit compatibility
    with UUID, Lexicographically sortable, case insensitive, URL safe
    and have a monotonic sort order (correctly detects and handles the
    same millisecond)
    """

        # Number of bits each ulid component should have
    __time = 50
    __randomness = 80

    # 32 Symbol notation
    __crockford_base = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"

    # prev_utc_time is represented as datetime obj. Default is None
    __prev_utc_time = None
    __prev_rand_bits = None

    MAX_EPOCH_TIME = 281474976710655

    def __init__(self):
        self.__prev_utc_time = datetime(1970, 1, 1, tzinfo=timezone.utc)

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, str(self))

    # Function to generate the ulid
    def generate(self) -> str:
        #Get current UTC time as a datetime obj
        curr_utc_time = datetime.now(timezone.utc)
        # print("Now: {}, Last: {}".format(curr_utc_time, self.__prev_utc_time))

        # Calculate the difference in the current time and the last generated time
        # using the timedelta microseconds function
        ms_diff = (curr_utc_time - self.__prev_utc_time).microseconds / 1000
        # print("ms diff: {}".format(ms_diff))

        # The generate calls happened in the same millisecond
        if ms_diff <= 1.0:

            # Convert the prev time datetime object to a unix timestamp in milliseconds
            prev_utc_timestamp = int(self.__prev_utc_time.timestamp() * 1000)
            epoch_bits = format(prev_utc_timestamp, f"0{self.__time}b")

            # If for some reason the rand_bits for the last generate call were not set,
            # Set them to be some random bits
            if self.__prev_rand_bits is None:
                rand_num_bits = format(secrets.randbits(self.__randomness), f"0{self.__randomness}b")
            else:
                prev_rand_num = int(self.__prev_rand_bits, base=2)
                if len(bin(prev_rand_num + 1)[2:]) > self.__randomness:
                    # Random component overflow
                    raise ValueError("The random component has overflowed")
                else:
                    rand_num_bits = format((prev_rand_num + 1), f"0{self.__randomness}b")

            self.__prev_rand_bits = rand_num_bits
            ulid_bits = epoch_bits + rand_num_bits
            return self.__from_bits_to_ulidstr(ulid_bits)
        else:
            # The generate calls did not happen in the same millisecond
            self.__prev_utc_time = curr_utc_time
            curr_utc_timestamp = int(curr_utc_time.timestamp() * 1000)
            epoch_bits = format(curr_utc_timestamp, f"0{self.__time}b")

            #Generate the randomness bits using the secrets modules
            rand_num_bits = format(secrets.randbits(self.__randomness), f"0{self.__randomness}b")
            self.__prev_rand_bits = rand_num_bits
            ulid_bits = epoch_bits + rand_num_bits
            return self.__from_bits_to_ulidstr(ulid_bits)

    def encode(self, i: int) -> str:
        if i < 0 or i >= (1 << 128):
            raise ValueError("int is out of range need a 128-bit value")
        ulid_bits = format(i, f"0{self.__time + self.__randomness}b")
        return self.__from_bits_to_ulidstr(ulid_bits)

    def decode(self, s: str) -> Tuple[int, int]:
        ulid_bits = ""
        for c in s:
            pos = self.__crockford_base.find(c)
            ulid_bits += format(pos, f"0{5}b")
        epoch_time_in_ms = int(ulid_bits[0:self.__time], base=2)

        if epoch_time_in_ms > self.MAX_EPOCH_TIME:
            raise ValueError("Timestamp is larger than the max possible value")

        random_component = int(ulid_bits[self.__time:], base=2)
        return (epoch_time_in_ms, random_component)

    def __from_bits_to_ulidstr(self, ulid_bits: str) -> str:
        ulid_str = ""
        for i in range(0, len(ulid_bits), 5):
            ulid_str += self.__crockford_base[int(ulid_bits[i : i + 5], base=2)]
        return ulid_str
