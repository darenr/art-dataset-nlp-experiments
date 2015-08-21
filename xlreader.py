# -*- encoding: utf-8 -*-
import xlrd
import json
import csv
import sys
import codecs

wb = xlrd.open_workbook(sys.argv[1])
sh = wb.sheet_by_name(sys.argv[2])

fieldnames = sh.row_values(0)

data = []

def clean(v):
  if type(v) is str:
    return unicode(v, "utf-8").strip().replace(u'—', ' ').replace('\n', ' ')
  else:
    if type(v) is float and v == int(v):
      v = int(v)
    return v

tagged = []
descriptions = []
for rownum in xrange(1, sh.nrows):
  d = dict(zip(fieldnames, [clean(x) for x in sh.row_values(rownum)]))
  data.append(d)
  if d['tags']:
    d['tags'] = d['tags'].split(',')  
  if d['major_tags']:
    d['major_tags'] = d['major_tags'].split(',')  
    tagged.append(d)
  if d['description']:
    descriptions.append(d['description'])

with codecs.open('kadist.json', 'wb', 'utf-8') as out:
  out.write(json.dumps(data, indent=2, ensure_ascii=False))

with codecs.open('kadist-tagged.json', 'wb', 'utf-8') as out:
  out.write(json.dumps(tagged, indent=2, ensure_ascii=False))

with codecs.open('kadist_descriptions.txt', 'wb', 'utf-8') as out:
  for desc in descriptions:
    out.write(desc + '\n')
