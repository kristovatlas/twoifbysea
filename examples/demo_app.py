"""Sends a single notification using a GMail account connecting via HTTP.

Credentials are read from these environment variables:

* TWOIFBYSEA_DEFAULT_GMAIL_USERNAME
* TWOIFBYSEA_DEFAULT_GMAIL_PASSWORD
"""
#Python Standard Library 2.7
import os
import sys
import warnings
import json

#pip modules
import requests

GET_SECRETS_URL = 'http://127.0.0.1:51337/get_app_secrets'

STORE_URL = 'http://127.0.0.1:51337/store?'

NOTIFICATION_URL = ('http://127.0.0.1:51337/notify?channel=email&'
                    'subject=My%20Subject&'
                    'body=This%20Is%20My%20URL-encoded%20message&'
                    'error_channel=email')

DEMO_RECIPIENT = 'bob%40example.com'
DEMO_ERROR_RECIPIENT = 'sad%40example.com'

GITHUB_ISSUES = 'https://github.com/kristovatlas/twoifbysea/issues'

GMAIL_USERNAME_STR = 'gmail_username'
GMAIL_PASSWORD_STR = 'gmail_password'

def _get_notify_url(app_id, app_secret):
    return '{0}&recipient={1}&error_recipient={2}&app_id={3}&app_secret={4}'.format(
        NOTIFICATION_URL, DEMO_RECIPIENT, DEMO_ERROR_RECIPIENT, app_id, app_secret)

def _get_store_url(app_id, app_secret, key, val):
    return '{0}app_id={1}&app_secret={2}&key={3}&value={4}'.format(
        STORE_URL, app_id, app_secret, key, val)

def get_username_pass():
    """Get username and password from env vars"""
    username = os.getenv('TWOIFBYSEA_DEFAULT_GMAIL_USERNAME', None)
    assert username is not None and username != ''
    password = os.getenv('TWOIFBYSEA_DEFAULT_GMAIL_PASSWORD', None)
    assert password is not None and password != ''
    return (username, password)

def _get_resp(url):
    req = None
    try:
        req = requests.get(url)
    except requests.exceptions.ConnectionError:
        print "Web server not availabe. Try starting it with `make start`."
        sys.exit(1)

    if req.status_code != 200:
        print "Web server response is bad. Please report to {0}".format(
            GITHUB_ISSUES)
        sys.exit(1)

    if 'application/json' not in req.headers['content-type']:
        warnings.warn('JSON content type missing')

    return json.loads(req.text)

def get_app_secrets():
    """Fetch app_id and app_secret"""
    resp = _get_resp(GET_SECRETS_URL)
    return (resp['app_id'], resp['app_secret'])

def store_creds(username, password, app_id, app_secret):
    """Store Gmail credentials for notifications"""
    url1 = _get_store_url(app_id, app_secret, GMAIL_USERNAME_STR, username)
    resp1 = _get_resp(url1)
    if resp1['status'] != 'success':
        print "Storage of username failed with error message: {0}".format(
            resp1['message'])
        sys.exit(1)
    url2 = _get_store_url(app_id, app_secret, GMAIL_PASSWORD_STR, password)
    resp2 = _get_resp(url2)
    if resp2['status'] != 'success':
        print "Storage of password failed with error message: {0}".format(
            resp2['message'])
        sys.exit(1)
    assert resp1['status'] == 'success' and resp2['status'] == 'success'

def submit_notif_req(app_id, app_secret):
    url = _get_notify_url(app_id, app_secret)
    resp = _get_resp(url)
    if resp['status'] != 'success':
        print "Reqest for notification failed with error message: {0}".format(
            resp['message'])
        sys.exit(1)

def _main():
    username, password = get_username_pass()
    app_id, app_secret = get_app_secrets()
    print "Acquired app id: {0}".format(app_id)
    store_creds(username, password, app_id, app_secret)
    print "Stored credentials successfully."
    submit_notif_req(app_id, app_secret)
    print "Notification request submitted successfully."

if __name__ == '__main__':
    _main()
