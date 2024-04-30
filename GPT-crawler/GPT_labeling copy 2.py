from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import csv
import random
import os
import re
def extract_column_data(csv_path, column_index):
    column_data = []
    if os.path.exists(csv_path):
        with open(csv_path, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                # Kiểm tra xem hàng có đủ cột không
                if len(row) > column_index:
                    column_data.append(row[column_index])
                else:
                    print(f"Hàng không có đủ cột: {row}")
    else:
        print(f"Đường dẫn '{csv_path}' không tồn tại.")

    return column_data

def get_lines_from_file(file_path):
    # Khai báo một danh sách để lưu trữ các dòng từ file
    data_list = []

    # Mở file và đọc các dòng vào danh sách
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            data_list.append(line.strip())

    return data_list

def remove_quotes_and_duplicates(file_path):
    # Đọc dữ liệu từ file và xóa dấu "
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
        lines = [line.replace('"', '') for line in lines] 
        lines = [line.replace('"', '').strip() for line in lines]

    # Loại bỏ các dòng trùng
    unique_lines = list(set(lines))

    # Ghi lại các dòng đã loại bỏ dấu " và trùng vào file
    with open(file_path, "w", encoding="utf-8") as file:
        file.writelines(unique_lines)

import unicodedata

def is_bmp(char):
    return ord(char) <= 0xFFFF

def preprocess_text(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()

    # Loại bỏ các ký tự không được hỗ trợ trong BMP
    text = ''.join(char for char in text if is_bmp(char))

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(text)

# Thay đổi 'file.csv' thành đường dẫn của file CSV thực tế của bạn
txt_file = r"E:\PBL-7\GPT-crawler\reviews_data.txt"
# column_index = 1  # Cột thứ hai (0-indexed)

# preprocess_text(txt_file, txt_file)

# data_list = extract_column_data(csv_file, column_index)
# remove_quotes_and_duplicates(txt_file)
data_list = get_lines_from_file(txt_file)

# --------------------------------------------------------------------------------------------------------------------------------------------------

opt =  webdriver.ChromeOptions()
opt.add_experimental_option("debuggerAddress","localhost:8989")
driver = webdriver.Chrome(options = opt)
driver.get("https://chat.openai.com/c/609f3a87-3a0a-4381-af93-ce9e6d762ce5")
# driver.get("https://chat.openai.com/c/a3154972-ec02-4faa-915d-1edfb8405e34")
# driver.get("https://chat.openai.com/c/e395d708-ba29-4761-a281-806de7630e10")
# driver.get("https://chat.openai.com/c/9ffa57ba-91db-4f5b-8d9f-6e0b036d78ae")
time.sleep(15)

evaluate_text = "Khá ổn, ok. "

prompt_text = " Tôi sẽ cung cấp ví dụ sau: Chỉ cách hồ Đà Lạt 15 phút đi xe máy, ngôi chùa này sẽ mê hoặc trí tưởng tượng của bạn hàng giờ nếu bạn dành thời gian khám phá tinh hoa của ngôi chùa và các yếu tố xung quanh, đặc biệt là đồ nội thất, đồ thủ công, cửa hàng đá liền kề và tu viện Phật giáo trên ngọn đồi phía trên. --> Kết quả: hồ, ngôi chùa, đồ nội thất, đồ thủ công, cửa hàng đá, tu viện Phật giáo.  Biết rằng kết quả là danh sách những danh từ hoặc cụm danh từ chung chỉ các thứ, các chi tiết nó về một thứ gì đó tại điểm du lịch trong câu (không được bao gồm danh từ riêng hoặc tên riêng). Một câu có thể có hoặc không có từ đặc trưng nào. Thật vậy, tương tự, hãy lấy ra kết quả  từ văn bản sau cho tôi (nếu có): "
tail_text = ""
for item in data_list:
    try:
        content_text = item
        content_text = re.sub(r"\n$", "", content_text)
        
        end_message = evaluate_text + prompt_text  + content_text + tail_text
        print(end_message)
        textarea = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "prompt-textarea")))
        # Nhập nội dung vào thẻ textarea
        textarea.clear()
        textarea.send_keys(end_message)
        random_wait_time = random.randint(6, 10)
        time.sleep(random_wait_time)
        send_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='send-button']")))
        # Chờ cho đến khi nút button xuất hiện và trở thành khả năng tương tác
        # Click vào nút button
        send_button.click()
        random_wait_time = random.randint(40, 50)
        time.sleep(random_wait_time)
    
    except:
        continue
    # bonus_message = "ngắn gọn hơn nếu có thể."
    # textarea = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "prompt-textarea")))
    # # Nhập nội dung vào thẻ textarea
    # textarea.send_keys(bonus_message)
    # random_wait_time = random.randint(3, 5)
    # time.sleep(random_wait_time)
    # send_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='send-button']")))
    # # Chờ cho đến khi nút button xuất hiện và trở thành khả năng tương tác
    # # Click vào nút button
    # send_button.click()
    # random_wait_time = random.randint(40, 50)
    # time.sleep(random_wait_time)


time.sleep(10)

# print(result_list)
