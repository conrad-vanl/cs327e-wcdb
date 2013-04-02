# How to Install Python-MYSQL libraries
This won't install MYSQL on the command line, just the Python libraries.

## On Windows:
http://www.lfd.uci.edu/~gohlke/pythonlibs/#mysql-python

download the .exe for your system (either amd64 for 64-bit or win32 for 32-bit)
install. enjoy

## On Mac:
Not an easy one click install. I found this stackoverflow thread:
http://stackoverflow.com/questions/1448429/how-to-install-mysqldb-python-data-access-library-to-mysql-on-mac-os-x

The highest voted answer loks correct, but the problem is, at the end, he shwos you testing it by trying to "import MySQLdb" but Downing's examples and our code uses "import _mysql"...so not sure if this is installing the right library or not.