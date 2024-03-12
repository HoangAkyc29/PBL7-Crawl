import scrapy
import json

class MySpider(scrapy.Spider):
    name = 'my_spider'

    custom_settings = {
        'CONCURRENT_REQUESTS': 12  # Số lượng luồng
    }

    def start_requests(self):
        # Đọc danh sách liên kết từ output.json
        with open('output.json') as f:
            data = json.load(f)
        urls = [item['url'] for item in data]

        # Tạo yêu cầu truy cập cho từng liên kết
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # Tạo tên file
        file_number = response.url.split('/')[-2]  # Lấy phần số thứ tự từ URL
        file_name = f'output_{file_number}.txt'

        # Ghi nội dung vào file
        with open(file_name, 'w', encoding='utf-8') as f:
            # Lặp qua các phần tử p trong thẻ article
            for paragraph in response.css('article p'):
                # Lấy đoạn văn bản của phần tử p
                text = paragraph.xpath('string()').get().strip()
                # Kiểm tra nếu đoạn văn bản không chứa chuỗi cụ thể
                if "Bài viết có sử dụng tư liệu được tổng hợp và biên tập lại từ nhiều nguồn trên Internet" not in text:
                    # Ghi đoạn văn bản vào file
                    f.write(text + '\n')