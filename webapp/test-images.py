import json
import sys
import codecs
import requests


def test_images(filename):
  with codecs.open(filename, 'rb', 'utf-8') as f:
    kadist = json.loads(f.read())
    for m in kadist:
      if 'imgurl' in m and m['imgurl']:
        r = requests.get(m['imgurl'])
        if r.status_code != 200:
          print(m['imgurl'], r.status_code)



if len(sys.argv) != 2:
  print 'usage: <kadist.json>'
  sys.exit(-1)
else:
  test_images(filename=sys.argv[1])
