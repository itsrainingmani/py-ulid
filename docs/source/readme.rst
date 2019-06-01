|ulid logo|

The py-ulid library is a *minimal*, self-contained implementation of
the ULID (Universally Unique Lexicographically Sortable Identifier)
specification in Python. For more information, please refer to the
`official specification`_.

Installation
------------

You can install the py-ulid library from `PyPi`_

.. code:: shell

   pip install py-ulid

The py-ulid library can be used in any version of python >= 3.5 and does
not require *any* additional packages or modules.

How to use
----------

To generate a ULID, simple run the generate() function

.. code:: python

   from ulid import ULID

   #Instantiate the ULID class
   ulid = ULID()
   ulid.generate()  #01BX5ZZKBKACTAV9WEVGEMMVRZ

Seeding Time
~~~~~~~~~~~~

You can instantiate the instance of the ULID class with a seed time
which will output the same string for the time component. This could be
useful when migrating to ulid

.. code:: python

   from ulid import ULID

   #Instantiate the ULID class
   ulid = ULID(1469918176385)
   ulid.generate()  #01ARYZ6S41TSV4RRFFQ69G5FAV

Monotonic ULIDs
~~~~~~~~~~~~~~~

.. code:: python

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

.. _official specification: https://github.com/ulid/spec
.. _PyPi: https://pypi.org/project/py-ulid
.. |ulid logo| image:: https://raw.githubusercontent.com/tsmanikandan/py-ulid/master/logo.png