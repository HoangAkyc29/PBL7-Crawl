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

def scrape_GPT_data(url, retry = False, proxy = None, retry_times = 0):

    try:
        try:
            if (retry == True):
                check_csv()
                driver = defaultconnectdriver(get_1_proxy_data())
            else:
                if proxy == None:
                    driver = defaultconnectdriver()
                else:
                    driver = defaultconnectdriver(proxy)

            driver.get(url)
            driver.implicitly_wait(10)  # Đợi 10 giây để load trang
        
        except Exception as e:
            print(f"Lỗi kết nối driver. {e}")
            driver.quit()
            if (retry_times < 2):
                scrape_GPT_data(url, False, proxy, retry_times + 1)
            return
        time.sleep(5)

        # # Tìm nút bằng data-testid
        # button = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='login-button']"))
        # )

        # # Nhấp vào nút
        # button.click()
        time.sleep(90)

        # Tìm thẻ input bằng class
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".email-input"))
        )

        # Nhập nội dung vào thẻ input
        email_input.send_keys("Vinh.nd0231@gmail.com")

        time.sleep(5)

        # Tìm thẻ input bằng name và id
        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[name='password'][id='password']"))
        )

        # Nhập nội dung vào thẻ input
        password_input.send_keys("Nhoknadost@1")

        time.sleep(3)

        # Tìm button bằng type
        button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']"))
        )
        driver.quit()

    except Exception as e:
        print(f"Lỗi kết nối driver. {e}")
        driver.quit()
        return

scrape_GPT_data(r"https://chat.openai.com/auth/login?next=%2Fc%2F987b4931-272e-4d70-a21c-728366169288")