import os
import time
import re
import requests
from datetime import datetime, timedelta
import threading
from collections import deque
import queue
import keyboard
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.command import Command
from selenium.webdriver.common.keys import Keys
from unidecode import unidecode  # Để loại bỏ dấu tiếng Việt
from difflib import SequenceMatcher

from setup_crawl import check_csv, get_1_proxy_data, connectdriver, headlessconnectdriver, defaultconnectdriver, get_extension_list, save_to_file, filter_duplicate_lines, is_https_url

def negate_duplicate_urls(file_path1, file_path2):
    # Đọc tất cả các URL từ file_path2 và đặt chúng vào một set để loại bỏ các URL trùng lặp
    urls_set = set()
    with open(file_path2, 'r', encoding='utf-8') as file2:
        for line in file2:
            urls_set.add(line.strip())

    # Mở file_path1 để đọc các URL và ghi lại chỉ các URL không trùng lặp vào file
    with open(file_path1, 'r', encoding='utf-8') as file1:
        urls = [line.strip() for line in file1 if line.strip() not in urls_set]

    # Ghi lại các URL không trùng lặp vào file_path1
    with open(file_path1, 'w', encoding='utf-8') as file1:
        for url in urls:
            file1.write(url + '\n')

def find_most_similar_url(url, file_path):
    max_similarity = 0
    most_similar_url = None
    
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            candidate_url = line.strip()
            similarity = SequenceMatcher(None, url, candidate_url).ratio()
            if similarity > max_similarity and similarity < 1:
                max_similarity = similarity
                most_similar_url = candidate_url
    
    return most_similar_url

def extract_place_text(url):
    try:

        processed_string = re.sub(r'[^\w\s]', '--', url)
        return processed_string
    except Exception as e:
        print("Đã xảy ra lỗi:", e)
        return None

def get_first_url(file_path):
    with open(file_path, 'r') as file:
        first_line = file.readline().strip()
        return first_line


def scrape_tourist_destination_data(url, url_source_name, retry = False, proxy = None, retry_times = 0):

    try:
        try:
            if (retry == True):
                check_csv()
                driver = defaultconnectdriver(get_1_proxy_data())
            else:
                if not proxy:
                    driver = defaultconnectdriver()
                else:
                    driver = defaultconnectdriver(proxy)

            driver.get(url)
            driver.implicitly_wait(10)  # Đợi 10 giây để load trang
        
        except Exception as e:
            print(f"Lỗi kết nối driver. {e}")
            driver.quit()
            if (retry_times < 5):
                scrape_tourist_destination_data(url, url_source_name, False, proxy, retry_times + 1)
            return
        
        # Đặt điều kiện chờ (chờ tối đa 7 giây)
        wait = WebDriverWait(driver, 7)
        time.sleep(5)
        
        all_urls = []
        retry_value = 0
        try:
            # Lấy tất cả các thẻ a có href
            href_elements = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[href]')))

            hrefs = [element.get_attribute("href") for element in href_elements]

            if(len(hrefs) <= 10):
                driver.quit()
                if (retry_times < 5):
                    scrape_tourist_destination_data(url, url_source_name, True, proxy, retry_times + 1)
                return

        except Exception as e:
            print(f"Lỗi tìm các thẻ a. {e}")
            driver.quit()
            if (retry_times < 5):
                scrape_tourist_destination_data(url, url_source_name, True, proxy, retry_times + 1)
            return
        
        All_urls_filepath = save_to_file(hrefs, url_source_name)
        filter_duplicate_lines(All_urls_filepath)

        try:
            # Chờ đợi tất cả các thẻ <span> xuất hiện trên trang
            span_elements = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.taLnk.ulBlueLinks")))

            # Lặp qua từng phần tử <span> và kiểm tra nội dung
            for span_element in span_elements:
                try:
                    text = span_element.text.strip()  # Lấy văn bản của phần tử và loại bỏ khoảng trắng ở đầu và cuối
                    if text.lower() == "more" or text.lower() == "read more" or text.lower() == "đọc thêm":
                        span_element.click()
                except Exception as e:
                    print("Đã xảy ra lỗi khi lấy văn bản từ phần tử span:", e)

        except Exception as e:
            print("Đã xảy ra lỗi khi tìm các phần tử span:", e)

        try:
            # Lấy tất cả các thẻ trên trang web
            text_elements = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a, span, div, p, li, h1, h2, h3, h4, h5, h6")))

            # Danh sách để lưu trữ văn bản từ các thẻ
            text_list = []

            # Lặp qua từng phần tử và lấy văn bản
            for element in text_elements:
                try:
                    text = element.text
                    if text:
                        text_list.append(text)
                except Exception as e:
                    print("Đã xảy ra lỗi khi lấy văn bản từ phần tử:", e)

        except Exception as e:
            print("Đã xảy ra lỗi khi tìm các phần tử trên trang web:", e)
        
        driver.quit()
        place_string = extract_place_text(url)

        try: 
            destination_content_file_path = save_to_file(text_list, place_string, "destination_content")
            filter_duplicate_lines(destination_content_file_path)

            used_url = []
            used_url.append(url)
            used_urls_file_path = save_to_file(used_url, "used_urls.txt")
            negate_duplicate_urls(All_urls_filepath, used_urls_file_path)
            most_related_url = find_most_similar_url(url, All_urls_filepath)
            scrape_tourist_destination_data(most_related_url, url_source_name, False, proxy)

        except Exception as e:
            print(f"Lỗi xử lý lưu trữ file. {e}")

    except Exception as e:
        print(f"Lỗi kết nối driver. {e}")
        driver.quit()
        return