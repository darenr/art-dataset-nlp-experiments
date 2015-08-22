import re
import sys
import codecs
import json

## INSERT INTO "kadist_majortag" VALUES(1,'conceptual','conceptual');

results = {}

if len(sys.argv) != 3:
  print "usage: <sql dump file>, <output json>"
  sys.exit(-1)

with codecs.open(sys.argv[1], 'rb', 'utf-8') as f:
  for line in f:
    m = re.match("INSERT INTO \"kadist_majortag\" VALUES\((\d+),\'(.*[^'])\',\'(.*[^'])\'.*$", line)
    if m:
      results[int(m.group(1))] = {'name': m.group(2), 'slug': m.group(3)}

with codecs.open(sys.argv[2], 'wb', 'utf-8') as out:
  out.write(json.dumps(results, indent=2, ensure_ascii=False))


