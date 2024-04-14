from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from setup_crawl import save_to_file
import time
import csv
import random
import os

# def extract_column_data(csv_path, column_index):
#     column_data = []
#     if os.path.exists(csv_path):
#         with open(csv_path, 'r', newline='', encoding='utf-8') as file:
#             reader = csv.reader(file)
#             for row in reader:
#                 # Kiểm tra xem hàng có đủ cột không
#                 if len(row) > column_index:
#                     column_data.append(row[column_index])
#                 else:
#                     print(f"Hàng không có đủ cột: {row}")
#     else:
#         print(f"Đường dẫn '{csv_path}' không tồn tại.")

#     return column_data

# Thay đổi 'file.csv' thành đường dẫn của file CSV thực tế của bạn
# csv_file = r"E:\PBL-7\GPT-crawler\raw_data.csv"
# column_index = 1  # Cột thứ hai (0-indexed)

# data_list = extract_column_data(csv_file, column_index)


# --------------------------------------------------------------------------------------------------------------------------------------------------

opt =  webdriver.ChromeOptions()
opt.add_experimental_option("debuggerAddress","localhost:8989")
driver = webdriver.Chrome(options = opt)
driver.get("https://chat.openai.com/share/23106837-f53b-4c7f-b6ca-d57ae9e6ec91")
random_wait_time = random.randint(25, 30)
time.sleep(random_wait_time)
# Xác định locator của các thẻ div
div_locator = (By.CSS_SELECTOR, "div.w-full.text-token-text-primary")

# Chờ cho đến khi tất cả các thẻ div được tải
wait = WebDriverWait(driver, 10)
divs = wait.until(EC.presence_of_all_elements_located(div_locator))

data_list = []

for div in divs:
  # Lấy dữ liệu text từ thẻ div
  data_list.append(div.text)

save_to_file(data_list, "textdata.txt")

# print(result_list)
