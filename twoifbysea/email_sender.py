"""Classes that attempt to send email

Todos:
    * Implement PGP encryption support. Receiver can use:
    https://www.openkeychain.org/apps/
"""

#Standard Python Library 2.7
#import subprocess
import smtplib
import logging
from copy import deepcopy
#import tempfile

#twoifbysea modules
import common #common.py
import config #config.py

GMAIL_SMTP_SERVER = 'smtp.gmail.com'

class SMTPAuthenticationFailureError(Exception):
    """There was a problem with SMTP authentication."""
    pass

class EmailSender(object):
    """Defines interface for senders of email"""

    def send(self, notif_req):
        """Send the email encapsulated in the notification request
        Returns: bool: Whether email was sent
        """
        assert isinstance(notif_req, common.NotificationRequest)
        raise NotImplementedError()

''' not working currently -- may resurrect in future
class UnixMailSender(EmailSender):
    """Sends unauthenticated email via the MAIL(1) UNIX command"""

    def send(self, notif_req):
        """Attempt to send email or deliver error notification

        Requires no email account but will instead use mail service
        on localhost.

        Todos:
            * Raise errors instead of returning if needed

        Returns: bool: Whether email was sent successfully
        """
        assert isinstance(notif_req, common.NotificationRequest)
        assert notif_req.channel == common.SupportedChannels.EMAIL

        #http://www.binarytides.com/linux-mail-command-examples/
        #mail -s subject bob1@example.com,bob2@example.com < contents_file

        email_body_filename = ''
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as email_body:
            email_body.write(notif_req.message)
            email_body_filename = email_body.name

        recipients = common.email_list_to_str(notif_req.recipients)
        command = ['mail']
        if notif_req.subject is not None:
            command.append('-s')
            command.append(notif_req.subject)
        command.append(recipients)
        #command.append('<')
        #command.append(email_body_filename)

        output = _get_command_result2(command, stdin=notif_req.message)
        print 'DEBUG: %s' % output
'''



class GmailSender(EmailSender):
    """Send email via authenticated gmail acount."""
    def __init__(self, gmail_username=None, gmail_password=None):
        if gmail_username is None:
            try:
                gmail_username = config.get_value('gmail_username')
            except config.KeyNotStoredAndNoFallbackError, err:
                raise SMTPAuthenticationFailureError(err)

        if (gmail_username is None or not isinstance(gmail_username, str) or
                gmail_username == ''):
            raise SMTPAuthenticationFailureError()

        if gmail_password is None:
            try:
                gmail_password = config.get_value('gmail_password')
            except config.KeyNotStoredAndNoFallbackError, err:
                raise SMTPAuthenticationFailureError(err)

        if (gmail_password is None or not isinstance(gmail_password, str) or
                gmail_password == ''):
            raise SMTPAuthenticationFailureError()

        self.username = gmail_username
        self.password = gmail_password

    def send(self, notif_req):
        """Send email via smtp.gmail.com

        Returns: bool: Whether email was sent
        """
        smtp_auth = {'username': self.username,
                     'password': self.password,
                     'server': GMAIL_SMTP_SERVER}
        recipient = deepcopy(notif_req.recipients).pop()
        return send_email(smtp_auth=smtp_auth, recipient=recipient,
                   subject=notif_req.subject, body=notif_req.message)

'''deprecated for now
def _get_command_result2(command, stdin=None):
    print "DEBUG: Entered _get_command_result with command={0} stdin={1}".format(
        str(command), str(stdin))
    print "DEBUG: About to popen..."
    proc = subprocess.Popen(command, )
    print "DEBUG: About to communicate()..."
    stdoutdata, stderrdata = proc.communicate(stdin)
    #TODO: consider this more deeply
    return stdoutdata

def _get_command_result(command):
    print "DEBUG: Entered _get_command_result with {0}".format(str(command))
    return subprocess.check_output(command, stderr=None, shell=True)
'''

def send_email(smtp_auth, recipient, subject, body):
    """Send email via SMTP.

    Args:
        smtp_auth (dict): Contains 'username' (str), 'password' (str), and
            'server' (str).
        recipient (str): The email address to send to
        subject (str)
        body (str)

    Returns: bool: Whether email was successfully sent according to STMP server

    http://stackoverflow.com/questions/10147455/trying-to-send-email-gmail-as-mail-provider-using-python
    """
    email_to = [recipient]

    #Sending message, first construct actual message
    message = ("From: {0}\nTo: {1}\nSubject: {2}\n\n{3}".format
               (smtp_auth['username'], ", ".join(email_to), subject, body))
    try:
        server_ssl = smtplib.SMTP_SSL(smtp_auth['server'], 465)
        server_ssl.ehlo()
        server_ssl.login(smtp_auth['username'], smtp_auth['password'])
        server_ssl.sendmail(smtp_auth['username'], email_to, message)
        server_ssl.close()
        return True
    except Exception, err:
        msg = 'Unable to send mail: {0}'.format(err)
        common.log(msg=msg, level=logging.ERROR)
        return False
