# in a terminal, just run python TestQueries.py

import _mysql

MYSQL_CONNECT = { 
  "host"   : "cs327ewcdb.cz0aokgawzgn.us-east-1.rds.amazonaws.com", #"z",
  "user"   : "cs327ewcdb", #"<username>",
  "passwd" : "grouppassword", #"<password>",
  "db"     : "cs327ewcdb" #"downing_test"
}

_c = _mysql.connect(**MYSQL_CONNECT)

print(_c.query(open("WCDB3q.sql").read()))
