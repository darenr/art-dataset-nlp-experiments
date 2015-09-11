from flask import Flask, render_template, request
from elasticsearch import Elasticsearch

app = Flask(__name__)

es = Elasticsearch()

@app.route('/')
def homepage():
  title = "Kadist"

  q = request.args.get('q')

  if q:
    q = q.strip()

    # fuzziness is allowed edit distance (ED), for words that are short we disable it, but for longer words
    # where the chance of a misspelling are increased we ED 2
    fuzziness = "0" if len(q) < 10 else "1"

    search_body = {
      "size": 50,

      "query": {
        "multi_match": {
          "query": q,
          "fuzziness": fuzziness,
          "type": "phrase",
          "fields": ["major_tags^5",
                      "minor_tags^4",
                      "title^3",
                      "artist_name^2",
                      "description",
                      "worktype",
                      "artist_description"
                     ]
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
      },
    }
    if 'term' in search_body['filter']:
      results['filter'] = tuple(search_body['filter']['term'].items()[0])

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
  if len(sys.argv) == 2:
    # if there's a second argument it is assumed to be a valid word vector model
    print "please wait, loading wordvector model ..."
    model = Word2Vec.load_word2vec_format(sys.argv[1])

  sys.exit(-1)  app.run(debug=True, host='0.0.0.0', port=5000, passthrough_errors=True)
