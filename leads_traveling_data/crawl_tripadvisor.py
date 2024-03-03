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
from difflib import SequenceMatcher

from setup_crawl import check_csv, get_1_proxy_data, connectdriver, headlessconnectdriver, defaultconnectdriver, get_extension_list, save_to_file, filter_duplicate_lines

urls_overview_general = [
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
            if similarity > max_similarity:
                max_similarity = similarity
                most_similar_url = candidate_url
    
    return most_similar_url

def extract_place_text(url):
    try:
        # Cắt bỏ phần đầu của URL
        url = url.replace("https://www.tripadvisor.com/", "")
        url = url.replace("https://www.tripadvisor.com.vn/", "")
        url = url.replace("/","---")

        # Tìm vị trí kết thúc của phần text cần lấy (lấy từ đầu đến ký tự ".html")
        end_index = url.find(".html")

        # Lấy phần text từ URL
        review_text = url[:end_index]

        return review_text
    except Exception as e:
        print("Đã xảy ra lỗi:", e)
        return None

def scrape_tourist_destination_data(url, retry = False, proxy = None):

    # subfolder = ["tourist_destination_data"]

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
            driver.implicitly_wait(20)  # Đợi 10 giây để load trang
        
        except Exception as e:
            print(f"Lỗi kết nối driver. {e}")
            driver.quit()
            scrape_tourist_destination_data(url, False, proxy)
            return
        
        # Đặt điều kiện chờ (chờ tối đa 5 giây)
        wait = WebDriverWait(driver, 5)
        time.sleep(5)
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

        # urls_destination_detail = []
        # try:
        #     # Tìm tất cả các thẻ li có id là "Mkrpq Fg I _u"
        #     list_items = driver.find_elements(By.CSS_SELECTOR, 'li.Mkrpq.Fg.I._u')

        #     print("Số lượng thẻ li được tìm thấy:", len(list_items))

        #     # Duyệt qua từng thẻ li
        #     for item in list_items:
        #         try:
        #             # Tìm tất cả các thẻ a trong thẻ li đó
        #             anchor_tags = item.find_elements(By.TAG_NAME, 'a')
                    
        #             # Duyệt qua từng thẻ a và lấy địa chỉ href
        #             for a_tag in anchor_tags:
        #                 href = a_tag.get_attribute("href")
        #                 if href:
        #                     urls_destination_detail.append(href)

        #         except Exception as e:
        #             print("Lỗi khi tìm thẻ a:", e)
        #             continue

        # except Exception as e:
        #     print("Lỗi khi tìm thẻ li:", e)

        # urls_overview = []

        # try:
        #     # Đợi cho tất cả các thẻ a có class name chứa đúng chuỗi "UikNM _G B- _S _W T c G wSSLS" xuất hiện
        #     elements = wait.until(
        #         EC.presence_of_all_elements_located((By.XPATH, '//a[contains(@class, "UikNM") and contains(@class, "_G") and contains(@class, "B-") and contains(@class, "_S") and contains(@class, "_W") and contains(@class, "T") and contains(@class, "c") and contains(@class, "G") and contains(@class, "wSSLS")]'))
        #     )

        #     for element in elements:
        #         try:
        #             href = element.get_attribute("href")
        #             urls_overview.append(href)
        #         except Exception as e:
        #             print("Error while extracting href:", e)

        # except Exception as e:
        #     print("Lỗi khi tìm đối tượng 'Xem tất cả':", e)

        # # Đóng trình duyệt
        # driver.quit()
        # print(urls_destination_detail)
        # print(urls_overview)

        # save_to_file(urls_destination_detail, "urls_destination_detail")
        # save_to_file(urls_overview, "urls_overview")
        
        all_urls = []
        retry_value = 0
        try:
            # Lấy tất cả các thẻ a có href
            href_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[href]')))

            hrefs = [element.get_attribute("href") for element in href_elements]

            if(len(hrefs) <= 10):
                driver.quit()
                scrape_tourist_destination_data(url, True, proxy)
                return

        except Exception as e:
            print(f"Lỗi tìm các thẻ a. {e}")
            driver.quit()
            scrape_tourist_destination_data(url, True, proxy)
            return
        
        All_urls_filepath = save_to_file(hrefs, "all_urls")
        filter_duplicate_lines(All_urls_filepath)

        try:
            # Chờ đợi tất cả các thẻ <span> xuất hiện trên trang
            span_elements = WebDriverWait(driver, 10).until(
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
            used_urls_file_path = save_to_file(used_url, "used_urls")
            negate_duplicate_urls(All_urls_filepath, used_urls_file_path)
            most_related_url = find_most_similar_url(url, All_urls_filepath)
            scrape_tourist_destination_data(most_related_url, False, proxy)

        except Exception as e:
            print(f"Lỗi xử lý lưu trữ file. {e}")

    except Exception as e:
        print(f"Lỗi kết nối driver. {e}")
        driver.quit()
        return None

scrape_tourist_destination_data("https://www.tripadvisor.com.vn/Attraction_Review-g293923-d1968469-Reviews-Halong_Bay-Halong_Bay_Quang_Ninh_Province.html")