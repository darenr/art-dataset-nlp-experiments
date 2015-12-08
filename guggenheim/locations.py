import unicodedata
import json
import codecs
import re
from string import punctuation

with codecs.open('postwar_unicode_guggenheim.json', 'wb', 'utf-8') as fout:
    results = []
    r = re.compile(r'[{}]+'.format(re.escape(punctuation)))
    with codecs.open('unicode_guggenheim.json', 'rb', 'utf-8') as fin:
        guggenheim = json.loads(fin.read())
        for map in guggenheim:
          if 'date' in map: 
            try:
              if int(map['date']) >= 1945:
                x = r.split(map['artist_meta_data'].strip())[-1]
                
                print x
            except:
              pass
    fout.write(json.dumps(results, indent=2, sort_keys=True, ensure_ascii=False))
