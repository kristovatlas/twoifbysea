"""Unit tests for common"""
import unittest
import os
from twoifbysea import common #common.py

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

VALID_EMAIL_ADDRS_FILENAME = 'valid_email_addresses.txt'
INVALID_EMAIL_ADDRS_FILENAME = 'invalid_email_addresses.txt'
WEIRD_EMAIL_ADDRS_FILENAME = 'weird_email_addresses.txt'

VALID_EMAIL_ADDRS_PATH = os.path.join(
    DIR_PATH, VALID_EMAIL_ADDRS_FILENAME)
INVALID_EMAIL_ADDRS_PATH = os.path.join(
    DIR_PATH, INVALID_EMAIL_ADDRS_FILENAME)
WEIRD_EMAIL_ADDRS_PATH = os.path.join(
    DIR_PATH, WEIRD_EMAIL_ADDRS_FILENAME)

LEVIATHAN = (
    'Man is distinguished, not only by his reason, but by this singular passion '
    'from other animals, which is a lust of the mind, that by a perseverance '
    'of delight in the continued and indefatigable generation of knowledge, '
    'exceeds the short vehemence of any carnal pleasure.')
LEVIATHAN_B64 = (
    'TWFuIGlzIGRpc3Rpbmd1aXNoZWQsIG5vdCBvbmx5IGJ5IGhpcyByZWFzb24sIGJ1dCBieSB0aGlz'
    'IHNpbmd1bGFyIHBhc3Npb24gZnJvbSBvdGhlciBhbmltYWxzLCB3aGljaCBpcyBhIGx1c3Qgb2Yg'
    'dGhlIG1pbmQsIHRoYXQgYnkgYSBwZXJzZXZlcmFuY2Ugb2YgZGVsaWdodCBpbiB0aGUgY29udGlu'
    'dWVkIGFuZCBpbmRlZmF0aWdhYmxlIGdlbmVyYXRpb24gb2Yga25vd2xlZGdlLCBleGNlZWRzIHRo'
    'ZSBzaG9ydCB2ZWhlbWVuY2Ugb2YgYW55IGNhcm5hbCBwbGVhc3VyZS4=')

class HelperFunctionsTest(unittest.TestCase):
    """Test funtionality of helper functions"""
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_valid_email_addr(self):
        """Make sure a valid email address passes"""
        with open(VALID_EMAIL_ADDRS_PATH) as valid_f:
            addresses = [addr for addr in valid_f.readlines()]
            for address in addresses:
                address = address.strip()
                if address != '':
                    self.assertTrue(
                        common.is_valid_email_addr(address), address)

    def test_invalid_email_addr(self):
        """Make sure an invalid email address fails"""
        with open(INVALID_EMAIL_ADDRS_PATH) as invalid_f:
            addresses = [addr for addr in invalid_f.readlines()]
            for address in addresses:
                address = address.strip()
                if address != '':
                    self.assertFalse(
                        common.is_valid_email_addr(address), address)

    def test_weird_email_addr(self):
        """Some email addresses are technically valid but we're OK w/ rejecting."""
        with open(WEIRD_EMAIL_ADDRS_PATH) as weird_f:
            addresses = [addr for addr in weird_f.readlines()]
            for address in addresses:
                address = address.strip()
                if address != '':
                    self.assertFalse(
                        common.is_valid_email_addr(address), address)

    def test_b64encode_sample(self):
        """Base-64 encode some sample text"""
        self.assertEqual(LEVIATHAN_B64, common.b64encode(LEVIATHAN))

    def test_b64decode_sample(self):
        """Base-64 decode some sample text"""
        self.assertEqual(LEVIATHAN, common.b64decode(LEVIATHAN_B64))

    def test_b64encode_urlsafe(self):
        """Base-64 encode text that generates encoding w/ last 2 chars of set"""
        self.assertEqual('-_s=', common.b64encode('\xfb\xfb'))

    def test_b64decode_urlsafe(self):
        """Base-64 decode text that generates encoding w/ last 2 chars of set"""
        self.assertEqual('\xfb\xfb', common.b64decode('-_s='))
