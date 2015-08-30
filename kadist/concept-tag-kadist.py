# -*- encoding: utf-8 -*-
import base64
import json
import os
import sys
import codecs
from alchemyapi.alchemyapi import AlchemyAPI

alchemyapi = AlchemyAPI()

if len(sys.argv) != 2:
  print "usage: <kadist corpus json>"
  sys.exit(-1)

def load_json():
  with codecs.open(sys.argv[1], 'rb', 'utf-8') as f:
    data = json.loads(f.read())
    return data

def save_json(data):
  with codecs.open(sys.argv[1], 'wb', 'utf-8') as f:
    f.write(json.dumps(data, indent=2, ensure_ascii=False))

def get_tags(txt):
  concepts = alchemyapi.concepts('text', txt)
  if concepts['status'] == 'OK':
    tags = []
    for tag in concepts['concepts']:
      tags.append(tag['text'])
    return tags
  else:
    print concepts
    return None

j = load_json()

for row in j:
  if not 'alchemy_tags' in row:
    row['alchemy_tags'] = []
  if row['major_tags'] and row['worktype'] and row['description'] and row['imgurl']:
    if len(row['alchemy_tags']) == 0:
      tags = get_tags(row['description'])
      print tags
      if tags:
        row['alchemy_tags'] = tags

save_json(j)
