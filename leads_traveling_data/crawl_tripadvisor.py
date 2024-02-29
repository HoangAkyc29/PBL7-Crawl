import os
import time
import re
import requests
from datetime import datetime, timedelta
import threading
from collections import deque
import queue

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.command import Command
from selenium.webdriver.common.keys import Keys
from unidecode import unidecode  # Để loại bỏ dấu tiếng Việt

from setup_crawl import check_csv, get_1_proxy_data, connectdriver, headlessconnectdriver, defaultconnectdriver, get_extension_list

urls_overview = [
    # Miền Bắc
    "https://www.tripadvisor.com/Tourism-g303942-Can_Tho_Mekong_Delta-Vacations.html",
    "https://www.tripadvisor.com/Tourism-g298085-Da_Nang-Vacations.html",
    "https://www.tripadvisor.com/Attraction_Review-g293923-d1968469-Reviews-Halong_Bay-Halong_Bay_Quang_Ninh_Province.html",
    "https://www.tripadvisor.com/Tourism-g303944-Hai_Phong-Vacations.html",
    "https://www.tripadvisor.com/Tourism-g1544599-Ha_Giang_Ha_Giang_Province-Vacations.html",
    "https://www.tripadvisor.com/Tourism-g293924-Hanoi-Vacations.html",
    "https://www.tripadvisor.com/Tourism-g3320435-Hoa_Binh_Hoa_Binh_Province-Vacations.html",
    "https://www.tripadvisor.com/Tourism-g293926-Hue_Thua_Thien_Hue_Province-Vacations.html",
    "https://www.tripadvisor.com/Tourism-g2144896-Lang_Son_Lang_Son_Province-Vacations.html",
    "https://www.tripadvisor.com/Tourism-g5556249-Nam_Dinh_Province-Vacations.html",
    "https://www.tripadvisor.com/Tourism-g2146239-Ninh_Binh_Province-Vacations.html",
    "https://www.tripadvisor.com/Tourism-g4355229-Phu_Tho_Phu_Tho_Province-Vacations.html",
    "https://www.tripadvisor.com/Attractions-g2146283-Activities-Quang_Ninh_Province.html",
    "https://www.tripadvisor.com/Attractions-g2146290-Activities-Quang_Tri_Province.html",
    "https://www.tripadvisor.com/Tourism-g4355220-Thai_Binh_Thai_Binh_Province-Vacations.html",
    "https://www.tripadvisor.com/Tourism-g1753936-Thai_Nguyen_Thai_Nguyen_Province-Vacations.html",
    "https://www.tripadvisor.com/Tourism-g1236104-Thanh_Hoa_Thanh_Hoa_Province-Vacations.html",
    "https://www.tripadvisor.com/Attractions-g2146363-Activities-Vinh_Phuc_Province.html",
    "https://www.tripadvisor.com/Tourism-g800616-Yen_Bai_Yen_Bai_Province-Vacations.html",
    # Miền Trung
    "https://www.tripadvisor.com/Attractions-g2145138-Activities-Binh_Dinh_Province.html",
    "https://www.tripadvisor.com/Tourism-g2145211-Binh_Thuan_Province-Vacations.html",
    "https://www.tripadvisor.com/Tourism-g1633422-Dak_Lak_Province-Vacations.html",
    "https://www.tripadvisor.com/Tourism-g2146200-Dak_Nong_Province-Vacations.html",
    "https://www.tripadvisor.com/Attractions-g1156336-Activities-Gia_Lai_Province.html",
    "https://www.tripadvisor.com/Tourism-g3312572-Ha_Tinh_Province-Vacations.html",
    "https://www.tripadvisor.com/Attractions-g1184689-Activities-Khanh_Hoa_Province.html",
    "https://www.tripadvisor.com/Tourism-g1156337-Kontum_Kon_Tum_Province-Vacations.html",
    "https://www.tripadvisor.com/Attractions-g2146217-Activities-Lam_Dong_Province.html",
    "https://www.tripadvisor.com/Attractions-g2146235-Activities-Nghe_An_Province.html",
    "https://www.tripadvisor.com/Tourism-g2146245-Phu_Yen_Province-Vacations.html",
    "https://www.tripadvisor.com/Tourism-g2146269-Quang_Binh_Province-Vacations.html",
    "https://www.tripadvisor.com/Tourism-g2146272-Quang_Nam_Province-Vacations.html",
    "https://www.tripadvisor.com/Tourism-g2146276-Quang_Ngai_Province-Vacations.html",
    "https://www.tripadvisor.com/Tourism-g469420-Soc_Trang_Soc_Trang_Province_Mekong_Delta-Vacations.html",
    "https://www.tripadvisor.com/Tourism-g2146376-Thua_Thien_Hue_Province-Vacations.html",
    "https://www.tripadvisor.com/Tourism-g2062551-Tien_Giang_Province_Mekong_Delta-Vacations.html",
    "https://www.tripadvisor.com/Tourism-g1535794-Tra_Vinh_Tra_Vinh_Province_Mekong_Delta-Vacations.html",
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

url_detail = []

def scrape_tourist_destination_data(url):

    # subfolder = ["tourist_destination_data"]

    try:
        # check_csv()
        # driver = defaultconnectdriver(get_1_proxy_data())
        driver = defaultconnectdriver()

        driver.get(url)
        driver.implicitly_wait(10)  # Đợi 5 giây để load trang
        # Đặt điều kiện chờ (chờ tối đa 5 giây)
        wait = WebDriverWait(driver, 5)

        # Đợi cho tất cả các phần tử a có class là "BMQDV _F Gv wSSLS SwZTJ hNpWR" xuất hiện
        # elements = wait.until(
        #     EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.BMQDV._F.Gv.wSSLS.SwZTJ.hNpWR"))
        # )
        
        # # Lặp qua từng phần tử a và lấy giá trị href của chúng
        # hrefs = []
        # for element in elements:
        #     href = element.get_attribute("href")
        #     if href:
        #         hrefs.append(href)
        
        # # In tất cả các địa chỉ href đã lấy được
        # print("Các địa chỉ href:")
        # for href in hrefs:
        #     print(href)
        
        # driver.quit()
        try:
            # Tìm tất cả các thẻ li có id là "Mkrpq Fg I _u"
            list_items = driver.find_elements(By.CSS_SELECTOR, 'li.Mkrpq.Fg.I._u')

            print("Số lượng thẻ li được tìm thấy:", len(list_items))

            # Duyệt qua từng thẻ li
            for item in list_items:
                try:
                    # Tìm tất cả các thẻ a trong thẻ li đó
                    anchor_tags = item.find_elements(By.TAG_NAME, 'a')
                    
                    # Duyệt qua từng thẻ a và lấy địa chỉ href
                    for a_tag in anchor_tags:
                        href = a_tag.get_attribute("href")
                        if href:
                            url_detail.append(href)

                except Exception as e:
                    print("Lỗi khi tìm thẻ a:", e)
                    continue

        except Exception as e:
            print("Lỗi khi tìm thẻ li:", e)

        # Đóng trình duyệt
        driver.quit()
        print(url_detail)

    except Exception as e:
        print(f"Lỗi kết nối driver. {e}")
        driver.quit()
        return None

scrape_tourist_destination_data("https://www.tripadvisor.com.vn/Attractions-g293925-Activities-Ho_Chi_Minh_City.html")