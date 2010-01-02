"""Library for implementing Multipass for Tenderapp.
(c) http://bitbucket.org/mtrichardson/tender-multipass/
"""
import base64
import json
import hashlib
import urllib
from itertools import izip, cycle

from M2Crypto import EVP


class MultiPass(object):

    def __init__(self, site_key, api_key):
        secret = hashlib.sha1(api_key + site_key).digest()[:16]
        # Yes, really.
        self.iv = "OpenSSL for Ruby"
        self.aes = EVP.Cipher("aes_128_cbc", key=secret,
            iv=self.iv, op=1)

    def handle_xor(self, raw_string):
        """Double XOR the first block"""
        data = list(raw_string)
        new_data = [chr(ord(x) ^ ord(y)) for (x, y)
            in izip(raw_string[:16], cycle(self.iv))]
        data[:16] = new_data
        return ''.join(data)

    def encode(self, data):
        """Turns a dictionary into urlquoted base64'd encrypted JSON data.
        """
        raw_string = json.dumps(data)
        raw_string = self.handle_xor(raw_string)
        v = self.aes.update(raw_string)
        v += self.aes.final()
        return urllib.quote(v.encode('base64'))
