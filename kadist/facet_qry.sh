curl -XPOST "http://localhost:9200/kadist/kadist_art_collection/_search?q=war" -d '
{
   "size": 0,
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
'
