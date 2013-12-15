# Scrapy settings for leboncoin project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

import pymongo

BOT_NAME = 'leboncoin'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['leboncoin.spiders']
NEWSPIDER_MODULE = 'leboncoin.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

BASE_DIR = '/tmp'

DOWNLOADER_MIDDLEWARE = {
    'spider.middlewares.RetryChangeProxyMiddleware': 600,
}

ITEM_PIPELINES = ['leboncoin.pipelines.MongoDBPipeline',]

MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "leboncoin"
MONGODB_COLLECTION = "adds"
MONGODB_COLLECTION_ADDS = "adds"
MONGODB_COLLECTION_SEARCH = "search"

LOG_LEVEL='INFO'

def getSearches():
    connection      = pymongo.Connection(MONGODB_SERVER, MONGODB_PORT)
    db              = connection[MONGODB_DB]
    collection      = db[MONGODB_COLLECTION_SEARCH]

    # get categories
    searches    = list(collection.find())
    return searches

    

LBC_SEARCHES = getSearches()

#LBC_SEARCHES    = ['industriel','loft','bois metal','porte manteau','vintage', 'meuble hifi', 'meuble tv']
#LBC_CATEGORIES  = ['ameublement','decoration','arts_de_la_table']
LBC_DEPTH       = 15
#LBC_SEARCHES    = config['searches']
#LBC_CATEGORIES  = config['categories']


# > db.adds.aggregate({$group: { _id: {search: "$search", category: "$category"}  }   })
# > db.adds.distinct("search")


