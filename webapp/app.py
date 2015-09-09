from flask import Flask, render_template, request
from datetime import datetime
from elasticsearch import Elasticsearch

app = Flask(__name__)

es = Elasticsearch()

@app.route('/')
def homepage():
  title = "Kadist"

  q = request.args.get('q')



  if q:
    q = q.strip()

    search_body = {
      "size": 50,

      "query": {
        "multi_match": {
          "query": q,
          "fields": ["major_tags^5", "minor_tags^4", "title^3", "artist_name^2", "description", "worktype"]
        }
      },

      "aggregations": {
        "worktype": {
          "terms": {
            "field": "worktype"
          }
        }
      },

      "filter": {

      }
    }

    if request.args.get('filter_field') and request.args.get('filter_value'):
      search_body['filter'] = {
        "term":{
          request.args.get('filter_field'): request.args.get('filter_value')
        }
      }

    sr = es.search(index="kadist", body=search_body)

    hits = sr['hits']
    aggs = sr['aggregations']

    results = {
      "count": hits['total'],
      "hits": [hit['_source'] for hit in hits['hits'] if hit['_source']['description']],
      "hidden": len([hit for hit in hits['hits'] if not hit['_source']['description']]),
      "facets": {
        "worktype": aggs['worktype']['buckets']
      }
    }
  else:
    results = {
      "count": 0,
      "hidden": 0,
      "hits": None
    }

  print results['count']

  try:
    return render_template("index.html",
                           q=q,
                           title=title,
                           results=results)
  except Exception, e:
    return str(e)


if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0', port=5000, passthrough_errors=True)
