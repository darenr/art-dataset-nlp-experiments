# -*- coding: utf-8 -*-
import json
import codecs
import sys
import requests

class BaseRequest(object):
    BASE_URL_API = 'https://api.artsy.net/api'

    def __init__(self,
            client_id,
            client_secret,
            grant_type='credentials',
            **kwargs):
        self.xapp_token = self.get_xapp_token(client_id, client_secret).json()
        self.access_token = self.get_access_token(
                client_id, client_secret, grant_type, **kwargs).json()

    def get_xapp_token(self, client_id, client_secret):
        return requests.post('https://api.artsy.net/api/tokens/xapp_token',
                params={
                    'client_id': client_id,
                    'client_secret': client_secret
                })

    def get_access_token(self, client_id, client_secret, grant_type, **kwargs):
        kwargs['client_id'] = client_id
        kwargs['client_secret'] = client_secret
        kwargs['grant_type'] = grant_type
        return requests.post('https://api.artsy.net/oauth2/access_token',
                params=kwargs)

    def new_request(self, method, path, **kwargs):
        url = '%s/%s' % (self.BASE_URL_API, path)
        return requests.request(method, url,
                headers={
                    'X-Xapp-Token': self.xapp_token['token'],
                    # 'X-Access-Token': self.access_token['access_token']
                }, **kwargs)

    def new_raw_request(self, method, url, **kwargs):
        return requests.request(method, url,
                headers={
                    'X-Xapp-Token': self.xapp_token['token'],
                    # 'X-Access-Token': self.access_token['access_token']
                }, **kwargs)

    def get(self, path, **kwargs):
        return self.new_request('GET', path, **kwargs)

    def get_raw(self, path, **kwargs):
        return self.new_raw_request('GET', path, **kwargs)

    def post(self, path, **kwargs):
        return self.new_request('POST', path, **kwargs)

    def put(self, path, **kwargs):
        return self.new_request('PUT', path, **kwargs)

    def delete(self, path, **kwargs):
        return self.new_request('DELETE', path, **kwargs)

class Api(BaseRequest):

    def get_status(self):
        return self.get('status')

    def get_artists(self, id=None, **kwargs):
        return self.get('artists/%s' % (id or ''), params=kwargs)

    def get_artworks(self, id=None, **kwargs):
        return self.get('artworks/%s' % (id or ''), params=kwargs)

    def get_images(self, id, **kwargs):
        return self.get('images/%s' % id)

    def get_editions(self, artwork_id, id=None, **kwargs):
        kwargs['artwork_id'] = artwork_id
        return self.get('editions/%s' % (id or ''), params=kwargs)

    def get_fairs(self, id=None, **kwargs):
        return self.get('fairs/%s' % (id or ''), params=kwargs)

    def get_genes(self, id=None, **kwargs):
        return self.get('genes/%s' % (id or ''), params=kwargs)

    def get_partners(self, id=None, **kwargs):
        return self.get('partners/%s' % (id or ''), params=kwargs)

    def get_user_details(self, id):
        return self.get('user_details/%s' % id)

    def get_users(self, id=None, **kwargs):
        return self.get('users/%s' % (id or ''), params=kwargs)

    def get_collections(self, user_id, id=None, **kwargs):
        kwargs['user_id'] = user_id
        return self.get('collections/%s' % (id or ''), params=kwargs)

    def post_collections(self, user_id, name, **kwargs):
        kwargs['user_id'] = user_id
        kwargs['name'] = name
        return self.post('collections/', data=kwargs)

    def put_collections(self, id, user_id, **kwargs):
        kwargs['user_id'] = user_id
        return self.put('collections/%s' % id, data=kwargs)

    def delete_collections(self, id, user_id, **kwargs):
        kwargs['user_id'] = user_id
        return self.delete('collections/%s' % id, params=kwargs)

    def get_collection_items(self, collection_id, user_id, id=None, **kwargs):
        kwargs['collection_id'] = collection_id
        kwargs['user_id'] = user_id
        return self.get('collection_items/%s' % (id or ''), params=kwargs)

    def post_collection_items(self,
            collection_id, user_id, artwork_id, **kwargs):
        kwargs['collection_id'] = collection_id
        kwargs['user_id'] = user_id
        kwargs['artwork_id'] = artwork_id
        return self.post('collection_items/', data=kwargs)

    def put_collection_items(self, id, collection_id, user_id, **kwargs):
        kwargs['collection_id'] = collection_id
        kwargs['user_id'] = user_id
        return self.put('collection_items/%s' % id, data=kwargs)

    def delete_collection_items(self, id, collection_id, user_id, **kwargs):
        kwargs['collection_id'] = collection_id
        kwargs['user_id'] = user_id
        return self.delete('collection_items/%s' % id, params=kwargs)

    def get_profiles(self, id=None, **kwargs):
        return self.get('profiles/%s' % (id or ''), params=kwargs)

    def search(self, q, **kwargs):
        kwargs['q'] = q
        return self.get('search/', params=kwargs)

    def get_shows(self, id=None, **kwargs):
        return self.get('shows/%s' % (id or ''), params=kwargs)

    def get_current_user(self):
        return self.get('current_user/')

    def get_docs(self, name=None):
        return self.get('docs/%s' % (name or ''))


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
        try:
            r = api.search(artist_name+search_flags).json()
            if r and '_embedded' in r:
              print ' * ', artist_name, '...'
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
