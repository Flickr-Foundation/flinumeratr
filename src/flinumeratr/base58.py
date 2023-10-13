"""
A couple of functions related to base58 encoding, which is used for Flickr's short URLs.
"""

BASE58_ALPHABET = "123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ"


def is_base58(num):
    """
    Returns True if a string looks like a base58-encoded value, false otherwise.
    """
    return all(digit in BASE58_ALPHABET for digit in num)


def base58_decode(num):
    """
    Do a base58 decoding of a string, as used in flic.kr-style photo URLs.
    """
    # This is a Python translation of some PHP code posted by Flickr user kellan
    # at https://www.flickr.com/groups/51035612836@N01/discuss/72157616713786392/
    decoded = 0
    multi = 1

    while num:
        digit = num[-1]
        decoded += multi * BASE58_ALPHABET.index(digit)
        multi = multi * len(BASE58_ALPHABET)
        num = num[:-1]

    return str(decoded)
