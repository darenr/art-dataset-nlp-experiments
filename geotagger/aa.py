import csv

with open('x') as f:
  for row in csv.reader(f, quotechar="'"):
    print "%s:%s," % (row[1], row[0])
