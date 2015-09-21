#TODO List

- use http://leaverou.github.io/awesomplete/ seed with artist names and works titles
- add artist name as a facet (and other categorical types)
- try on other browsers
- if q is a synset we need to NOT do fuzzy search
- "taboo" only matches 2 works, word2vec should expand this to include the gay/lesbian works too,
  an example of their power of expansion
- term expansion: for every major/minor tag create es synonyms, then weight them in main query
- figure out more-like-this query on tags only 
- better than MLT is to use disjunctive filtered OR
- 
  ```
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
  ```
  
  requires change to elasticsearch.yml
  
  ```
  script.inline: on
  script.indexed: on
  ```
- alternative, pre-compute tag hypernyms and store in results, then query becomes an 
  OR of the current work's tag's hypernyms. Eg. if this work has the tag "war.n.01" the hypernym
  Synset('military_action.n.01') is common to:
  [Synset('amphibious_landing.n.01'), 
   Synset('battle.n.01'), 
   Synset('blockade.n.01'), 
   Synset('defense.n.01'), 
   Synset('electronic_warfare.n.01'), 
   Synset('police_action.n.01'), 
   Synset('resistance.n.04'), 
   Synset('saber_rattling.n.01'), 
   Synset('sortie.n.01'), 
   Synset('war.n.01')]
   
   hence a work that is tagged with battle.n.01 will also match the search. When multiple tags are 
   involved, the query becomes an OR to bias towards the most matching. This is a filter query, so 
   relevance can be superimposed on top if required.
   
  
  ```
  {
    "filtered" : {
        "query" : {
        "filter" : {
            "or" : [
                {
                    "term" : { "hypernym" : "amphibious_landing.n.01" }
                },
                ...
            ]
        }
    }
}
```