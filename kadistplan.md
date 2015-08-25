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

3. *Tag search*, within a collection (or across collections in the future), if a 

