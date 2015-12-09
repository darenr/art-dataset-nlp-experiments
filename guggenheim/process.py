import unicodedata
import json
import codecs
import re
from string import punctuation

r = re.compile(r'[{}]+'.format(re.escape(punctuation)))

loc_map = {}

with codecs.open('manual_geotagging.csv', 'rb', 'utf-8') as mtf:
  for line in mtf.readlines():
    parts = line.split('|')
    loc_map[parts[0].strip()] = parts[1].strip()

  
with codecs.open('postwar_unicode_guggenheim.json', 'wb', 'utf-8') as fout:
  results = []
  with codecs.open('unicode_guggenheim.json', 'rb', 'utf-8') as fin:
    guggenheim = json.loads(fin.read())
    for map in guggenheim:
      if 'date' in map: 
        try:
          if int(map['date']) >= 1945: # only keep post war artworks

            if map['description'].startswith('Description\n'):
              map['description'] = map['description'][len('Description\n'):]

            map['description'] = "%s\n\n%s" % (map['description'], map['url'])

            if 'artist_meta_data' in map:
              map['artist_meta_data'] = map['artist_meta_data'].strip()
              x = r.split(map['artist_meta_data'].strip())[-1].strip()
              if x in loc_map:
                map['nationality_code'] = loc_map[x]

            results.append(map)
        except:
          pass
  fout.write(json.dumps(results, indent=2, sort_keys=True, ensure_ascii=False))


        
