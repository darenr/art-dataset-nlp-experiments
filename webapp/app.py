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
      sr = es.search(index="kadist", body={"query": {"match": {"_all": q}}})['hits']
      results= {
        "count": sr['total'],
        "hits": [hit['_source'] for hit in sr['hits'] if hit['_source']['description']],
        "hidden": len([hit for hit in sr['hits'] if not hit['_source']['description']])
      }
    else:
      results = {
        "count": 0,
        "hidden": 0,
        "hits" : None
      }

    print results

    try:
        return render_template("index.html", 
          q = q,
          title = title, 
          results=results)
    except Exception, e:
        return str(e)

if __name__ == "__main__":
  app.run(debug = True, host='0.0.0.0', port=5000, passthrough_errors=True)
