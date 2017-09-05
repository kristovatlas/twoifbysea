"""Unit tests for processing notification requests.

Todos:
    * Devise a scenario in which mail sending should fail, and test the error
        alert funtionality.

"""

import unittest
import tempfile
from twoifbysea import datastore, notify, common

'''deprecated
class UnixMailSendTest(unittest.TestCase):
    """Test funtionality of notify using a unix mail sender"""

    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile()

    def tearDown(self):
        self.temp_file.close()

    def test_send_valid_email(self):
        """Make sure create statement generator works correctly"""

        test_notif = common.NotificationRequest()
        test_notif.set_channel(common.SupportedChannels.EMAIL)
        test_notif.add_recipient('example@example.com')
        test_notif.set_subject('send_valid_email test')
        test_notif.set_when(common.SupportedTimes.ONCE_NEXT_BATCH)
        test_notif.set_message('send_valid_email message body')

        with datastore.DatabaseConnection(
            filename=self.temp_file.name, file_path_abs=True) as db_con:

            db_con.add_notification(test_notif)
            notify.run(db_con) #should not raise notify.NotificationSendError
'''
