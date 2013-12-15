from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.loader import XPathItemLoader
from leboncoin.items import LeboncoinItem

from scrapy.conf import settings

import urllib
from urlparse import urlparse, parse_qs



class LeboncoinSpider(BaseSpider):
    name = "leboncoin"
    allowed_domains = ["www.leboncoin.fr"]
   #start_urls = [
   #    "http://www.leboncoin.fr/annonces/offres/nord_pas_de_calais/"
   #]

    start_urls      = []

    searches        = settings['LBC_SEARCHES']
    #categories      = settings['LBC_CATEGORIES']

    for page in range(1,settings['LBC_DEPTH']):
        for search in searches:
            #for category in categories:
            start_urls.append('http://www.leboncoin.fr/'+urllib.quote(search['category'])+'/offres/nord_pas_de_calais/?q='+urllib.quote(search['search'])+'&o='+str(page))


    def parse(self, response):
        #filename = response.url.split("/")[-2]
        #open(filename, 'wb').write(response.body)
        hxs         = HtmlXPathSelector(response)
        ads         = hxs.select('//div[@class="list-lbc"]/a')
        items       = []
        def get_first(iterable, default=None):
            if iterable:
                for item in iterable:
                    return item
                return default
        for ad in ads:
            item        = LeboncoinItem()
            item['id']          = get_first(ad.select('@href').re('(\d+).htm'))
            item['name']        = get_first(ad.select('div[@class="lbc"]/div[@class="detail"]/div[@class="title"]/text()').re('^\s*([\w\s]+\w)\s*'))
            item['photo']       = get_first(ad.select('div[@class="lbc"]/div[@class="image"]/div[@class="image-and-nb"]/img/@src').extract())
            item['url']         = get_first(ad.select('@href').extract())
            item['price']       = get_first(ad.select('div[@class="lbc"]/div[@class="detail"]/div[@class="price"]/text()').re('^\s*([\w\s]+\w)\s*'))
            item['placement']   = get_first(ad.select('div[@class="lbc"]/div[@class="detail"]/div[@class="placement"]/text()').re('^\s*([\w\s]+\w)\s*'))
            item['category']    = response.url.split("/")[-4] 
            # Or use the parse_qs method
            
            query_components    = parse_qs(urlparse(response.url).query)
            item['search']      = get_first(query_components["q"] )

            #item['search']      = response.url.split("/")[-4] 
            items.append(item)
        return items
