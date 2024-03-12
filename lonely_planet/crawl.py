# scrapy runspider crawl.py
import scrapy
import json
from service import save_to_file, extract_place_text, get_first_url, filter_duplicate_lines, negate_duplicate_urls, find_most_similar_url, fix_urls
class MySpider(scrapy.Spider):
    name = 'my_spider'
    
    custom_settings = {
        'CONCURRENT_REQUESTS': 12  # Số lượng luồng
    }

    def start_requests(self):
        # Đọc danh sách liên kết từ output.json
        file_path = f"crawling_urls.txt"
        url = get_first_url(file_path)

        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        domain = "https://www.lonelyplanet.com"
        url = response.url
        href_list = []

        # Lặp qua tất cả các thẻ <a>
        for a_tag in response.css('a'):
            # Lấy thuộc tính href của thẻ a
            href = a_tag.attrib.get('href')

            # Nếu tồn tại thuộc tính href, thêm vào danh sách
            if href:
                href_list.append(href)
        
        urls_file_path = save_to_file(href_list, "crawling_urls.txt")
        fix_urls("crawling_urls.txt", domain)
        place_string = extract_place_text(url)

        data_list = []
        # Lặp qua các phần tử p trong thẻ article
        for element in response.css('a, span, div, p, li, h1, h2, h3, h4, h5, h6'):
            text = element.xpath('string()').get().strip()
            # Kiểm tra nếu đoạn văn bản không chứa chuỗi cụ thể
            if text:
                # Thêm đoạn văn bản vào danh sách
                data_list.append(text)
        
        destination_content_file_path = save_to_file(data_list, place_string, "destination_content_folder")
        filter_duplicate_lines(destination_content_file_path)
        
        used_url = []
        used_url.append(url)
        used_urls_file_path = save_to_file(used_url, "crawl_used_urls.txt")
        negate_duplicate_urls(urls_file_path, used_urls_file_path)
        most_related_url = find_most_similar_url(url, urls_file_path)

        if most_related_url:
            # Tiếp tục crawl với most_related_url
            yield scrapy.Request(url=most_related_url, callback=self.parse, meta={'previous_url': url})