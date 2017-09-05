"""Classes that attempt to send notifications via Telegram

As of March 2017, these notifications are NOT encrypted:
http://stackoverflow.com/questions/32093188/telegram-bots-secret-chats-possible

Requirements: You must register a Telegram bot and get its token. You can do
this by messaging https://telegram.me/botfather through the Telegram app and
using the /newbot command. More details here: https://core.telegram.org/bots

Once you acquire a bot token, you can store that in this environment variable:

Environment variables:
* TWOIFBYSEA_DEFAULT_TELEGRAM_TOKEN

You must also open a chat with your new bot from the account that you wish to
receive notifications.

Usage:

    >>> ts = telegram_sender.TelegramSender()
    >>> notif_req = common.NotificationRequest()
    >>> notif_req.set_channel(common.SupportedChannels.TELEGRAM)
    >>> notif_req.add_recipient('mytelegramusername')
    >>> notif_req.set_message('Test telegram message')
    >>> ts.send(notif_req)

Todos
* Consider merging with email_sender module to make 'sender' module
"""

#Python Standard Library 2.7
import logging
import json
from copy import deepcopy
import os
import sys
import urllib

#pip modules
import requests

#twoifbysea modules
import config
import common

BASE_URL = 'https://api.telegram.org/bot'
GET_ME_PATH = '/getMe'
SEND_MESSAGE_PATH = '/sendMessage'
GET_UPDATES_PATH = '/getUpdates'

class TelegramChatNotFoundError(Exception):
    """Unable to find a matching Telegram chat"""
    pass

class TelegramSecretSender(object):
    """TODO

    https://github.com/vysheng/tg
    """

class TelegramBotSender(object):
    """Send Telegram message via bot account."""

    def __init__(self, token=None):
        if token is None:
            token = config.get_value('telegram_token')
            assert token is not None
            self.token = token
        status_url = get_status_url(token)
        resp = get_response(status_url)
        if not resp['ok']:
            pass #TODO raise error?

    def send(self, notif_req):
        """Send notification via Telegram

        Returns: bool: Whether notification was sent
        """
        assert len(notif_req.recipients) == 1
        recipient = deepcopy(notif_req.recipients).pop()
        assert isinstance(recipient, str)

        chat_id = None
        try:
            chat_id = find_chat_id(token=self.token, telegram_username=recipient)
        except TelegramChatNotFoundError:
            raise TelegramChatNotFoundError(
                ('Could not find matching Telegram chat. Have you messaged the '
                 'bot? Have you deleted your chat with the bot?'))
        if chat_id is not None:
            send_url = get_message_url(
                token=self.token, chat_id=chat_id,
                message=notif_req.message)
            resp = get_response(send_url)
            print "DEBUG: %s" % str(resp)

def get_response(url):
    """Make GET request to specified url and return JSON response"""
    req = requests.get(url)
    if req.status_code != 200:
        msg = 'Received status code {0} for fetching url {1}: {2}'.format(
            req.status_code, url, req.text)
        common.log(msg=msg, level=logging.ERROR)
        #TODO: raise error?
        sys.exit(1)
    else:
        return json.loads(req.text)

def find_chat_id(token, telegram_username):
    """Look through our bot's updates to find first chat_id matching username

    Raises: TelegramChatNotFoundError
    """
    resp = get_response(get_update_url(token))
    print "DEBUG: find_chat_id: %s" % str(resp)
    assert resp['ok']
    for result in resp['result']:
        if 'message' in result and 'chat' in result['message']:
            username = result['message']['chat']['username']
            if username == telegram_username:
                chat_id = result['message']['chat']['id']
                return chat_id

    raise TelegramChatNotFoundError()

def get_status_url(token):
    assert isinstance(token, str)
    return ''.join([BASE_URL, token, GET_ME_PATH])

def get_update_url(token):
    assert isinstance(token, str)
    return ''.join([BASE_URL, token, GET_UPDATES_PATH])

def get_message_url(token, chat_id, message):
    assert isinstance(token, str)
    assert isinstance(chat_id, int)
    assert isinstance(message, str)
    url = ''.join([BASE_URL, token, SEND_MESSAGE_PATH, '?'])
    url = ''.join([url, '&chat_id=', urllib.quote(str(chat_id))])
    url = ''.join([url, '&text=', urllib.quote(message)])
    return url

if __name__ == '__main__':
    print "DEBUG"
    ts = TelegramSender()
    notif_req = common.NotificationRequest()
    notif_req.set_channel(common.SupportedChannels.TELEGRAM)
    notif_req.add_recipient('kristovatlas')
    notif_req.set_message('Test telegram message')
    ts.send(notif_req)
