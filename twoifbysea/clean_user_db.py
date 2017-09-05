"""A script that deletes the user database file, useful for debugging only."""
#Standard Python Library 2.7
import os

#twoifbysea modules
import common #common.py
import datastore #datastore.py

db_file_path = common.get_app_file_loc(datastore.DB_FILENAME_DEFAULT)
try:
    os.remove(db_file_path)
except OSError:
    pass
