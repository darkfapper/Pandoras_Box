import scrapy
from scrapy_splash import SplashRequest
from fake_useragent import UserAgent


class TerpySpideySpider(scrapy.Spider):
    name = 'terpy_spidey'
    allowed_domains = ['terpyseeds.com']
    start_urls = 'https://terpyseeds.com/shop'
    
    ua = UserAgent()
    userAgent = ua.random
    
    def start_requests(self):
        yield SplashRequest(
            self.start_urls,
            callback=self.parse,
            endpoint="execute",
            headers={"User-Agent": self.userAgent},
        )


    def parse(self, response):
        strains = response.xpath("//div[@data-source='main_loop']//div[@class = 'product-wrapper']")
 
        for strain in strains:
            name = strain.xpath(".//h3[@class='wd-entities-title']/a/text()").get()
            price = strain.xpath(".//div[@class='wrapp-product-price']//ins//bdi/text()").get()
            
            tags = strain.xpath(".//div[@class='wd-product-cats']/a")
            
            tags = [tag.xpath("./text()").get() for tag in tags]
            
            if not price:
                price = strain.xpath(".//div[@class='wrapp-product-price']//bdi/text()").get()
            
            yield{
                "name":name,
                "price":price,
                "tags":tags
            }
            
        next_page_url = response.xpath(
            "//a[@class='next page-numbers']/@href"
        ).get()
        
        
        print(next_page_url)
        print(type(next_page_url))
        if next_page_url:
            yield SplashRequest(next_page_url,
                    callback=self.parse,
                    endpoint="execute",
                    headers={"User-Agent": self.userAgent},
        )