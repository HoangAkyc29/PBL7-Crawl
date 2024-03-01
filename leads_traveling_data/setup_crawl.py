import os
import time
import csv
import re
import requests
from datetime import datetime, timedelta
import threading
import queue
import random
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

def get_path(A, B): #A là tên file, B là thư mục chứa file A có cùng cấp thư mục với file chương trình. Lấy ra đường dẫn file A trong thư mục B.
    # Lấy đường dẫn thực thi của chương trình
    program_path = os.path.dirname(os.path.abspath(__file__))
    
    # Kết hợp đường dẫn của thư mục B và tên file A
    file_path = os.path.join(program_path, B, A)

    # Kiểm tra xem file có tồn tại hay không
    if os.path.exists(file_path):
        return file_path
    else:
        # Nếu không tồn tại, tạo mới file
        os.makedirs(os.path.join(program_path, B), exist_ok=True)
        with open(file_path, 'w') as new_file:
            pass  # Mở và đóng file để tạo mới nó

        return file_path


def get_folder_path(folder_name): # cho folder name, hàm này sẽ lấy ra đường dẫn của thư mục đó với điều kiện thư mục đó cùng cấp thư mục với chương trình thực thi.
    current_directory = os.path.dirname(os.path.realpath(__file__))
    folder_path = os.path.join(current_directory, folder_name)
    return folder_path


def create_1D_csv_file(data):
    # Tạo tên tệp dựa trên thời gian hiện tại
    current_time = time.strftime("%Y%m%d_%H%M%S")
    file_name = f"output_{current_time}.csv"

    # Mở tệp CSV để ghi
    with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
        # Tạo đối tượng ghi CSV
        csv_writer = csv.writer(csvfile)

        # Ghi dữ liệu vào tệp CSV
        for item in data:
            csv_writer.writerow([item])  # Mỗi phần tử trong danh sách sẽ được ghi trên một dòng mới

    print(f"Tạo tệp {file_name} thành công!")

def create_edgedriver(edgeOptions=None): #khởi tạo Edge_Driver 
    if edgeOptions is None:
        edgeOptions = webdriver.EdgeOptions()
        
    edgeOptions.add_argument('--enable-chrome-browser-cloud-management')
    # edgeOptions.add_argument('--window-size=1920,1080')  # Use desktop size
    # edgeOptions.add_argument('--headless')
    edgeOptions.add_argument("--test-third-party-cookie-phaseout")
    edgeOptions.add_argument('log-level=3')
    return webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=edgeOptions)

def defaultconnectdriver(proxy_data = None):
    options = webdriver.EdgeOptions()

    if proxy_data:
        proxy = f"{proxy_data['IP Address']}:{proxy_data['Port']}"
        options.add_argument(f'--proxy-server={proxy}')
    
    driver = create_edgedriver(options)
    driver.maximize_window()
    return driver

def headlessconnectdriver(proxy_data = None): # sử dụng chế độ headless trong quá trình crawl
    options = webdriver.EdgeOptions()
    options.add_argument('--headless')
    options.add_argument('--window-size=1920,1080')  # Use desktop size

    if proxy_data:
        proxy = f"{proxy_data['IP Address']}:{proxy_data['Port']}"
        options.add_argument(f'--proxy-server={proxy}')

    driver = create_edgedriver(options)
    return driver

def get_extension_list(folder_path): #folder_path là đường dẫn tới list extension cho driver sử dụng trong lúc crawl. Hàm này giúp chương trình crawl có thể sử dụng Extension của Edge.
    extension_list = []
    # Kiểm tra xem folder_path có tồn tại không
    if os.path.exists(folder_path):
        # Duyệt qua tất cả các tệp trong thư mục
        for file_name in os.listdir(folder_path):
            # Tạo đường dẫn tuyệt đối đến tệp
            file_path = os.path.join(folder_path, file_name)
            # Kiểm tra xem tệp có phải là một file không
            if os.path.isfile(file_path):
                # Lấy phần mở rộng của tệp
                _, file_extension = os.path.splitext(file_name)
                # Kiểm tra xem phần mở rộng có là .crx không
                if file_extension == ".crx":
                    # Thêm đường dẫn tuyệt đối của tệp vào danh sách nếu là một file .crx
                    extension_list.append(file_path)
    return extension_list

def connectdriver(i,subfolder_paths, proxy_data = None): #chế độ crawl cho phép thực hiện tải các file tại vị trí thư mục quy định. Nếu code crawl có phải thực hiện tải file thì sử dụng hàm này.
    options = webdriver.EdgeOptions()
    prefs = {"download.default_directory": subfolder_paths[i]}
    options.add_experimental_option("prefs", prefs)
    # options.add_argument("enable-automation")
    # options.add_argument("--no-sandbox")
    # options.add_argument("--dns-prefetch-disable")
    # options.add_argument("--disable-gpu")

    if proxy_data:
        proxy = f"{proxy_data['IP Address']}:{proxy_data['Port']}"
        options.add_argument(f'--proxy-server={proxy}')

    driver_extension_folder_path = get_folder_path(r"driver_extension")
    extension_list = get_extension_list(driver_extension_folder_path)
    for extension in extension_list:
        options.add_extension(extension)
    # chromeOptions.add_argument("--headless=new")
    driver = create_edgedriver(options)
    driver.maximize_window()
    return driver

# Get free proxies for rotating
def get_free_proxies(driver):
    driver.get('https://sslproxies.org')

    table = driver.find_element(By.TAG_NAME, 'table')
    thead = table.find_element(By.TAG_NAME, 'thead').find_elements(By.TAG_NAME, 'th')
    tbody = table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')

    headers = []
    for th in thead:
        headers.append(th.text.strip())

    proxies = []
    for tr in tbody:
        proxy_data = {}
        tds = tr.find_elements(By.TAG_NAME, 'td')
        for i in range(len(headers)):
            proxy_data[headers[i]] = tds[i].text.strip()
        proxies.append(proxy_data)
    
    return proxies[:30]

def check_csv(filename='sampleproxies.csv'):

    if not os.path.exists(filename):
        write_proxies_to_csv()
        return
    
    with open(filename, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header row
        row_count = sum(1 for row in reader)

    if row_count <= 1:
        write_proxies_to_csv()
    
    return

def write_proxies_to_csv(filename='sampleproxies.csv'):

    driver = headlessconnectdriver()
    proxies = get_free_proxies(driver)
    file_exists = os.path.exists(filename)
    with open(filename, 'a', newline='') as csvfile:
        fieldnames = proxies[0].keys() if proxies else []  # Sử dụng keys của dictionary đầu tiên trong danh sách proxies làm tên cột
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Nếu file chưa tồn tại, viết tiêu đề của các cột
        if not file_exists:
            writer.writeheader()

        # Viết dữ liệu cho mỗi proxy vào file CSV
        for proxy in proxies:
            writer.writerow(proxy)

def get_1_proxy_data(filename='sampleproxies.csv'):
    # Kiểm tra xem file đã tồn tại hay không
    if not os.path.exists(filename):
        print("File not found!")
        return None

    with open(filename, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        data = list(reader)

    # Lấy dữ liệu của dòng cuối cùng
    if data:
        proxy_data = data[-1]
    else:
        print("File is empty!")
        return None

    # Xóa dòng cuối cùng khỏi danh sách
    data = data[:-1]

    # Ghi lại nội dung mới vào file CSV
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = proxy_data.keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Viết tiêu đề của các cột
        writer.writeheader()

        # Viết lại dữ liệu cho mỗi proxy vào file CSV
        for row in data:
            writer.writerow(row)

    return proxy_data

# write_proxies_to_csv()

# # Sử dụng hàm get_proxy_data để lấy dữ liệu của dòng cuối cùng từ file CSV
# proxy_data = get_1_proxy_data()
# if proxy_data:
#     print("Proxy data:", proxy_data)
# else:
#     print("Failed to get proxy data or file is empty.")

def save_to_file(data, filename):
    """
    Lưu trữ dữ liệu vào tệp tin.
    """
    # Kiểm tra xem tệp tin đã tồn tại hay chưa
    file_exists = os.path.exists(filename)

    # Mở tệp tin ở chế độ 'a' để ghi tiếp vào cuối tệp, hoặc 'w' nếu tệp không tồn tại
    with open(filename, 'a' if file_exists else 'w') as file:
        # Ghi mỗi mục trong dữ liệu vào tệp tin, mỗi mục trên một dòng
        for item in data:
            file.write(item + '\n')