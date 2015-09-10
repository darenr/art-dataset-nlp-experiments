curl -XPOST "http://localhost:9200/kadist/kadist_art_collection/_search" -d '
{
  "size": 2,
  "query": {
    "multi_match" : {
      "query" : "war",
      "type": "cross_fields",
      "fields" : [ "title^3", "description", "artist_name", "worktype" ]
    }
  },
  "filter": {
    "term": {
      "worktype": "photograph"
    }
  }
}
'
