"""Unit tests for crypt"""

#Python Standard Library 2.7
import unittest
import os

#pip modules
from Crypto.Cipher import AES

#twoifbysea modules
from twoifbysea import crypt, common

MIN_LENGTH = (crypt.STANDARD_PAD_LENGTH + crypt.PREFIX_PAD_LENGTH +
              crypt.SUFFIX_PAD_LENGTH)

LONG_MESSAGE = (
    "Hello this is my message in plaintext and it is longer than a "
    "single block of data. Aardvark Albatross Alligator Alpaca Ant "
    "Anteater Antelope Ape Armadillo Ass Baboon Badger Barracuda Bat "
    "Bear Beaver Bee Bird Bison Boar Buffalo Butterfly Camel Caribou "
    "Cassowary Cat Caterpillar Cattle Chamois Cheetah Chicken "
    "Chimpanzee Chinchilla Chough Coati Cobra Cockroach Cod Cormorant "
    "Coyote Crab Crane Crocodile Crow Curlew Deer Dinosaur Dog Dogfish "
    "Dolphin Donkey Dotterel Dove Dragonfly Duck Dugong Dunlin")

class PaddingTest(unittest.TestCase):
    """Test random_pad"""
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def check_random_padded_length(self, msg, padded):
        """Ensure length is correct -- msg + prefix + suffix"""
        expected_len = len(msg)+ crypt.PREFIX_PAD_LENGTH + crypt.SUFFIX_PAD_LENGTH

        self.assertEqual(len(padded), expected_len)

    def check_length(self, msg, padded, expected_len=None):
        """Ensure length of result of crypt.pad() is correct

        Message should be padded to at least STANDARD_PAD_LENGTH and length
        should be mod STANDARD_PAD_LENGTH. Then, the prefix and suffix are
        added.
        """
        if expected_len is None:
            expected_pad = (crypt.STANDARD_PAD_LENGTH -
                            (len(msg) % crypt.STANDARD_PAD_LENGTH))
            expected_len = (len(msg) + expected_pad + crypt.PREFIX_PAD_LENGTH +
                            crypt.SUFFIX_PAD_LENGTH)
            if len(msg) < crypt.STANDARD_PAD_LENGTH:
                expected_len = MIN_LENGTH

        self.assertEqual(len(padded), expected_len)

    def is_good(self, msg):
        """Check out that all manner of padding looks correct"""
        padded = crypt.random_pad(msg)
        self.check_random_padded_length(msg, padded)
        self.check_message(msg, padded)

        very_padded = crypt.pad(msg)
        self.check_length(msg, very_padded)
        self.check_message(msg, very_padded)

    def check_message(self, msg, padded):
        """Ensure that 'msg' portion of padded is correct"""
        msg_portion = padded[crypt.PREFIX_PAD_LENGTH:crypt.PREFIX_PAD_LENGTH + len(msg)]
        self.assertEqual(len(msg), len(msg_portion))
        self.assertEqual(msg, msg_portion)

    def test_short_message_padded(self):
        """Messages should be padded to min of STANDARD_PAD_LENGTH.
        This is intended to make it harder to determine message length from
        the lenth of the ciphertext.
        """
        for i in range(0, crypt.STANDARD_PAD_LENGTH):
            msg = 'a' * i
            padded = crypt.standard_pad(msg)
            self.assertEqual(len(padded), crypt.STANDARD_PAD_LENGTH)

            very_padded = crypt.pad(msg)
            self.check_length(msg, very_padded)

    def test_random_pad_empty(self):
        """Verify an empty message is padded correctly"""
        msg = ""
        self.is_good(msg)

    def test_random_pad_short(self):
        """Verify a short string is padded correctly"""
        msg = "x"
        self.is_good(msg)

    def test_random_pad_long(self):
        """Verify that data is padded correctly"""
        msg = LONG_MESSAGE
        self.is_good(msg)

class EncryptionTest(unittest.TestCase):
    """Test encryption and decryption"""
    def __init__(self, methodName='runTest'):
        super(EncryptionTest, self).__init__(methodName)
        self.key = None

    def setUp(self):
        self.key = common.b64encode(os.urandom(32))

    def tearDown(self):
        pass

    def is_b64(self, data):
        """Is the data  base 64 encoded string?"""
        self.assertTrue(isinstance(data, str))
        common.b64decode(data) #raises TypeError

    def is_good(self, msg, is_arr=False):
        """Make sure the msg encrypts and decrypts properly"""
        (iv, ciphertext) = crypt.encrypt(data=msg, key=self.key)
        self.is_b64(iv)
        self.assertEqual(len(common.b64decode(iv)), AES.block_size)
        self.is_b64(ciphertext)
        plaintext = crypt.decrypt(ciphertext=ciphertext, key=self.key, iv=iv)
        if is_arr:
            self.assertEqual(str(msg), plaintext)
        else:
            self.assertEqual(msg, plaintext)

    def test_empty(self):
        """Test encryption and decryption of empty message"""
        self.is_good("")

    def test_some_array(self):
        """Test encryption and encryption with an array of non-string vals"""
        self.is_good(range(0, 100), is_arr=True)

    def test_short(self):
        """Test a short message"""
        self.is_good('x')

    def test_long(self):
        """Test a long message"""
        self.is_good(LONG_MESSAGE)

    def test_fail_on_bad_key_size(self):
        """Encryption should fail if they key size is wrong"""

        bad_key = '\x00' * 16
        with self.assertRaises(AssertionError):
            crypt.encrypt(data='', key=bad_key)

    def test_fail_on_bad_key_type(self):
        """Encryption should fail if the key type is wrong"""

        bad_key = [0] * 16
        with self.assertRaises(AssertionError):
            crypt.encrypt(data='', key=bad_key)

    def test_result_changes_each_encrypt(self):
        """The result of each encryption should change due to random padding."""
        iv = common.b64encode(os.urandom(AES.block_size))
        key = common.b64encode(os.urandom(32))
        ciphertexts = set()
        for _ in range(0, 10):
            iv_used, ciphertext = crypt.encrypt(data='', key=key, iv=iv)
            self.assertEqual(iv, iv_used)
            self.assertNotIn(ciphertext, ciphertexts)
            ciphertexts.add(ciphertext)

    def test_use_my_iv(self):
        """If we specify an iv, that one should be used for encryption"""
        iv = common.b64encode(os.urandom(AES.block_size))
        key = common.b64encode(os.urandom(32))
        iv_used = crypt.encrypt(data='', key=key, iv=iv)[0]
        self.assertEqual(iv, iv_used)
