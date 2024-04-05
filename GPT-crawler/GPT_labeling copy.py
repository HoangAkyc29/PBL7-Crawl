from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import csv
import random
import os

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

# Thay đổi 'file.csv' thành đường dẫn của file CSV thực tế của bạn
csv_file = r"E:\PBL-7\GPT-crawler\raw_data.csv"
column_index = 1  # Cột thứ hai (0-indexed)

data_list = extract_column_data(csv_file, column_index)


# --------------------------------------------------------------------------------------------------------------------------------------------------

opt =  webdriver.ChromeOptions()
opt.add_experimental_option("debuggerAddress","localhost:8989")
driver = webdriver.Chrome(options = opt)
driver.get("https://chat.openai.com/c/b03d1c39-ac87-4da1-a1ed-25784daaac96")
time.sleep(60)
evaluate_text = "rất chuẩn, tốt lắm. "

prompt_text = "Tôi sẽ cung cấp lại ví dụ sau: #Làng nổi Tân Lập nằm sâu bên trong lòng Đồng Tháp Mười, nơi chủ yếu là vùng rừng ngập nước với hệ sinh thái mang đậm vẻ đặc trưng của Đông Nam Bộ. Tràm, sen, súng, lục bình cùng với hệ động vật cò, cá phong phú đã tạo nên cho nơi này một mảng màu sắc riêng.# --> Kết quả: làng nổi, vùng rừng ngập nước, hệ sinh thái, hệ động vật.  Biết rằng kết quả là danh sách các từ đặc trưng, với từ đặc trưng là những cụm danh từ chung (không bao gồm tên riêng và danh từ riêng) nói lên các feature tại địa điểm du lịch nằm trong câu. Một câu có thể có hoặc không có từ đặc trưng nào. Thật vậy, tương tự, hãy lấy ra các từ đặc trưng từ văn bản sau cho tôi (nếu có):"
for item in data_list:

    content_text = item
    end_message = evaluate_text + prompt_text  + content_text
    print(end_message)
    textarea = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "prompt-textarea")))
    # Nhập nội dung vào thẻ textarea
    textarea.send_keys(end_message)
    random_wait_time = random.randint(3, 5)
    time.sleep(random_wait_time)
    send_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='send-button']")))
    # Chờ cho đến khi nút button xuất hiện và trở thành khả năng tương tác
    # Click vào nút button
    send_button.click()
    random_wait_time = random.randint(55, 70)
    time.sleep(random_wait_time)


time.sleep(10)

# print(result_list)
