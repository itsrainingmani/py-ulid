# content of test_ulid.py

import ulid


class TestUlid(object):
    def test_generate_length(self):
        _ulid = ulid.generate()
        print(_ulid)
        assert len(_ulid) == 26

    def test_ulid_object(self):
        _ulid = ulid.ULID(32143215987)
        assert _ulid != ulid.generate()