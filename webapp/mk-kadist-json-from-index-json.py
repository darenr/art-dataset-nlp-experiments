#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3 as db
from collections import defaultdict
import json
import sys
import codecs
import re

if len(sys.argv) != 3:
  print 'usage: <index.json> <output json file>'
  sys.exit(-1)


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

def fixupImgurl(img):
  return re.sub(r'\.pdf\.jpg$|\.pct$|\.jpeg$|\.jpg\.jpeg$|\.JPG$|\.png$|\.tiff?$', '.jpg', img).replace('#', '')

with codecs.open(sys.argv[1], 'rb', 'utf-8') as f:

  kadist = json.loads(f.read())

  # artists
  for row in kadist:
    if row["model"] == "kadist.artist":
      artists[row['pk']] = {"name": row["fields"]["name"] }

  # load the major_tags
  for row in kadist:
    if row["model"] == "kadist.majortag":
      major_tags[row["pk"]] = {"name": row["fields"]["name"] }

  # load the major tag to works relationship
  for row in kadist:
    if row["model"] == "kadist.majortaggeditem":
      major_tags_rel[row["fields"]["object_id"]].append(row["fields"]["tag"])

  # load the minor
  for row in kadist:
    if row["model"] == "taggit.tag":
      minor_tags[row["pk"]] = {"name": row["fields"]["name"] }

  # load the minor tag to works relationship
  for row in kadist:
    if row["model"] == "taggit.taggeditem":
      minor_tags_rel[row["fields"]["object_id"]].append(row["fields"]["tag"])


  # load the works
  for row in kadist:
    if row["model"] == "kadist.work":
      id = row['fields']['workid']
      d = { 'id': id }
      d['artist_name'] = artists[row['fields']['creator']]['name']
      d['artist_description'] = row['fields']['artistdescription']
      d['description'] = row['fields']['description']
      d['imgurl'] = fixupImgurl(row['fields']['imgurl'])
      d['worktype'] = row['fields']['worktype']
      d['year'] = row['fields']['year']
      d['title'] = row['fields']['title']

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



