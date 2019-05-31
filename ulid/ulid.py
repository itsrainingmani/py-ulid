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
    _time = 50
    _randomness = 80

    # 32 Symbol notation
    crockford_base = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"

    MAX_EPOCH_TIME = 281474976710655

    def __init__(self, seed=None):
        self.__prev_utc_time = datetime(1970, 1, 1, tzinfo=timezone.utc)
        self.__prev_rand_bits = None
        self.seed_time = seed

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, str(self))

    # Function to generate the ulid without monotonicity or ms time handling
    def generate(self) -> str:
        if self.seed_time is None:
            curr_utc_timestamp = int(datetime.now(timezone.utc).timestamp() * 1000)
            epoch_bits = format(curr_utc_timestamp, f"0{self._time}b")
        else:
            epoch_bits = format(self.seed_time*1000, f"0{self._time}b")
        
        rand_num_bits = format(secrets.randbits(self._randomness), f"0{self._randomness}b")
        ulid_bits = epoch_bits + rand_num_bits
        return self.__from_bits_to_ulidstr(ulid_bits)

    def encode(self, i: int) -> str:
        if i < 0 or i >= (1 << 128):
            raise ValueError("Input is out of range need a 128-bit value")
        ulid_bits = format(i, f"0{self._time + self._randomness}b")
        return self.__from_bits_to_ulidstr(ulid_bits)

    def decode(self, s: str) -> Tuple[int, int]:
        ulid_bits = ""
        for c in s:
            pos = self.crockford_base.find(c)
            ulid_bits += format(pos, f"0{5}b")
        epoch_time_in_ms = int(ulid_bits[0:self._time], base=2)

        if epoch_time_in_ms > self.MAX_EPOCH_TIME:
            raise ValueError("Timestamp is larger than the max possible value")

        random_component = int(ulid_bits[self._time:], base=2)
        return (epoch_time_in_ms, random_component)

    def __from_bits_to_ulidstr(self, ulid_bits: str) -> str:
        ulid_str = ""
        for i in range(0, len(ulid_bits), 5):
            ulid_str += self.crockford_base[int(ulid_bits[i : i + 5], base=2)]
        return ulid_str

class Monotic(ULID):
    """The Monotonic class represent an extension of the base ULID 
    class ULIDS with the addition of a monotonic sort order (correctly 
    detects and handles the same millisecond)
    """

    def __init__(self, seed=None):
        self.__prev_utc_time = datetime(1970, 1, 1, tzinfo=timezone.utc)
        self.__prev_rand_bits = None
        self.seed_time = seed

    # Function to generate the ulid monotonically
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
            epoch_bits = format(prev_utc_timestamp, f"0{self._time}b")

            # If for some reason the rand_bits for the last generate call were not set,
            # Set them to be some random bits
            if self.__prev_rand_bits is None:
                rand_num_bits = format(secrets.randbits(self._randomness), f"0{self._randomness}b")
            else:
                prev_rand_num = int(self.__prev_rand_bits, base=2)
                if len(bin(prev_rand_num + 1)[2:]) > self._randomness:
                    # Random component overflow
                    raise ValueError("The random component has overflowed")
                else:
                    rand_num_bits = format((prev_rand_num + 1), f"0{self._randomness}b")

            self.__prev_rand_bits = rand_num_bits
            ulid_bits = epoch_bits + rand_num_bits
            return self.__from_bits_to_ulidstr(ulid_bits)
        else:
            # The generate calls did not happen in the same millisecond
            self.__prev_utc_time = curr_utc_time
            curr_utc_timestamp = int(curr_utc_time.timestamp() * 1000)
            epoch_bits = format(curr_utc_timestamp, f"0{self._time}b")

            #Generate the randomness bits using the secrets modules
            rand_num_bits = format(secrets.randbits(self._randomness), f"0{self._randomness}b")
            self.__prev_rand_bits = rand_num_bits
            ulid_bits = epoch_bits + rand_num_bits
            return self.__from_bits_to_ulidstr(ulid_bits)