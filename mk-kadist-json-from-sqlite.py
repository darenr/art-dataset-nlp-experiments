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

def save_json(data):
  with codecs.open(sys.argv[2], 'wb', 'utf-8') as out:
    out.write(json.dumps(data, indent=2, ensure_ascii=False))

copydict = lambda dct, *keys: {key: dct[key] for key in keys}


artists = {}
minor_tags = {}
major_tags = {}
works = {}

try:
  con = db.connect(sys.argv[1])
  with con:    
    con.text_factory = lambda x: unicode(x, 'utf-8')
    con.row_factory = dict_factory
    cur = con.cursor()

    # load the artists
    cur.execute("SELECT * FROM kadist_artist")
    for row in cur.fetchall():
      artists[row['id']] = copydict(row, 'name', 'description')

    # load the major_tags
    cur.execute("SELECT * FROM kadist_majortag")
    for row in cur.fetchall():
      major_tags[row['id']] = {'name': row['name']}

    # load the minor_tags
    cur.execute("SELECT * FROM taggit_tag")
    for row in cur.fetchall():
      minor_tags[row['id']] = {'name': row['name']}

    # load the works
    cur.execute("SELECT * FROM kadist_work")
    for row in cur.fetchall():
      d = copydict(row, 'title', 'year', 'imgurl', 'worktype', 'technique', 'dimensions', 'description')
      # resolve artist details
      if row['creator_id'] and row['creator_id'] in artists:
        d['artist'] = artists[row['creator_id']]
      # resolve major_tags

      works[row['id']] = d

    save_json(works)

except db.Error, e:
    print "Error %s:" % e.args[0]
    sys.exit(-1)




