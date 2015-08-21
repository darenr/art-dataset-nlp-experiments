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

z = {}

with codecs.open('kadist.json', 'wb', 'utf-8') as out:
  for rownum in xrange(1, sh.nrows):
    d = dict(zip(fieldnames, 
          [clean(x) for x in sh.row_values(rownum)]))
    if d['id'] == 962:
      z = d
      print d['description']
      print type(d['id'])
    data.append(d)
  out.write(json.dumps(data, indent=2, ensure_ascii=False))

print json.dumps(z, indent=2, ensure_ascii=False)
  

