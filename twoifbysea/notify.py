"""Read messages from the queue one at a time and attempt to send them.

This program should be called regularly (e.g. cron job) to empty the queue.

Todos:
    * Use multiple threads to improve speed.
"""

#Standard Python Library 2.7
import logging

#twoifbysea modules
import common #common.py
import datastore #datastore.py
import email_sender #email_sender.py

class NotificationSendError(Exception):
    """The notificiation request was not properly serviced"""
    pass

def run(db_con=None):
    """Fetch notification requests from queue and process them.

    Returns: None

    Raises: NotificationSendError if notification not sent successfully
    """
    if db_con is None:
        db_con = datastore.DatabaseConnection()
    notif_req = None
    while True:
        print "DEBUG"
        try:
            notif_req = db_con.pop_notif()
        except datastore.EmptyQueueError:
            info_message = "No requests remain in the queue. Done."
            print info_message
            common.log(msg=info_message, level=logging.INFO)
            return
        except datastore.DatabaseReadError, err:
            #TODO: handle
            raise datastore.DatabaseReadError(err)
        except datastore.DatabaseWriteError, err:
            #TODO: handle
            raise datastore.DatabaseWriteError(err)

        info_message = "Fetched 1 message from queue to '{0}' subject '{1}'".format(
            common.email_list_to_str(notif_req.recipients), notif_req.subject)
        print info_message
        common.log(msg=info_message, level=logging.INFO)

        if notif_req.channel == common.SupportedChannels.EMAIL:
            process_email(db_con, notif_req)
        elif notif_req.channel == common.SupportedChannels.GMAIL:
            process_gmail(db_con, notif_req)
        else:
            raise NotImplementedError() #TODO

def process_email(db_con, notif_req):
    """Try to send notification via SMTP"""
    raise NotImplementedError('Sending for non-GMail SMTP not yet implemented.')
    '''deprecated
    #TODO: support other kinds of email senders and implement "from" field

    if notif_req.when == common.SupportedTimes.ONCE_NEXT_BATCH:
        sent = email_sender.UnixMailSender().send(notif_req)

        if sent:
            status_msg = 'Email succesfully sent to {0}.'.format(
                str(notif_req.recipients))
            common.log(msg=status_msg, level=logging.INFO)
            print status_msg

        if not sent:
            error_msg = 'Email failed to send to {0}'.format(
                str(notif_req.recipients))
            common.log(msg=error_msg, level=logging.ERROR)
            print error_msg
            #TODO: send error message out

            #put message back on queue in light of failure
            #TODO: should this eventually give up? maybe include counter
            db_con.add_notification(notif_req)
            raise NotificationSendError()

    elif notif_req.when == common.SupportedTimes.REPEAT_DAILY:
        raise NotImplementedError() #TODO
    '''

def process_gmail(db_con, notif_req):
    """Try to send notification via GMail"""
    if notif_req.when == common.SupportedTimes.ONCE_NEXT_BATCH:
        sent = email_sender.GmailSender().send(notif_req)

        if sent:
            status_msg = 'Email succesfully sent to {0}.'.format(
                str(notif_req.recipients))
            common.log(msg=status_msg, level=logging.INFO)
            print status_msg

        if not sent:
            error_msg = 'Email failed to send to {0}'.format(
                str(notif_req.recipients))
            common.log(msg=error_msg, level=logging.ERROR)
            print error_msg
            #TODO: send error message out

            #put message back on queue in light of failure
            #TODO: should this eventually give up? maybe include counter
            db_con.add_notification(notif_req)
            raise NotificationSendError()

    elif notif_req.when == common.SupportedTimes.REPEAT_DAILY:
        raise NotImplementedError() #TODO


if __name__ == '__main__':
    run()
