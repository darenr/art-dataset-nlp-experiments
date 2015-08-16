# -*- encoding: utf-8 -*-
import xlrd
import csv
import sys
import codecs


wb = xlrd.open_workbook(sys.argv[1])
sh = wb.sheet_by_name(sys.argv[2])

fieldnames = sh.row_values(0)

with codecs.open('kadist_descriptions.txt', 'wb', 'utf-8') as out:
  for rownum in xrange(1, sh.nrows):
    row = dict(zip(fieldnames, sh.row_values(rownum)))
    if 'description' in row and row['description']:
      desc = row['description'].strip().replace(u'—', ' ').replace('\n', ' ').encode('ascii', 'ignore')
      if desc:
        out.write(desc + '\n')
   

