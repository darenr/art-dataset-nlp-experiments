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
          "match": {
            "_all": q
          }
        },
        "aggregations": {
           "worktype_facet": {
              "terms": {
                 "field": "worktype"
              }
           },
           "year_facet": {
              "terms": {
                 "field": "year"
              }
           },
           "major_facet": {
              "terms": {
                 "field": "major_tags"
              }
           },
           "minor_facet": {
              "terms": {
                 "field": "minor_tags"
              }
           }
        }
      }
      sr = es.search(index="kadist", body=search_body)
      
      hits = sr['hits']
      aggs = sr['aggregations']
      
      results= {
        "count": hits['total'],
        "hits": [hit['_source'] for hit in hits['hits'] if hit['_source']['description']],
        "hidden": len([hit for hit in hits['hits'] if not hit['_source']['description']]),
        "facets": {
          "year_facet": aggs['year_facet']['buckets'],
          "worktype_facet": aggs['worktype_facet']['buckets']
        }
      }
    else:
      results = {
        "count": 0,
        "hidden": 0,
        "hits" : None
      }

    print results['count']

    try:
        return render_template("index.html", 
          q = q,
          title = title, 
          results=results)
    except Exception, e:
        return str(e)

if __name__ == "__main__":
  app.run(debug = True, host='0.0.0.0', port=5000, passthrough_errors=True)
