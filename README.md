# py-ulid - A ULID Implementation in Python

![ulid logo](https://raw.githubusercontent.com/tsmanikandan/py-ulid/master/logo.png)

[![Documentation Status](https://readthedocs.org/projects/py-ulid/badge/?version=latest)](https://py-ulid.readthedocs.io/en/latest/?badge=latest)

The py-ulid library is a minimal and self-contained implementation of the ULID (Universally Unique Lexicographically Sortable Identifier) specification in Python.
For more information, please refer to the [official specification](https://github.com/ulid/spec).

UUID can be suboptimal for many uses-cases because:

- It isn't the most character efficient way of encoding 128 bits of randomness
- UUID v1/v2 is impractical in many environments, as it requires access to a unique, stable MAC address
- UUID v3/v5 requires a unique seed and produces randomly distributed IDs, which can cause fragmentation in many data structures
- UUID v4 provides no other information than randomness which can cause fragmentation in many data structures

Instead, herein is proposed ULID:

- 128-bit compatibility with UUID
- 1.21e+24 unique ULIDs per millisecond
- Lexicographically sortable!
- Canonically encoded as a 26 character string, as opposed to the 36 character UUID
- Uses Crockford's base32 for better efficiency and readability (5 bits per character)
- Case insensitive
- No special characters (URL safe)
- Monotonic sort order (correctly detects and handles the same millisecond)

## Installation

You can install the py-ulid library from [PyPi](https://pypi.org/project/py-ulid)

```shell
pip install py-ulid
```

The py-ulid library can be used in any version of python >= 3.5 and does not require any additional packages or modules.

## How to use

To generate a ULID, simple run the generate() function

```python
from ulid import ULID

#Instantiate the ULID class
ulid = ULID()
ulid.generate()  #01BX5ZZKBKACTAV9WEVGEMMVRZ
```

### Seeding Time

You can instantiate the instance of the ULID class with a seed time which will output the same string for the time component. This could be useful when migrating to ulid

```python
from ulid import ULID

#Instantiate the ULID class
ulid = ULID(1469918176385)
ulid.generate()  #01ARYZ6S41TSV4RRFFQ69G5FAV
```

### Monotonic ULIDs

```python
from ulid import Monotonic

#Instantiate the Monotonic Class
ulid = Monotonic()

# Same timestamp when calls are made within the same
# millisecond and least-significant random bit is incremented by 1
ulid.generate()  #01DC8Y7RBV4RSXX0437Z1RQR11
ulid.generate()  #01DC8Y7RBV4RSXX0437Z1RQR12
ulid.generate()  #01DC8Y7RBV4RSXX0437Z1RQR13
ulid.generate()  #01DC8Y7RBV4RSXX0437Z1RQR14
ulid.generate()  #01DC8Y7RBV4RSXX0437Z1RQR15
ulid.generate()  #01DC8Y7RBV4RSXX0437Z1RQR16
ulid.generate()  #01DC8Y7RBV4RSXX0437Z1RQR17
ulid.generate()  #01DC8Y7RBV4RSXX0437Z1RQR18
ulid.generate()  #01DC8Y7RBV4RSXX0437Z1RQR19
```

## Prior Art

Partly inspired by:

- [Instagram](http://instagram-engineering.tumblr.com/post/10853187575/sharding-ids-at-instagram)
- [Firebase](https://firebase.googleblog.com/2015/02/the-2120-ways-to-ensure-unique_68.html)
