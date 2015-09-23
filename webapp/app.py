from flask import Flask, render_template, request, Markup
from elasticsearch import Elasticsearch
import urllib3
import sys

urllib3.disable_warnings()

app = Flask(__name__)

es = Elasticsearch(['https://tcw4l779:9xy6x6d2vg9u6f83@dogwood-2734599.us-east-1.bonsai.io'])

@app.route('/', methods=["GET", "POST"])
def homepage():  

  title = "Kadist"

  q = request.args.get('q')

  if q and len(q.strip()):
    
    q = q.strip()

    # fuzziness is allowed edit distance (ED), for words that are short we disable it, but for longer words
    # where the chance of a misspelling are increased we ED 2

    fuzziness = "0" if len(q) < 10 else "1"

    qry_aggs =  {
      "worktype": {
        "terms": {
          "field": "worktype",
        },
      },
      "collection": {
        "terms": {
          "field": "collection",
        }
      },
      "decade": {
        "terms": {
          "field": "decade",
        }
      }
      ,
      "artist_name": {
        "terms": {
          "field": "artist_name",
        }
      }
    }

    qry_highlight = {
      "pre_tags" : ["<em>"],
      "post_tags" : ["</em>"],
      "fields" : {
          "description" : {},
          "artist_description" : {},
          "title" : {}
        }
    }

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
      "highlight" : qry_highlight,
      "aggregations": qry_aggs,
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
      "highlight" : qry_highlight,
      "aggregations": qry_aggs,
      "filter": {
      }
    }

    search_body = more_like_this if q[0] == '_'  else search_regular

    if request.args.get('filter_field') and request.args.get('filter_value'):
      search_body['filter'] = {
        "term":{
          request.args.get('filter_field'): request.args.get('filter_value')
        }
      }   

    # TODO: use list comprehension
    if request.method == 'POST':      
      formData = request.values

      term = {}
      for filter_field in [key for key in formData.keys() if key != 'q']:
        filter_value = []
        for value in formData.getlist(filter_field):
          filter_value.append(value)    
        term[filter_field] = filter_value
      search_body['filter'] = { "and": [ { "terms": term } ] }



    sr = es.search(index="kadist", body=search_body)

    hits = sr['hits']
    aggs = sr['aggregations']

    # copy the highlighter results over the regular ones (when present)
    for hit in hits['hits']:
      if 'highlight' in hit:
        if 'description' in hit['highlight']:
          hit['_source']['description'] = Markup(hit['highlight']['description'][0])
        if 'artist_description' in hit['highlight']:
          hit['_source']['artist_description'] = Markup(hit['highlight']['artist_description'][0])
        if 'title' in hit['highlight']:
          hit['_source']['title'] = Markup(hit['highlight']['title'][0])


    results = {
      "count": hits['total'],
      "took": sr['took']/1000.0,
      "hits": [hit['_source'] for hit in hits['hits'] if hit['_source']['description']],
      "facets": {
        "worktype": [x for x in aggs['worktype']['buckets'] if len(x['key'])>1],
        "collection": [x for x in aggs['collection']['buckets'] if len(x['key'])>1],
        "decade": [x for x in aggs['decade']['buckets'] if len(x['key'])>1],
        "artist_name": [x for x in aggs['artist_name']['buckets'] if len(x['key'])>1]
      },
    }

    if 'term' in search_body['filter']:
      results['filter'] = tuple(search_body['filter']['term'].items()[0])


  else:
    results = {
      "count": 0,
    }

  # print results

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
