#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3 as db
from collections import defaultdict
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
    out.write(json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False))

def copydict(d, *keys):
  ret = {}
  for key in keys:
    if type(d[key]) in [str, unicode]:
      ret[key] = d[key].strip()
    else:
      ret[key] = d[key]
  return ret


artists = {} # keyed by artist ID
major_tags = {} # keyed on tag ID
major_tags_rel = defaultdict(list) # keyed by work ID
minor_tags = {} # keyed on tag ID
minor_tags_rel = defaultdict(list) # keyed by work ID
works = []

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
      major_tags[row['id']] = copydict(row, 'name')

    # load the major tag to works relationship
    cur.execute("SELECT * FROM kadist_majortaggeditem")
    for row in cur.fetchall():
      major_tags_rel[row['object_id']].append(row['tag_id'])

    # load the minor_tags
    cur.execute("SELECT * FROM taggit_tag")
    for row in cur.fetchall():
      minor_tags[row['id']] = copydict(row, 'name')

    # load the minor tag to works relationship
    cur.execute("SELECT * FROM taggit_taggeditem")
    for row in cur.fetchall():
      minor_tags_rel[row['object_id']].append(row['tag_id'])

    # load the works
    cur.execute("SELECT * FROM kadist_work")
    for row in cur.fetchall():
      id = row['id']
      d = copydict(row, 'id', 'title', 'year', 'imgurl', 'worktype', 'technique', 'dimensions', 'description')
      # resolve artist details
      if row['creator_id'] and row['creator_id'] in artists:
        d['artist_name'] = artists[row['creator_id']]['name']
        d['artist_description'] = artists[row['creator_id']]['description']

      # resolve major_tags
      d['major_tags'] = []
      if id in major_tags_rel:
        for tag in major_tags_rel[id]:
          if tag in major_tags:
            d['major_tags'].append(major_tags[tag]['name'])

      # resolve minor
      d['minor_tags'] = []
      if id in minor_tags_rel:
        for tag in minor_tags_rel[id]:
          if tag in minor_tags:
            d['minor_tags'].append(minor_tags[tag]['name'])

      works.append(d)

    save_json(works)

except db.Error, e:
    print "Error %s:" % e.args[0]
    sys.exit(-1)




