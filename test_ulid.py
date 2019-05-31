# content of test_ulid.py

import ulid
import time
import pytest


class TestUlid(object):
    def test_generate_length(self):
        _ulid = ulid.ULID()
        val = _ulid.generate()
        assert len(val) == 26

    def test_ulid_max(self):
        with pytest.raises(ValueError, match=r".*128-bit.*"):
            ulid.ULID(340282366920938463463374607431768211459)

    def test_ulid_min(self):
        with pytest.raises(ValueError, match=r".*128-bit.*"):
            ulid.ULID(-1)

    def test_lexicographic_sort(self):
        _ulid = ulid.ULID()
        ul_list = []
        for i in range(100):
            val = _ulid.generate()
            ul_list.append(val)
        sorted_ul = sorted(ul_list)
        assert sorted_ul == ul_list

    def test_encode_ulid_mismatched_arg_type(self):
        _ulid= ulid.ULID()
        i = "Hello"
        with pytest.raises(TypeError):
            _ulid.encode(i)

    def test_encode_return_val_length(self):
        _ulid= ulid.ULID()
        i = 3402823669209384634633
        assert len(_ulid.encode(i)) == 26

    def test_ulid_encode_max(self):
        with pytest.raises(ValueError, match=r".*128-bit.*"):
            ulid.ULID().encode(340282366920938463463374607431768211459)

    def test_ulid_encode_min(self):
        with pytest.raises(ValueError, match=r".*128-bit.*"):
            ulid.ULID().encode(-1)

    def test_ulid_decode_max(self):
        _ulid = ulid.ULID()
        s = '7ZZZZZZZZZZZZZZZZZZZZZZZZZ'
        val = _ulid.decode(s)
        assert val == (281474976710655,1208925819614629174706175)

    def test_ulid_decode_overflow(self):
        with pytest.raises(ValueError, match=r".*The input is larger than the max possible ULID.*"):
            _ulid = ulid.ULID()
            s = '8ZZZZZZZZZZZZZZZZZZZZZZZZZ'
            val = _ulid.decode(s)