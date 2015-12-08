import unicodedata
import json
import codecs

with codecs.open('unicode_guggenheim.json', 'wb', 'utf-8') as fout:
    results = []
    with codecs.open('guggenheim.json', 'rb', 'utf-8') as fin:
        guggenheim = json.loads(fin.read())
        for map_in in guggenheim:
            map_out = {}
            for key in map_in:
                v = map_in[key]
                if isinstance(v, list):
                    map_out[key] = [unicodedata.normalize('NFKD', x).encode('ascii','ignore') for x in v]
                else:
                    map_out[key] = unicodedata.normalize('NFKD', v).encode('ascii','ignore')
            results.append(map_out)
    fout.write(json.dumps(results, indent=2, sort_keys=True, ensure_ascii=False))
