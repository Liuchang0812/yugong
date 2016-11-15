#!/usr/bin/env python

from hashlib import sha256
import json


class BloomFilter(object):
    """A simple bloom filter"""

    def __init__(self, array_size=(1 * 1024), hashes=13):
        """Initializes a Filter() object
        Expects:
          array_size (in bytes): 4 * 1024 for a 4KB filter
          hashes (int): for the number of hashes to perform
        """
        self.filter = bytearray(array_size)  # The filter itself
        self.bitcount = array_size * 8  # Bits in the filter
        self.hashes = hashes  # The number of hashes to use

    def _hash(self, value):
        """Creates a hash of an int and yields a generator of hash functions
        Expects:
          value: int()
        Yields:
          generator of ints()
        """
        # Build an int() around the sha256 digest of int() -> value
        digest = int(sha256(value.__str__()).hexdigest(), 16)
        for _ in range(self.hashes):
            # bitwise AND of the digest and all of the available bit positions
            # in the filter
            yield digest & (self.bitcount - 1)
            # Shift bits in digest to the right, based on 256 (in sha256)
            # divided by the number of hashes needed be produced.
            # Rounding the result by using int().
            # So: digest >>= (256 / 13) would shift 19 bits to the right.
            digest >>= (256 / self.hashes)

    def add(self, value):
        """Bitwise OR to add value(s) into the self.filter
        Expects:
          value: generator of digest ints()
        """
        for digest in self._hash(value):
            # In-place bitwise OR of the filter, position is determined
            # by the (digest / 8) digest is described above in self._hash()
            # Bitwise OR is undertaken on the value at the location and
            # 2 to the power of digest modulo 8. Ex: 2 ** (30034 % 8)
            # to grantee the value is <= 128, the bytearray not being able
            # to store a value >= 256. Q: Why not use ((modulo 9) -1) then?
            self.filter[(digest / 8)] |= (2 ** (digest % 8))
            # The purpose here is to spread out the hashes to create a unique
            # "fingerprint" with unique locations in the filter array,
            # rather than just a big long hash blob.

    def query(self, value):
        """Bitwise AND to query values in self.filter
        Expects:
          value: value to check filter against (assumed int())
        """
        # If all() hashes return True from a bitwise AND (the opposite
        # described above in self.add()) for each digest returned from
        # self._hash return True, else False
        return all(self.filter[(digest / 8)] & (2 ** (digest % 8))
                   for digest in self._hash(value))

    def loads(self, s):
        ret = json.loads(s)

        self.hashes = ret['hashes']
        self.bitcount = ret['bitcount']
        self.filter = bytearray(ret['filter'])

    def dumps(self):
        ret = dict()
        ret['hashes'] = self.hashes
        ret['bitcount'] = self.bitcount
        ret['filter'] = [x for x in self.filter]
        return json.dumps(ret)


if __name__ == "__main__":
    bf = BloomFilter()

    bf.add(1234)
    bf.add(40005)
    bf.add(1)
    bf.add('helloworld')
    bf.add('helloworldforevery')

    print("Filter size {0} bytes").format(bf.filter.__sizeof__())

    print bf.query(1)  # True
    print bf.query(40005)  # True
    print bf.query(123)  # False
    print bf.query('helloworld')
    print bf.query('hellomath')
    s = bf.dumps()

    bf2 = BloomFilter()
    bf2.loads(s)

    print bf2.query(1)
    print bf2.query(2)
