#Kadist
##Engineering Plan

######Daren Race, 8/26/15

#Introduction
After an initial investigation into the current processes and goals for the Collection Index project this document attempts to set out a plan to meet those goals and improve the existing processes to be more repeatable and reliable.

#Goals
The Kadist collection strives to be an open and future thinking collection conforming to modern data practices. The goals can really be divided into two areas. The first is the data itself and the second what is expected from the data.

The **data goals** are to keep all views of the data synchronized consistently. The source-of-truth for the data is Devon’s database, however, this is missing enough information that is held in other applications. The specific goals here are to have a numeric unique identifier (“primary key”), not the work’s title that can be used to “join” collections together. For example, it’s perfectly fine for Devon’s database to not store the web site image url provided Devon’s collection can be joined through the unique identifier with another database that keeps other information.

As data is moved between applications we need to make sure the process is reliable and not lossy, we shouldn’t be losing any information, all sources should be in UTF-8 character encoding to prevent loss of diacritical characters (for example acute, grave accent characters)

The benefits of being able to materialize the data in this way is many fold, data forms the basis of the search goal along with making things like generating mobile or desktop web applications straightforward. If Kadist wanted in the future to participate in the new openness of data that is a stated goal of MOMA and other institutions having a consistent data representation is imperative.

An equally important reason for having a “clean” database is to facilitate the search goals.

The collection **search goals** are to be able to perform searches within a collection with the possible future extension of searching between collections. 
Stated simply the goal is to be to art search what Google is to web search, the similarity engine should be able to fast, powerful, intuitive and lightning fast. Much of this is the UX (user experience) but there’s also some sophisticated algorithmic approaches that should deliver on these goals.

There are three search types.

1. *Meta search*, for example answering questions:

  - “all works created after year 2000”
  - “all photographs”
  - “all installations by french artists”
  - “all works with sérigraphie in the title”

  The above should be able to suggest “did you mean” responses to common mistakes (e.g. spelling errors)

2. *Works search*, given a work as the search query the search should be able to return the list of other works in the collection that are related. Search accuracy is measured in terms of two metrics, recall and precision.  Precision is the fraction of retrieved works that are relevant, while recall (also known as sensitivity) is the fraction of relevant works that are retrieved. From a UX perspective it should be possible in the search app to drag a work onto the search box and use this as the starting point. 

3. *Tag search*, within a collection (or across collections in the future), given one or more search terms these are to be thematically matched to the work's thematic tags. Searching, for example, for the theme of **pollution** the results should contain a ranked list of works that consistent thematically with the search theme, for example, *environmental*, *sustainability*, *air quality*, etc. Understanding the relationship between tags is where machine learning will be useful. This remains, however, an unsolved problem and represents the state of the art in computer science (to set expectations.)

#Engineering Plan

The work that should be accomplished can be divided into the following areas:

1. Tagging the collection.

2. Data Integrity (Devon & Lincoln)
  The movement of data between Devon's database, the website and the tagging application should be lossless and reliable. This may not be much work.
  
3. Tagging Application (Lincoln)
  The tagging application is going to be used extensively and must meet some basic requirements:
  - be fast & intuitive
  - be able to easily handle new works entering the collection
  - be able to export the tags in a consistent way (currently the tags are a mixture between wordnet synset names ("Dog.n.01") and the regular undisambiguated format ("dog")
  - use auto-complete to try and normalize as much as possible to prevent one person tagging "dog" and someone else tagging "dogs", if taggers pick from the offered choices when it makes sense to we will have a more canonical representation of the tagger's intent. 
  - the first task here is to evaluate the current app and estimate how much time it would take to reach a good place. The application can also evolve as the taggers proceed. 

4. Search Engine (Daren)
  The initial search infrastructure can proceed without tags, however, it is hoped that as the search app proceeds the database of works that are tagged increases. More signal means better results.
  - build API (REST) framework so search can be used from a web app
  - build a pluggable "engine" so we can experiment with different thematic algorithms.
  - train/index/query a semantic model of the works descriptions that can be evaluated against works similarity through tags.
  - build/evaluate word vector models for tag expansion to improve tag search recall. For example if a works was tagged with "global warming" and another "climate change" without some form of expansion these two would never match.

5. Search Application (Daren)
  The search application uses the above search engine but presents a clean, modern search interface that can be used to evaluate the results as more sophisticated algorithms or improved data become available. 
  - Build App 
