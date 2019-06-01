# content of test_ulid.py

import ulid.ulid as ulid
import time
import pytest
from datetime import datetime, timezone


class TestUlid(object):
    def test_generate_length(self):
        _ulid = ulid.ULID()
        val = _ulid.generate()
        assert len(val) == 26

    def test_monotonic_lexicographic_sort(self):
        _ulid = ulid.Monotonic()
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
        i = 340282366920938463463374607431768167
        val = _ulid.encode(i)
        print(val)
        assert len(val) == 26

    def test_ulid_encode_max(self):
        with pytest.raises(ValueError, match=r".*larger than 128.*"):
            ulid.ULID().encode(340282366920938463463374607431768211459)

    def test_ulid_encode_min(self):
        with pytest.raises(ValueError, match=r".*has to be a positive.*"):
            ulid.ULID().encode(-1)

    def test_ulid_encode_timestamp(self):
        _ulid= ulid.ULID()
        t = int(datetime.now(timezone.utc).timestamp() * 1000)
        val = _ulid.encode_timestamp(t)
        print(val)
        assert len(val) == 10

    def test_ulid_encode_timestamp_max(self):
        _ulid= ulid.ULID()
        t = 281474976710655
        val = _ulid.encode_timestamp(t)
        assert val == '7ZZZZZZZZZ'

    def test_ulid_decode_max(self):
        _ulid = ulid.ULID()
        s = '7ZZZZZZZZZZZZZZZZZZZZZZZZZ'
        val = _ulid.decode(s)
        assert val == (281474976710655,1208925819614629174706175)

    def test_ulid_decode(self):
        _ulid = ulid.ULID()
        s = '01BX5ZZKBKACTAV9WEVGEMMVRY'
        val = _ulid.decode(s)
        assert val == (1508808576371, 392928161897179156999966)

    def test_ulid_decode_overflow(self):
        with pytest.raises(ValueError, match=r".*Cannot encode time larger than.*"):
            _ulid = ulid.ULID()
            s = '8ZZZZZZZZZZZZZZZZZZZZZZZZZ'
            val = _ulid.decode(s)

    def test_pretty_print(self):
        _ulid= ulid.ULID()
        _ulid.pretty_print("01BX5ZZKBKACTAV9WEVGEMMVS0")