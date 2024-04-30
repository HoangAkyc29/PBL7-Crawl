import pandas as pd

# Mở file txt
with open('textdata_3.txt', 'r', encoding='utf-8') as f:
  lines = f.readlines()

# Khởi tạo danh sách rỗng để lưu trữ dữ liệu
data = []
ano_chat = []
GPT_chat = []
# Xử lý từng dòng trong file
for line in lines:
  # Loại bỏ ký tự dòng mới
  line = line.strip()
  
  # Xác định speaker
  if line == 'Anonymous' or line == 'ChatGPT':
    speaker = line
  else:
    if speaker == 'Anonymous':
        ano_chat.append(line)
    elif speaker == 'ChatGPT':
        GPT_chat.append(line)

print(len(ano_chat))
print(len(GPT_chat))
for i in range(len(GPT_chat)):
    data.append([ano_chat[i],GPT_chat[i]])
# Chuyển đổi dữ liệu sang DataFrame
df = pd.DataFrame(data, columns=['Anonymous', 'ChatGPT'])

# Lưu DataFrame sang file csv
df.to_csv('data2.csv', index=False)