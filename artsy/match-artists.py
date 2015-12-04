from artsy import Api
import json
import codecs
import sys

client_name = 'kadist'
client_id = '696566944f21d2c417fc'
client_secret = '24f623232bf8d9dad5780951c4bf58a5'

bio_keys = ['nationality','location','hometown','gender','birthday']
gene_keys = ['name', 'description']

if __name__ == "__main__":
  api = Api(client_id, client_secret)

  with codecs.open('data/kadist.json', 'rb', 'utf-8') as f:
    works = json.loads(f.read())
    artists = list(set([m['artist_name'] for m in works]))
    print len(artists), 'artists'

    with codecs.open('data/artsy.json', 'wb', 'utf-8') as out:
      results = []
      search_flags = ' more:pagemap:metatags-og_type:artist'
      for artist_name in artists:
        print ' * ', artist_name, '...'
        try:
            r = api.search(artist_name+search_flags).json()
            if r and '_embedded' in r:
              artsy_id = r['_embedded']['results'][0]['_links']['self']['href'].rsplit('/',1)[1]
              a = api.get_artists(artsy_id).json()
              bio = { k: a[k] for k in bio_keys if k in a}

              genes = []
              similar = []

              if a and '_links' in a:
                try:
                  if 'genes' in a['_links']:
                    g = api.get_raw(a['_links']['genes']['href']).json()
                    if g and '_embedded' in g:
                      for gene in g['_embedded']['genes']:
                        genes.append({ k: gene[k] for k in gene_keys if k in gene})
                except:
                  pass

                try:
                  if 'similar_contemporary_artists' in a['_links']:
                    s = api.get_raw(a['_links']['similar_contemporary_artists']['href']).json()
                    if '_embedded' in s:
                      similar = [x['name'] for x in s['_embedded']['artists']]
                except:
                  pass

              results.append({
                'artist_name': artist_name,
                'bio': bio,
                'genes': genes,
                'similar': similar,
              })
        except Exception, e:
          print 'happily ignoring', e
      print len(results), 'artists matched'
      out.write(json.dumps(results, indent=2, sort_keys=True, ensure_ascii=False))
