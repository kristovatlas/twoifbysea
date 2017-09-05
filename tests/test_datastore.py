"""Unit tests for datastore"""

#Python Standard Library 2.7
import unittest
import tempfile
import random
import os

#pip modules
import blake2

#twoifbysea modules
from twoifbysea import datastore, common

ENABLE_DEBUG_PRINT = False

class DatabaseTableTest(unittest.TestCase):
    """Test funtionality of DatabaseTable class"""
    def setUp(self):
        self.table = datastore.DatabaseTable()

    def tearDown(self):
        pass

    def test_create_statement(self):
        """Make sure create statement generator works correctly"""
        self.table.name = 'myTable'
        self.table.cols = (('col1', 'INTEGER'), ('col2', 'TEXT'))
        expected = 'CREATE TABLE myTable (col1 INTEGER,col2 TEXT)'
        self.assertEqual(self.table.get_create_statement(), expected)

    def test_create_tbl_dict(self):
        """Create statement func should raise assertion if passed dict

        This is to avoid the table being created with cols out of order;
        an n-tuple of 2-tuples should be used instead.
        """
        self.table.name = 'myTable'
        self.table.cols = {'col1': 'INTEGER', 'col2': 'TEXT'}
        with self.assertRaises(AssertionError):
            self.table.get_create_statement()

class DatabaseConnectionTest(unittest.TestCase):
    """Test functionality of the DatabaseConnection class"""

    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile()
        self.app_id = common.b64encode(os.urandom(32))
        self.app_secret = common.b64encode(os.urandom(32))

    def tearDown(self):
        self.temp_file.close()

    def test_db_file_empty(self):
        """Initializes db if db file is initially empty."""
        self.assertEqual(os.stat(self.temp_file.name).st_size, 0)
        datastore.DatabaseConnection(filename=self.temp_file.name,
                                     file_path_abs=True)
        self.assertNotEqual(os.stat(self.temp_file.name).st_size, 0)


    def test_pop_fifo(self):
        """Pop should work in FIFO order.

        Uses random UUID as the point of comparison.
        """
        nr1 = get_dummy_email_notif_req()
        nr2 = get_dummy_email_notif_req()
        nr3 = get_dummy_email_notif_req()

        if ENABLE_DEBUG_PRINT:
            print("request #1: {0}".format(nr1.uuid))
            print("request #2: {0}".format(nr2.uuid))
            print("request #3: {0}".format(nr3.uuid))

        with datastore.DatabaseConnection(
            filename=self.temp_file.name, file_path_abs=True) as db_con:

            db_con.add_notification(nr1)
            nr1_expected = db_con.pop_notif()
            self.assertEqual(nr1.uuid, nr1_expected.uuid)
            self.assertNotEqual(nr2.uuid, nr1_expected.uuid)
            self.assertNotEqual(nr3.uuid, nr1_expected.uuid)
            db_con.add_notification(nr2)
            db_con.add_notification(nr3)
            nr2_expected = db_con.pop_notif()
            self.assertEqual(nr2.uuid, nr2_expected.uuid)
            self.assertNotEqual(nr1.uuid, nr2_expected.uuid)
            self.assertNotEqual(nr3.uuid, nr2_expected.uuid)

    def test_pop_removes_one_notif(self):
        """Popping a notification should cause it to be removed."""
        with datastore.DatabaseConnection(
            filename=self.temp_file.name, file_path_abs=True) as db_con:

            self.assertEqual(db_con.get_queue_size(), 0)
            nr1 = get_dummy_email_notif_req()
            nr2 = get_dummy_email_notif_req()
            db_con.add_notification(nr1)
            self.assertEqual(db_con.get_queue_size(), 1)
            db_con.add_notification(nr2)
            self.assertEqual(db_con.get_queue_size(), 2)
            db_con.pop_notif()
            self.assertEqual(db_con.get_queue_size(), 1)

    def test_store_key_val(self):
        """Store a key/value pair in the db"""
        with datastore.DatabaseConnection(filename=self.temp_file.name,
                                          file_path_abs=True) as db_con:

            key = 'myKey'
            val = 'myVal'
            db_con.store_key_val(app_id=self.app_id, app_secret=self.app_secret,
                                 key=key, val=val)

    def test_get_random_iv(self):
        """Retrieve random iv used to encrypt value in key-value store"""
        with datastore.DatabaseConnection(filename=self.temp_file.name,
                                          file_path_abs=True) as db_con:

            key = 'myKey'
            val = 'myVal'
            db_con.store_key_val(app_id=self.app_id, app_secret=self.app_secret,
                                 key=key, val=val)
            hashed_key = blake2.blake2(data=key, hashSize=64, key=self.app_secret)
            iv = db_con.get_iv(app_id=self.app_id, hashed_key=hashed_key)
            self.assertTrue(isinstance(iv, str))
            common.b64decode(iv) #raises TypeError

    def test_get_key_val(self):
        """Gey the value stored for 'key'"""
        with datastore.DatabaseConnection(filename=self.temp_file.name,
                                          file_path_abs=True) as db_con:

            key = 'myKey'
            val = 'myVal'
            db_con.store_key_val(app_id=self.app_id, app_secret=self.app_secret,
                                 key=key, val=val)

            value = db_con.get_key_val(app_id=self.app_id,
                                       app_secret=self.app_secret, key='myKey')
            self.assertEqual(val, value)

    def test_val_unretrievable_bad_app_id(self):
        """If the app id is not correct, the value should be unretrievable."""
        with datastore.DatabaseConnection(filename=self.temp_file.name,
                                          file_path_abs=True) as db_con:

            key = 'myKey'
            val = 'myVal'
            bad_secret = common.b64encode(os.urandom(32))
            db_con.store_key_val(app_id=self.app_id, app_secret=self.app_secret,
                                 key=key, val=val)

            with self.assertRaises(datastore.DecryptionFailError):
                db_con.get_key_val(
                    app_id=self.app_id, app_secret=bad_secret, key=key)

    def test_val_unretrievable_bad_app_secret(self):
        """If the app secret is not correct, the value should be unretrievable."""
        with datastore.DatabaseConnection(filename=self.temp_file.name,
                                          file_path_abs=True) as db_con:

            key = 'myKey'
            val = 'myVal'
            bad_app_id = datastore.generate_app_id()
            db_con.store_key_val(app_id=self.app_id, app_secret=self.app_secret,
                                 key=key, val=val)

            with self.assertRaises(datastore.DecryptionFailError):
                db_con.get_key_val(
                    app_id=bad_app_id, app_secret=self.app_secret, key=key)


def get_dummy_email_notif_req():
    """Generate a dummy notification request using email channel"""
    notif_req = common.NotificationRequest()
    notif_req.set_channel(common.SupportedChannels.EMAIL)
    notif_req.add_recipient('recipient1@example.com')
    notif_req.set_sender('sender@example.com')
    notif_req.set_subject('random subject {0}'.format(random.randint(1, 1000)))
    notif_req.set_when(common.SupportedTimes.ONCE_NEXT_BATCH)
    notif_req.set_message('random message {0}'.format(random.randint(1, 1000)))
    notif_req.set_error_channel(common.SupportedChannels.EMAIL)
    notif_req.add_error_recipient('error_recipient1@example.com')
    notif_req.assign_random_uuid()
    return notif_req
