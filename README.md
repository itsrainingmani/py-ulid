# py-ulid - A ULID Implementation in Python

![ulid logo](https://raw.githubusercontent.com/tsmanikandan/py-ulid/master/logo.png)

The py-ulid library is a minimal and self-contained implementation of the ULID (Universally Unique Lexicographically Sortable Identifier) specification in Python.
For more information, please refer to the [official specification](https://github.com/ulid/spec).

## Installation

You can install the py-ulid library from [PyPi](https://pypi.org)

```shell
$ pip install py-ulid
```

The py-ulid library can be used in any version of python >= 3.5 and does not require any additional packages or modules.

## How to use

THe py-ulid library can be integrated into any of your existing python programs to provide generate, encode and decode ULIDs.

An example of a simple use case is shown below

```python
from ulid import ULID

def main():

  # Create an ULID object
  ulid = ULID()

  # Generate a ULID
  value = ulid.generate()

  print(value)

if __name__ == '__main__':
  main()
```

Running that sample program would yield an output as follows

```shell
$ python sample_ulid.py

01BX5ZZKBKACTAV9WEVGEMMVRZ
```

## Properties of an ULID

The proposed ULID spechas the following properties that give it an advantage over UUIDs

* 128-bit compatibility with UUID
* 1.21e+24 unique ULIDs per millisecond
* Lexicographically sortable!
* Canonically encoded as a 26 character string, as opposed to the 36 character UUID
* Uses Crockford's base32 for better efficiency and readability (5 bits per character)
* Case insensitive
* No special characters (URL safe)
* Monotonic sort order (correctly detects and handles the same millisecond)

## Prior Art

Partly inspired by:

* [Instagram](http://instagram-engineering.tumblr.com/post/10853187575/sharding-ids-at-instagram)
* [Firebase](https://firebase.googleblog.com/2015/02/the-2120-ways-to-ensure-unique_68.html)