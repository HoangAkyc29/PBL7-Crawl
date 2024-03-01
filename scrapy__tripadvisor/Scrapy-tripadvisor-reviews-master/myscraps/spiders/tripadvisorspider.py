#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy
from myscraps.items import ReviewItem
from scrapy import Request

class TripAdvisorReview(scrapy.Spider):
    name = "tripadvisor"
    # Cities: Recife, Porto Alegre, Salvador, Brasilia, Fortaleza, Curitiba, Belo Horizonte, Vitoria, Florianopolis, Natal, Goiania.
    start_urls = [
    # Miền Nam
    "https://www.tripadvisor.com/Tourism-g2145104-Ba_Ria_Vung_Tau_Province-Vacations.html",
    "https://www.tripadvisor.com/Tourism-g6936569-Bac_Lieu_Bac_Lieu_Province_Mekong_Delta-Vacations.html",
    "https://www.tripadvisor.com/Tourism-g737085-Ben_Tre_Ben_Tre_Province_Mekong_Delta-Vacations.html",
    "https://www.tripadvisor.com/Tourism-g1568668-Ca_Mau_Ca_Mau_Province_Mekong_Delta-Vacations.html",
    "https://www.tripadvisor.com/Tourism-g2146205-Dong_Nai_Province-Vacations.html",
    "https://www.tripadvisor.com/Tourism-g2146206-Dong_Thap_Province_Mekong_Delta-Vacations.html",
    "https://www.tripadvisor.com/Attractions-g2146212-Activities-Kien_Giang_Province.html",
    "https://www.tripadvisor.com/Attractions-g2062768-Activities-Long_An_Province_Mekong_Delta.html",
    "https://www.tripadvisor.com/Tourism-g298084-Tay_Ninh_Tay_Ninh_Province-Vacations.html",
    "https://www.tripadvisor.com/Tourism-g2062551-Tien_Giang_Province_Mekong_Delta-Vacations.html"
]

    def parse(self, response):
        urls = []
        for href in response.xpath('//div[@class="property_title"]/a/@href').extract():
            url = response.urljoin(href)
            if url not in urls:
                urls.append(url)

                yield scrapy.Request(url, callback=self.parse_page)

        next_page = response.xpath('//div[@class="unified pagination "]/a/@href').extract()
        if next_page:
            url = response.urljoin(next_page[-1])
            print(url)
            yield scrapy.Request(url, self.parse)

    def parse_page(self, response):

        review_page = response.xpath('//div[@class="wrap"]/div/a/@href').extract()

        if review_page:
            for i in range(len(review_page)):
                url = response.urljoin(review_page[i])
                yield scrapy.Request(url, self.parse_review)

        next_page = response.xpath('//div[@class="unified pagination "]/a/@href').extract()
        if next_page:
            url = response.urljoin(next_page[-1])
            yield scrapy.Request(url, self.parse_page)



    def parse_review(self, response):

        item = ReviewItem()

        contents = response.xpath('//div[@class="entry"]/p').extract()
        content = contents[0].encode("utf-8")

        ratings = response.xpath('//span[@class="rate sprite-rating_s rating_s"]/img/@alt').extract()
        rating = ratings[0][0]


        item['rating'] = rating
        item['review'] = content
        yield item

