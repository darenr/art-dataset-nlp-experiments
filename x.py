

cd = lambda dct, *keys: {key: dct[key] for key in keys}

def copydict(d, *keys):
  ret = {}
  for key in keys:
    if type(d[key]) in [str, unicode]:
      ret[key] = d[key].strip()
    else:
      ret[key] = d[key]
  return ret
    

map = {'key1': 'foo  ', 'key2': 'bar  ', 'key3': 42}


print cd(map, 'key1','key2','key3')
print copydict(map, 'key1','key2','key3')
