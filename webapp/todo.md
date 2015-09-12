#TODO List

- use http://bartaz.github.io/sandbox.js/jquery.highlight.html when q is not None on all text fields
- move the search bar into the nav bar
- add artist name as a facet (and other categorical types)
- add major/minor tags to app DONE
- organize the year/media type etc better DONE
- try on other browsers
- add one facet to search DONE
- if q is a synset we need to NOT do fuzzy search
- "taboo" only matches 2 works, word2vec should expand this to include the gay/lesbian works too,
  an example of their power of expansion
- change tag fields to not_analyzed so they aren't full text searchable (mappings) DONE
- term expansion: for every major/minor tag create es synonyms, then weight them in main query
- change layout to image-first pinterest like responsive layout
- import imdb as a collection
- figure out more-like-this query on tags only 
- better than MLT is to use disjunctive filtered OR
  
  {
    "query": {
      "filtered": {
        "filter": {
          "or": [ {
            "script": {
              "script": "_index['mlt_tags']['warn01'].tf() >= 1"
            }
             },
                 {
            "script": {
              "script": "_index['mlt_tags']['violencen01'].tf() >= 1"
            }
             }
           ]
        }
      }
    }
  }
  
  requires change to elasticsearch.yml
  
  script.inline: on
  script.indexed: on
