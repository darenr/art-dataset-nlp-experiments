# -*- coding: utf-8 -*-
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
