#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3 as db
import json
import sys
import codecs

if len(sys.argv) != 3:
  print 'usage: <sqlite3 db file> <output json file>'
  sys.exit(-1)

def dict_factory(cursor, row):
  d = {}
  for idx, col in enumerate(cursor.description):
    d[col[0]] = row[idx]
  return d

data = []

try:
  con = db.connect(sys.argv[1])
  with con:    
    con.text_factory = lambda x: unicode(x, 'utf-8')
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute("SELECT * FROM kadist_artist")
    for row in cur.fetchall():
      print row

except db.Error, e:
    print "Error %s:" % e.args[0]
    sys.exit(-1)



if data:
  with codecs.open(sys.argv[2], 'wb', 'utf-8') as out:
    out.write(json.dumps(data, indent=2, ensure_ascii=False))


