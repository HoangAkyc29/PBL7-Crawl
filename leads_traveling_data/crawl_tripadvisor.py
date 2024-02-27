import os
import time
import re
import requests
from datetime import datetime, timedelta
import threading
import queue
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.command import Command
from selenium.webdriver.common.keys import Keys
from unidecode import unidecode  # Để loại bỏ dấu tiếng Việt
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from setup_crawl import get_free_proxies, connectdriver, headlessconnectdriver, defaultconnectdriver, get_extension_list


def scrape_tourist_destination_data(url):

    # subfolder = ["tourist_destination_data"]

    try:
        driver = defaultconnectdriver()

        driver.get(url)
        driver.implicitly_wait(5)  # Đợi 5 giây để load trang
        # Đặt điều kiện chờ (chờ tối đa 5 giây)
        wait = WebDriverWait(driver, 5)

        # Đợi cho tất cả các phần tử a có class là "BMQDV _F Gv wSSLS SwZTJ hNpWR" xuất hiện
        elements = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.BMQDV._F.Gv.wSSLS.SwZTJ.hNpWR"))
        )
        
        # Lặp qua từng phần tử a và lấy giá trị href của chúng
        hrefs = []
        for element in elements:
            href = element.get_attribute("href")
            if href:
                hrefs.append(href)
        
        # In tất cả các địa chỉ href đã lấy được
        print("Các địa chỉ href:")
        for href in hrefs:
            print(href)
        
        driver.quit()

    except Exception as e:
        print(f"Lỗi. {e}")
        driver.quit()
        return None

scrape_tourist_destination_data("https://www.tripadvisor.com.vn/Attractions-g293925-Activities-Ho_Chi_Minh_City.html")