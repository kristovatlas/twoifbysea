# twoifbysea
send notifications about events with ease

## About

twoifbysea is a server that receives messaging requests from clients. The goals for the project are:
* Rapid development for clients, abstracting the annoying details of messaging away
* Supporting a variety of messaging channels

## Installation

To install PyPI dependencies, run:

    $ pip install -r /path/to/twoifbysea/requirements.txt

### Troubleshooting pycrypto installation

If you see an error message such as:

```
blake2/blake2module.c:1:20: fatal error: Python.h: No such file or directory

 #include <Python.h>

                    ^

compilation terminated.

error: command 'x86_64-linux-gnu-gcc' failed with exit status 1

----------------------------------------
Cleaning up...
Command /usr/bin/python -c "import setuptools,
tokenize;__file__='/tmp/pip-build-Br8maE/blake2/setup.py';exec(compile(getattr(tokenize,
'open', open)(__file__).read().replace('\r\n', '\n'), __file__,
'exec'))" install --record /tmp/pip-EL6ID6-record/install-record.txt
--single-version-externally-managed --compile failed with error code 1
in /tmp/pip-build-Br8maE/blake2
```

This may indicate that you are lacking important source code files for Python-based development. This can be rectified for some Linux distributions by running:

    $ apt-get update && apt-get install python-dev

## Usage

Clients must connect to the server using a supported connection mechanism; currently, only HTTP is supported. (Please create a [GitHub issue](https://github.com/kristovatlas/twoifbysea/issues) to request additional connectors.) Once started, the server can then service client requests to send notifications. The notification script must be scheduled as a cron job to clear the queue.

### Starting the webserver

Currently the only connector available for the server is via HTTP. The webserver that receives and processes notification requests can be started as follows:

    $ cd /path/to/twoifbysea/master ; make start

### Scheduling the notification daemon

Notification requests by clients are added to a queue and will be sent when the `notify.py` script is run. To regularly empty the queue, this script should be run as a cron job. The `notify.py` script takes no arguments and will find the queue database file on its own using the `appdir` Python module.

Ex.:

Send queued notifications every 5 minutes:
```
5 * * * * /path/to/twoifbysea/master/twoifbysea/notify.py
```

### Client examples

See the [examples/](examples/) directory for general and Python-specific examples of connecting to the notification server.

### Logs

Check the `twoifbysea.log` file for error messages, such as those concerning missing environment variables for notification credentials. The location of this log file is determined by the (`appdirs`)[https://pypi.python.org/pypi/appdirs/1.4.3] Python module:

MacOS:
    ~/Library/Application Support/twoifbysea/twoifbysea.log

Windows (non-roaming profiles):
    C:\Documents and Settings\<User>\Application Data\Local Settings\atlas\twoifbysea\twoifbysea.log

Windows (roaming profiles):
    C:\Documents and Settings\<User>\Application Data\atlas\twoifbysea\twoifbysea.log

Linux:
    ~/.local/share/twoifbysea/twoifbysea.log

### Project cleaning

To delete the notification database (primarily for development purposes), use:

    $ cd /path/to/twoifbysea/master/twoifbysea ; make clean

## Supported communication channels

* Email (unencrypted, GMail only)
* Telegram bot (unencrypted)

## Important TODOs

* Add support for daily digest messages
* Add negative notifications (e.g. "no new messages for app-x today, all is good")
* Allow Python clients to initiate delivery of some or all types of messages without running a listening server
* Implement generic email accounts apart from GMail (need to figure out some spam filtering stuff)
* Add new communication channels, such as PGP-encrypted emails, Slack channels, etc.
* Refactor to minimize client footprint
* Create packaged installer for server
