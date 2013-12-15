#!/usr/bin/env python

import cgi
import cgitb; cgitb.enable()  # for troubleshooting

import pymongo

import sys

print "Content-Type: text/html\n\n"     # HTML is following



settings = {
    'MONGODB_SERVER'            : '127.0.0.1',
    'MONGODB_PORT'              : 27017,
    'MONGODB_DB'                : 'leboncoin',
    'MONGODB_COLLECTION'        : 'adds',
    'MONGODB_COLLECTION_SEARCH' : 'search',
}


def getSearches():
    connection      = pymongo.Connection(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
    db              = connection[settings['MONGODB_DB']]
    collection      = db[settings['MONGODB_COLLECTION_SEARCH']]

    # get categories
    searches    = list(collection.find())
    return searches



    
def printHTML(searches):

    print """
<html>
    <head>
        <meta charset="utf-8" />
        <title>LBC</title>
    </head>
    <body>
        <script src="/lbc/jquery-2.0.2.min.js"></script>
        <script>
$(document).ready(function() {
    $('#lbcform').on('submit', function() {
        $("#content").html('<img src="/lbc/images/loading.gif">')
 
            $.ajax({
                url: $(this).attr('action'),
                type: $(this).attr('method'), 
                data: $(this).serialize(), 
                success: function(html) { 
                    $("#content").html(html)
                }
            });
        return false; 
    });
    $('#lbcform_add').on('submit', function() {
        $("#content").html('<img src="/lbc/images/loading.gif">')
 
            $.ajax({
                url: $(this).attr('action'),
                type: $(this).attr('method'), 
                data: $(this).serialize(), 
                success: function(html) { 
                    $("#content").html(html)
                }
            });
        return false; 
    });


});
        </script>

        </form> 
        <div style="clear:both;float:left;">
            <form id="lbcform_add" action="/cgi-bin/leboncoin.cgi" method="get">
            Add Search <input type="text" value="" name="search_add">
            <select name="search_category">
                <option value="ameublement" >ameublement</option>
                <option value="decoration" >decoration</option>
                <option value="auto" >auto</option>
                <option value="informatique" >informatique</option>
                <option value="image_son" >image_son</option>
                <option value="consoles_jeux_video" >consoles_jeux_video</option>
                <option value="accessoires_bagagerie" >accessoires_bagagerie</option>
            </select>
            <input type="submit" value="Add" >
            </form> 
        </div>

        <form id="lbcform" action="/cgi-bin/leboncoin.cgi" method="get">
        <div style="width:250px;float:right;">
            <br /><input size="2" type="text" name="first" value="0" >:
            <input type="text" size="2" name="last" value="150" >
            <input type="submit" id="envoyer" value="Go" >
        </div>

        <div style="clear:both;"><br/></div>
        <div style="float:left;"><b>Search that: </b></div>
        """
    for search in searches:
        print '<div style="float:left;"><input type="checkbox" name="search_id" value="'+ str(search ['_id'])+'">'+ search['search'] +' ('+search['category']+')</div>'

    print """
        <div style="clear:both;"><br/></div>
        <div id="content" ></div>
    </body>
</html>

    """


def main():

    connection      = pymongo.Connection(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
    db              = connection[settings['MONGODB_DB']]
    collection      = db[settings['MONGODB_COLLECTION']]
    

    # get categories
    #categories  = collection.distinct("category")
    #searches    = collection.distinct("search")
    searches = getSearches()

    # get searches

    # print html
    printHTML(searches)


if __name__ == '__main__':
    main()


