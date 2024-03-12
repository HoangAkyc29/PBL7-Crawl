import scrapy

class MySpider(scrapy.Spider):
    name = 'my_spider'
    start_urls = ['https://anvietnam.net/category/du-ky/page/{}/'.format(i) for i in range(1, 23)]
    visited_links = set()

    def parse(self, response):
        for link in response.css('div.large-9.col a::attr(href)').getall():
            if link not in self.visited_links:
                self.visited_links.add(link)
                yield {
                    'url': link
                }
