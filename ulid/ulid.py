"""
This module provides immutable ULID objects (class ULID) according to the 
`ULID spec <https://github.com/ulid/spec>`_ and the functions *generate()* 
to generate ulids according to the specifications, *encode()* to transform a 
given integer to the canonical string representation of an ULID, and *decode()* to take 
a canonically encoded string and break it down into it's timestamp and randomness components.
The module also provides Monotonic sort order guarantee for ULIDs via the Monotonic
class and it's associated generate() function.

.. module:: ulid
    :platform: Unix, Windows
.. moduleauthor:: Manikandan Sundararajan <tsmanikandan@protonmail.com>

"""

import os
import sys
import time
import secrets
from typing import Any, Tuple
from datetime import datetime, timezone


__author__ = "Manikandan Sundararajan <tsmanikandan@protonmail.com>"

class ULID:
    """Instances of the ULID class represent ULIDS as specified in the 
    `ULID spec <https://github.com/ulid/spec>`_. ULIDS have 128-bit compatibility
    with UUID, are Lexicographically sortable, case insensitive and 
    URL safe
    """

        # Number of bits each ulid component should have
    _time = 50
    _randomness = 80

    # 32 Symbol notation
    crockford_base = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"

    # 2^48 - 1. Upto the year 10889 A.D
    MAX_EPOCH_TIME = 281474976710655

    def __init__(self, seed=None):
        self.seed_time = seed

    # Function to generate the ulid without monotonicity or ms time handling
    def generate(self) -> str:
        """
        Generate a 26 character ULID string encoded in Crockford's Base32

        :returns: Canonically encoded ULID string
        :rtype: str

        >>> from ulid import ULID
        >>> ulid = ULID()
        >>> ulid.generate()
        01BX5ZZKBKACTAV9WEVGEMMVRZ
        """
        if self.seed_time is None:
            curr_utc_timestamp = int(datetime.now(timezone.utc).timestamp() * 1000)
        else:
            curr_utc_timestamp = self.seed_time * 1000

        epoch_bits = format(curr_utc_timestamp, f"0{self._time}b")
        rand_num_bits = format(secrets.randbits(self._randomness), f"0{self._randomness}b")

        return self._from_bits_to_ulidstr(epoch_bits + rand_num_bits)

    # Function to encode an integer into a ulid canonical string
    def encode(self, i: int) -> str:
        """
        Convert a given integer into the canonical ULID string format

        :param i: The integer to convert
        :type i: int
        :returns: Canonically encoded ULID string
        :rtype: str
        :raises: TypeError, ValueError

        >>> from ulid import ULID
        >>> ulid = ULID()
        >>> ulid.encode(340282366920938463463374607431768167)
        00864KEJY6MZQSVCHD1SB08637
        """
        if not isinstance(i, int):
            raise TypeError("The input has to be an integer")
        if i < 0:
            raise ValueError("The input has to be a positive value")
        if i >= (1 << 128):
            raise ValueError("The input value is larger than 128 bits")

        ulid_bits = format(i, f"0{self._time + self._randomness}b")
        return self._from_bits_to_ulidstr(ulid_bits)

    # Function to encode a unix timestamp into ulid canonical string format
    def encode_timestamp(self, t: int) -> str:
        """
        Convert a given unix timestamp into the canonical ULID string format

        :param t: The unix timestamp to convert
        :type t: int
        :returns: Canonically encoded ULID string
        :rtype: str
        :raises: TypeError, ValueError

        >>> from ulid import ULID
        >>> ulid = ULID()
        >>> ulid.encode(281474976710655)
        7ZZZZZZZZZ
        """
        if not isinstance(t, int):
            raise TypeError("The timestamp has to be an integer")
        if t < 0:
            raise ValueError("The timestamp has to be a positive value")
        if t > self.MAX_EPOCH_TIME:
            raise ValueError("Cannot encode time larger than - {}".format(self.MAX_EPOCH_TIME))

        return self._from_bits_to_ulidstr(format(t, f"0{self._time}b"))

    def decode(self, s: str) -> Tuple[int, int]:
        """
        Given a properly formed ULID, return a tuple containing the 
        timestamp and the randomness component as ints

        :param s: ULID string to decode
        :type s: str
        :returns: (timestamp, randomness)
        :rtype: tuple(int, int)
        :raises: TypeError, ValueError

        >>> from ulid import ULID
        >>> ulid = ULID()
        >>> ulid.decode('01BX5ZZKBKACTAV9WEVGEMMVRY')
        (1508808576371, 392928161897179156999966)
        """
        if not isinstance(s, str):
            raise TypeError("The input value has to be a string")
        if len(s) > 26:
            raise ValueError("The string has to be 26 characters in length")

        ulid_bits = ""
        # Loop through the given string and find the position of the character
        # in crockfords base. Convert that position to a 5 bit string
        for c in s:
            pos = self.crockford_base.find(c)
            if pos == -1:
                raise ValueError("Invalid character: {} found in ulid string".format(c))
            ulid_bits += format(pos, f"0{5}b")
        epoch_time_in_ms = int(ulid_bits[0:self._time], base=2)

        if epoch_time_in_ms > self.MAX_EPOCH_TIME:
            raise ValueError("Cannot encode time larger than - {}".format(self.MAX_EPOCH_TIME))

        random_component = int(ulid_bits[self._time:], base=2)
        return (epoch_time_in_ms, random_component)

    def _from_bits_to_ulidstr(self, ulid_bits: str) -> str:
        ulid_str = ""
        for i in range(0, len(ulid_bits), 5):
            ulid_str += self.crockford_base[int(ulid_bits[i : i + 5], base=2)]
        return ulid_str

    # Function to print a given ULID as in the binary layout
    def pretty_print(self, s: str) -> None:
        """
        Print the given ULID string in a binary layout

        >>> from ulid import ULID
        >>> ulid = ULID()
        >>> ulid.pretty_print(ulid_str)
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |                      32_bit_uint_time_high                    |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |     16_bit_uint_time_low      |       16_bit_uint_random      |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |                       32_bit_uint_random                      |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |                       32_bit_uint_random                      |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        """
        # (timestamp, rand) = tuple(map(lambda x: bin(x)[2:], self.decode(s)))

        # interval = "".join(list(map(lambda a: '*' if a % 2 == 0 else '+', [for i in range(65)])))
        interval = "+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
        (timestamp, rand) = self.decode(s)

        time_bits = format(timestamp, f"0{48}b")
        rand_bits = format(rand, f"0{self._randomness}b")

        print("\n")
        print(interval)
        print("|" + " "*16 + time_bits[:32] + " "*15 + "|")
        print(interval)
        print("|" + " "*8 + time_bits[32:] + " "*7 + "|" + " "*8 + rand_bits[0:16] + " "*7 + "|")
        print(interval)
        print("|" + " "*16 + rand_bits[16:48]+ " "*15 + "|")
        print(interval)
        print("|" + " "*16 + rand_bits[48:] + " "*15 + "|")
        print(interval)


class Monotonic(ULID):
    """The Monotonic class represent an extension of the base ULID 
    class with the addition of a monotonic sort order (correctly 
    detects and handles the same millisecond)
    """

    def __init__(self, seed=None):
        self.__prev_utc_time = datetime(1970, 1, 1, tzinfo=timezone.utc)
        self.__prev_rand_bits = None
        self.seed_time = seed

    # Function to generate the ulid monotonically
    def generate(self) -> str:
        """
        Generate a 26 character ULID string encoded in Crockford's Base32

        :returns: Canonically encoded ULID string
        :rtype: str
        :raises: ValueError

        >>> from ulid import Monotonic
        >>> ulid = Monotonic()
        >>> ulid.generate()
        01BX5ZZKBKACTAV9WEVGEMMVRZ
        """
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
            return self._from_bits_to_ulidstr(ulid_bits)
        else:
            # The generate calls did not happen in the same millisecond
            self.__prev_utc_time = curr_utc_time
            curr_utc_timestamp = int(curr_utc_time.timestamp() * 1000)
            epoch_bits = format(curr_utc_timestamp, f"0{self._time}b")

            #Generate the randomness bits using the secrets modules
            rand_num_bits = format(secrets.randbits(self._randomness), f"0{self._randomness}b")
            self.__prev_rand_bits = rand_num_bits
            ulid_bits = epoch_bits + rand_num_bits
            return self._from_bits_to_ulidstr(ulid_bits)
