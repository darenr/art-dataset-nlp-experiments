import unicodedata
import json
import codecs

with codecs.open('postwar_unicode_guggenheim.json', 'wb', 'utf-8') as fout:
    results = []
    with codecs.open('unicode_guggenheim.json', 'rb', 'utf-8') as fin:
        guggenheim = json.loads(fin.read())
        for map in guggenheim:
          if 'date' in map: 
            try:
              if int(map['date']) >= 1945:
                d =map['description']
                if d.startswith('\nDescription\n'):
                  map['description'] = map['description'][len('\nDescription\n'):]
                results.append(map)
            except:
              pass
    fout.write(json.dumps(results, indent=2, sort_keys=True, ensure_ascii=False))
