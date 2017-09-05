Programming reference

* [https://www.python.org/dev/peps/pep-0328/](Relative imports in Python)
* [https://en.wikipedia.org/wiki/List_of_HTTP_status_codes](HTTP status codes)
* [http://flask.pocoo.org/snippets/88/](Job queue implemented using SQLite)
* [http://stackoverflow.com/questions/1679384/converting-python-dictionary-to-list#1679395](dict to list)
* [http://stackoverflow.com/questions/16566069/url-decode-utf-8-in-python#16566128](URL decoding in Python)
* [https://www.sqlite.org/datatype3.html](Sqlite3 data types)
* [https://developers.google.com/protocol-buffers/docs/proto3](Protobuf documentation)
* [http://docs.python-guide.org/en/latest/writing/structure/](Structuring Your Project)
* [http://stackoverflow.com/questions/2104080/how-to-check-file-size-in-python](Get size of file)
* [https://github.com/kristovatlas/gfyp/blob/54aaf90069e45c606b88bfe49e2c3140782d6d0a/gfyp_db.py](Some db code from here)
* [https://pypi.python.org/pypi/pycrypto](pycrypto for AES)
* [http://search.cpan.org/~lds/Crypt-CBC-2.24/CBC.pm#Padding_methods](perl Crypt-CBC and padding)
* [https://waymoot.org/home/python_string/](efficient string concatenation)
* [https://en.wikipedia.org/wiki/BLAKE_%28hash_function%29](Notes on BLAKE2)
* [https://github.com/darjeeling/python-blake2](blake2 from pip docs/source code)

Programming bugs
* [http://stackoverflow.com/questions/24708741/attributeerror-builtin-function-or-method-object-has-no-attribute-replace#24708743](AttributeError: 'builtin_function_or_method' object has no attribute 'replace')
* [http://stackoverflow.com/questions/1945920/why-doesnt-os-path-join-work-in-this-case#1945930](Gotchas for os.path.join)

How not to check if a file is writeable:

```
f = open(filename, 'w')
f.close() #zeroes out the contents of the file
```

[http://stackoverflow.com/questions/2113427/determining-whether-a-directory-is-writeable#2113511](How to do it correctly):
```
os.access('/path/to/folder', os.W_OK) # W_OK is for writing, R_OK for reading, etc.
```
