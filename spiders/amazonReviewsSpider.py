import scrapy
import random

class AmazonReviewsSpider(scrapy.Spider):
    
    name = "amazon_reviews"

    def __init__(self, *args, **kwargs):
        self.id = kwargs.pop('id', []) 
        #self.proxy_pool = [
        #    'http://103.105.48.16:80',
        #    'http://101.108.244.225:8080',
        #    'http://101.231.104.82:80',
        #    'http://1.10.228.18:8080',
         #   'http://102.140.108.98:53281',
        #    'http://1.20.100.165:61085',
         #   'http://101.108.111.66:8080',
          #  'http://1.20.99.125:56613',
         #   'http://101.50.1.2:80',
         #   'http://103.106.114.58:8080',
        #    'http://1.20.100.133:46755'
         #   ]
        self.user_agent_pool = [
            'Mozilla/5.0 (Amiga; U; AmigaOS 1.3; en; rv:1.8.1.19) Gecko/20081204 SeaMonkey/1.1.14',
            'Mozilla/5.0 (AmigaOS; U; AmigaOS 1.3; en-US; rv:1.8.1.21) Gecko/20090303 SeaMonkey/1.1.15',
            'Mozilla/5.0 (AmigaOS; U; AmigaOS 1.3; en; rv:1.8.1.19) Gecko/20081204 SeaMonkey/1.1.14',
            'Mozilla/5.0 (Android 2.2; Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4',
            'Mozilla/5.0 (BeOS; U; BeOS BeBox; fr; rv:1.9) Gecko/2008052906 BonEcho/2.0',
            'Mozilla/5.0 (BeOS; U; BeOS BePC; en-US; rv:1.8.1.1) Gecko/20061220 BonEcho/2.0.0.1',
            'Mozilla/5.0 (BeOS; U; BeOS BePC; en-US; rv:1.8.1.10) Gecko/20071128 BonEcho/2.0.0.10',
            'Mozilla/5.0 (BeOS; U; BeOS BePC; en-US; rv:1.8.1.17) Gecko/20080831 BonEcho/2.0.0.17',
            'Mozilla/5.0 (BeOS; U; BeOS BePC; en-US; rv:1.8.1.6) Gecko/20070731 BonEcho/2.0.0.6',
            'Mozilla/5.0 (BeOS; U; BeOS BePC; en-US; rv:1.8.1.7) Gecko/20070917 BonEcho/2.0.0.7',
            'Mozilla/5.0 (BeOS; U; BeOS BePC; en-US; rv:1.8.1b2) Gecko/20060901 Firefox/2.0b2',
            'Mozilla/5.0 (BeOS; U; BeOS BePC; en-US; rv:1.9a1) Gecko/20051002 Firefox/1.6a1',
            'Mozilla/5.0 (BeOS; U; BeOS BePC; en-US; rv:1.9a1) Gecko/20060702 SeaMonkey/1.5a',
            'Mozilla/5.0 (BeOS; U; Haiku BePC; en-US; rv:1.8.1.10pre) Gecko/20080112 SeaMonkey/1.1.7pre',
            'Mozilla/5.0 (BeOS; U; Haiku BePC; en-US; rv:1.8.1.14) Gecko/20080429 BonEcho/2.0.0.14',
            'Mozilla/5.0 (BeOS; U; Haiku BePC; en-US; rv:1.8.1.17) Gecko/20080831 BonEcho/2.0.0.17',
            'Mozilla/5.0 (BeOS; U; Haiku BePC; en-US; rv:1.8.1.18) Gecko/20081114 BonEcho/2.0.0.18',
            'Mozilla/5.0 (BeOS; U; Haiku BePC; en-US; rv:1.8.1.21pre) Gecko/20090218 BonEcho/2.0.0.21pre',
            'Mozilla/5.0 (Darwin; FreeBSD 5.6; en-GB; rv:1.8.1.17pre) Gecko/20080716 K-Meleon/1.5.0',
            'Mozilla/5.0 (Darwin; FreeBSD 5.6; en-GB; rv:1.9.1b3pre)Gecko/20081211 K-Meleon/1.5.2',
            'Mozilla/5.0 (Future Star Technologies Corp.; Star-Blade OS; x86_64; U; en-US) iNet Browser 4.7',
            'Mozilla/5.0 (Linux 2.4.18-18.7.x i686; U) Opera 6.03 [en]',
            'Mozilla/5.0 (Linux 2.4.18-ltsp-1 i686; U) Opera 6.1 [en]',
            'Mozilla/5.0 (Linux 2.4.19-16mdk i686; U) Opera 6.11 [en]',
            'Mozilla/5.0 (Linux 2.4.21-0.13mdk i686; U) Opera 7.11 [en]',
            'Mozilla/5.0 (Linux X86; U; Debian SID; it; rv:1.9.0.1) Gecko/2008070208 Debian IceWeasel/3.0.1',
            'Mozilla/5.0 (Linux i686 ; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.70',
            'Mozilla/5.0 (Linux i686; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0',
            'Mozilla/5.0 (Linux i686; U; en; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 Opera 10.51',
            'Mozilla/5.0 (Linux) Gecko Iceweasel (Debian) Mnenhy',
            ]
        super(AmazonReviewsSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        for i in range(1,20):
            request = scrapy.Request("https://www.amazon.ca/product-reviews/" + str(self.id) + "/?ie=UTF8&reviewerType=all_reviews&pageNumber=" + str(i), self.parse, headers={'User-Agent': random.choice(self.user_agent_pool)})
            #request.meta['proxy'] = random.choice(self.proxy_pool)
            yield request

    # Defining a Scrapy parser
    def parse(self, response):
        
        data = response.css('#cm_cr-review_list')
             
        # Collecting product star ratings
        star_rating = data.css('.review-rating')
             
        # Collecting user reviews
        comments = data.css('.review-text')
        count = 0
             
        # Combining the results
        for review in star_rating:
            yield{
                'stars': ''.join(review.xpath('.//text()').extract()),
                'comment': ''.join(comments[count].xpath(".//text()").extract())
                }
            count=count+1