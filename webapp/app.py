from flask import Flask, render_template, request
from elasticsearch import Elasticsearch
import json
import sys

app = Flask(__name__)

es = Elasticsearch()

@app.route('/', methods = ['POST', 'GET'])
def homepage():
  title = "Kadist"

  q = request.args.get('q')
  # print "response object: " + q

  # Multifacet Search
  # checked_options = request.form.getlist('check')
  # checked_facets = request.form.getlist('id')
  # print checked_options, checked_facets


  if q and len(q.strip()):
    q = q.strip()

    # fuzziness is allowed edit distance (ED), for words that are short we disable it, but for longer words
    # where the chance of a misspelling are increased we ED 2

    fuzziness = "0" if len(q) < 10 else "1"

    # for a more-like-this query q will have the form of _<id number>, if we see this
    # pattern we use the alternative query form

    more_like_this = {
      "size": 50,
      "query": {
          "more_like_this": {
              "fields": [
                "mlt_tags"
              ],
              "docs": [
                  {
                      "_index": "kadist",
                      "_type": "kadist_art_collection",
                      "_id": q[1:]
                  }
              ],
              "min_term_freq": 1,
              "percent_terms_to_match": 0,
              "min_doc_freq": 1
          }
      },

      "aggregations": {
        "worktype": {
          "terms": {
            "field": "worktype"
          }
        },
        "year": {
          "terms": {
            "field": "year"
          }
        }
      },

      "filter": {
      }
    }

    search_regular = {
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
                      "artist_description",
                      "id"
                     ]
        }
      },

      "aggregations": {
        "worktype": {
          "terms": {
            "field": "worktype"
          }
        },
        "year": {
          "terms": {
            "field": "year"
          }
        },
        "collection": {
          "terms": {
            "field": "collection"
          }
        }         
      },

      "filter": {
      }
    }


    search_body = more_like_this if q[0] == '_'  else search_regular

    # print search_body

    if request.args.get('filter_field') and request.args.get('filter_value'):
      search_body['filter'] = {
        "term":{
          request.args.get('filter_field'): request.args.get('filter_value')
        }
      }

    #### Multifacet Search
    #if form object "submitted"
    # loop thru the list
    # if request.args.get('filter1') and request.args.get('filter1'):    
    #   search_body['filter'] = {
    #       "and" : [
    #           {
    #               "range" : {
    #                   "postDate" : {
    #                       "from" : "2010-03-01",
    #                       "to" : "2010-04-01"
    #                   }
    #               }
    #           },
    #           {
    #               "prefix" : { "name.second" : "ba" }
    #           }
    #       ]
    #   }



    sr = es.search(index="kadist", body=search_body)

    hits = sr['hits']
    aggs = sr['aggregations']

    results = {
      "count": hits['total'],
      "list_layout": "list" in request.args,
      "hits": [hit['_source'] for hit in hits['hits'] if hit['_source']['description']],
      "facets": {
        "worktype": [x for x in aggs['worktype']['buckets'] if len(x['key'].strip())>0],        
        "year": [x for x in aggs['year']['buckets']],
        "collection": [x for x in aggs['collection']['buckets']]
      },
    }

    print json.dumps([x['title'] for x in results['hits']], indent=True)

    if 'term' in search_body['filter']:
      results['filter'] = tuple(search_body['filter']['term'].items()[0])      


  else:
    results = {
      "count": 0,
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

  app.run(debug=True, host='0.0.0.0', port=5000, passthrough_errors=True)
