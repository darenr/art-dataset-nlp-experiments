from artsy import Api
import json

client_name = 'kadist'
client_id = '696566944f21d2c417fc'
client_secret = '24f623232bf8d9dad5780951c4bf58a5' 
   

if __name__ == "__main__":
  api = Api(client_id, client_secret)
  r = api.get_artists().json()
  print json.dumps(r, indent=2, sort_keys=True, ensure_ascii=False)
