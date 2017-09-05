"""Demo of using the connectors.HTTPConnector for a Python client sending notifs

Usage: python examples/python_demo.py [optional-recipient@example.com]

Requires the following environment variables to be set:
* TWOIFBYSEA_DEFAULT_GMAIL_USERNAME
* TWOIFBYSEA_DEFAULT_GMAIL_PASSWORD
"""

#Python Standard Library 2.7
import sys
import os

# Adds parent directory into path
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")

#twoifbysea modules
from twoifbysea import connectors, common

DEMO_RECIPIENT = 'bob@example.com'
DEMO_ERROR_RECIPIENT = 'sad@example.com'
DEMO_SUBJECT = 'This is a demo notification'
DEMO_MESSAGE = 'This is a demo notification. This could be very important.'

def _main():
    recipients = [DEMO_RECIPIENT]
    if len(sys.argv) == 2:
        recipients = [sys.argv[1]]

    print 'Planning to send demo message to {0}...'.format(DEMO_RECIPIENT)

    with connectors.HTTPConnector() as con:
        con.notify(subject=DEMO_SUBJECT, body=DEMO_MESSAGE,
                   recipients=recipients, channel=common.SupportedChannels.GMAIL,
                   error_channel=common.SupportedChannels.GMAIL,
                   error_recipients=[DEMO_ERROR_RECIPIENT])

if __name__ == '__main__':
    _main()
