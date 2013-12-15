#!/usr/bin/env python

import cgi
import cgitb; cgitb.enable()  # for troubleshooting

import pymongo
#from pymongo.objectid import ObjectId
#from bson.objectid import Objectid
from bson.objectid import ObjectId

import sys

print "Content-Type: text/html\n\n"     # HTML is following



settings = {
    'MONGODB_SERVER'            : '127.0.0.1',
    'MONGODB_PORT'              : 27017,
    'MONGODB_DB'                : 'leboncoin',
    'MONGODB_COLLECTION'        : 'adds',
    'MONGODB_COLLECTION_ADDS'   : 'adds',
    'MONGODB_COLLECTION_SEARCH' : 'search',
}

def getSearches(ids):
    connection      = pymongo.Connection(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
    db              = connection[settings['MONGODB_DB']]
    collection      = db[settings['MONGODB_COLLECTION_SEARCH']]

    objectIdds = []
    for idd in ids:
        objectIdds.append( ObjectId(idd)  )


    # get categories
    searches    = list(collection.find({"_id": {"$in": objectIdds } },{"_id" : 0}))
    return searches

    
def printItem(item):
    keys = ['photo','url','name','price','placement']
    for key in keys:
        if not key in item:
            item[key] = ''
        if not item[key]:
            item[key] = ''
    html = """<div>
        <div style="width:auto;height:180px;float:left;margin:1px;font-size:10px;">
            <a href="%s" alt="%s">
                <img src="%s" />
                <br/>
                %s &euro; - %s
            </a>
        </div>
    </div>""" % (''.join(item['url']), ''.join(item['name']), ''.join(item['photo']), item['price'], item['placement'] )
    print html;

    sys.stdout.flush()


def main():
    form = cgi.FieldStorage()


    if "search_id" in form:
        search      = form.getlist("search_id")
        first       = (form.getfirst("first", ""))
        last        = (form.getfirst("last", ""))

        if not first :
            first = 0
        if not last :
            last = 50

        if not last > first:
            print "<H1>Error</H1>"
            print "Wrong tabs"
            return


        connection      = pymongo.Connection(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db              = connection[settings['MONGODB_DB']]
        collection      = db[settings['MONGODB_COLLECTION_SEARCH']]
        
        # get searches
        searches = getSearches(search)
        # find it !
        collection      = db[settings['MONGODB_COLLECTION_ADDS']]
        for item in collection.find( { "$or":  searches  }  ).sort("id",-1)[int(first):int(last)] :
            printItem(item)

    elif "search_add" in form:
        if not "search_category" in form:
            print "<H1>Insufficient search parameters</H1>"

        search_search       = (form.getfirst("search_add", ""))
        search_category     = (form.getfirst("search_category", ""))

        connection      = pymongo.Connection(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db              = connection[settings['MONGODB_DB']]
        collection      = db[settings['MONGODB_COLLECTION_SEARCH']]

        collection.insert({"category": search_category, "search":search_search})

        print "search added! "
    else:

        print "<H1>Wrong usage</H1>"




if __name__ == '__main__':
    main()


