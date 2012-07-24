#!/usr/bin/env python

import json
import sys
import xapian

### Start of example code.
def search(dbpath, querystring, offset=0, pagesize=20):
    # offset - defines starting point within result set
    # pagesize - defines number of records to retrieve

    # Open the database we're going to search.
    db = xapian.Database(dbpath)

    # Set up a QueryParser with a stemmer and suitable prefixes
    queryparser = xapian.QueryParser()
    queryparser.set_stemmer(xapian.Stem("en"))
    queryparser.set_stemming_strategy(queryparser.STEM_SOME)
    queryparser.add_prefix("title", "S")
    queryparser.add_prefix("reviewer", "U")

    # And parse the query
    query = queryparser.parse_query(querystring)

    # Use an Enquire object on the database to run the query
    enquire = xapian.Enquire(db)
    enquire.set_query(query)

    # And print out something about each match
    matches = []
    for match in enquire.get_mset(offset, pagesize):
        fields = json.loads(match.document.get_data())
        print u"%(rank)i: #%(docid)3.3i %(reviewer)s: %(title)s %(content)s" % {
            'rank': match.rank + 1,
            'docid': match.docid,
            'title': fields.get('title', u''),
            'content': fields.get('content', u''),
            'reviewer': fields.get('reviewer', u''),
        }

search(dbpath = '/Users/appwillmini8/src/indexd/test_comments', querystring = " ".join(sys.argv[1:]))
