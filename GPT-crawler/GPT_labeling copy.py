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
csv_file = r"E:\PBL-7\GPT-crawler\raw_data_copy_2.csv"
column_index = 1  # Cột thứ hai (0-indexed)

data_list = extract_column_data(csv_file, column_index)


# --------------------------------------------------------------------------------------------------------------------------------------------------

opt =  webdriver.ChromeOptions()
opt.add_experimental_option("debuggerAddress","localhost:8989")
driver = webdriver.Chrome(options = opt)
driver.get("https://chat.openai.com/c/42a50c03-8db5-4790-85f8-5367d934d6a2")
# driver.get("https://chat.openai.com/c/a3154972-ec02-4faa-915d-1edfb8405e34")
# driver.get("https://chat.openai.com/c/e395d708-ba29-4761-a281-806de7630e10")
# driver.get("https://chat.openai.com/c/9ffa57ba-91db-4f5b-8d9f-6e0b036d78ae")
time.sleep(15)
evaluate_text = "Rồi, câu tiếp theo. "

prompt_text = "Tên riêng là danh từ chỉ định một cá thể hoặc đối tượng cụ thể, phân biệt nó với các cá thể hoặc đối tượng khác cùng loại. Tên riêng thường được sử dụng để gọi hoặc để xác định danh tính của một ai đó hoặc một cái gì đó. Đồng thời, tên riêng thường được viết hoa chữ cái đầu tiên trong tiếng Việt. Thật vậy,  hãy lấy ra kết quả chỉ bao gồm CÁC TÊN RIÊNG của con người, địa lý hoặc dịa danh nằm trong văn bản sau (không phải tên riêng thì chắc chắn không phải kết quả): "
tail_text = " (một câu hoàn toàn có thể không có kết quả hợp lệ nào)"
for item in data_list:

    content_text = item
    
    end_message = evaluate_text + prompt_text  + content_text + tail_text
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
    random_wait_time = random.randint(45, 60)
    time.sleep(random_wait_time)


time.sleep(10)

# print(result_list)
