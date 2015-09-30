#TODO List

- use http://leaverou.github.io/awesomplete/ seed with artist names and works titles, tags
- if q is a synset we need to NOT do fuzzy search
- use word2vec for synonym expansion without adding runtime dependency on it
- filtered OR for similar works (possibly)  
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