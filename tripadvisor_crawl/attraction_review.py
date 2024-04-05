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


def scrape_tourist_destination_data(url, retry = False, proxy = None, retry_times = 0):

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
                scrape_tourist_destination_data(url, False, proxy, retry_times + 1)
            return

        try:

            # Tìm thẻ h1 theo class name
            attraction_name_ele = driver.find_element("class name", "biGQs._P.fiohW.eIegw")

            # Lấy nội dung của thẻ h1
            name = attraction_name_ele.text
            print(name)

        except Exception as e:
            driver.quit()
            scrape_tourist_destination_data(url, True, proxy, retry_times + 1)
        # # Chờ cho đến khi nút có thể nhấp được
        # buttons = WebDriverWait(driver, 10).until(
        #     EC.element_to_be_clickable((By.CLASS_NAME, "OKHdJ.z.Pc.PQ.Pp.PD.W._S.Gn.Rd._M.PQFNM.wSSLS"))
        # )

        # # Nhấp vào nút
        # buttons[0].click()
        # Chờ cho đến khi phần tử div có class là "biGQs _P fiohW hzzSG uuBRH" được tìm thấy và có thể nhận nội dung text
        review_ele = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.biGQs._P.fiohW.hzzSG.uuBRH"))
        )
        # Lấy nội dung text của phần tử div
        review_score = review_ele.text

        review_amount_ele = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "span.biGQs._P.pZUbB.KxBGd"))
        )
        # Lấy nội dung text của phần tử div
        review_amount= review_amount_ele.text
        print(review_amount)

        try:
            # Chờ đợi tất cả các thẻ <span> xuất hiện trên trang
            span_elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span")))

            # Lặp qua từng phần tử <span> và kiểm tra nội dung
            for span_element in span_elements:
                try:
                    text = span_element.text.strip()  # Lấy văn bản của phần tử và loại bỏ khoảng trắng ở đầu và cuối
                    if text.lower() == "more" or text.lower() == "read more" or text.lower() == "see more":
                        span_element.click()
                except Exception as e:
                    print("Đã xảy ra lỗi khi lấy văn bản từ phần tử span:", e)

        
        except Exception as e:
            print("Đã xảy ra lỗi khi tìm các phần tử span:", e)
        
        try: 
            review_comment_ele = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "span.yCeTE"))
            )
            
            review_comment = review_comment_ele.text
            print(review_comment)
        
        except Exception as e:
            driver.quit()
            print("Đã xảy ra lỗi khi tìm các phần tử comment span:", e)

        driver.quit()

    except Exception as e:
        print(f"Lỗi kết nối driver. {e}")
        driver.quit()
        return

scrape_tourist_destination_data("https://www.tripadvisor.com/Attraction_Review-g293924-d8587645-Reviews-Trap_Viet_Nam-Hanoi.html")