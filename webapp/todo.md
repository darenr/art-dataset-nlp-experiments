#TODO List

- add to welcome screen some example searches
- use http://leaverou.github.io/awesomplete/ seed with artist names and works titles, tags
- load other datasets or federate
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

- for similarity measure that's computed using an external to es algorithm the result should be a list of ids which
are then submitted to es for consistency using the ids query type

```
{
    "filtered" : {
        "filter" : {
          {
              "ids" : {
                  "values" : ["1", "4", "100"]
              }
          }
        }
    }
}
```