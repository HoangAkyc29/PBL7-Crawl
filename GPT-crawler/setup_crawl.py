import csv
import os
def convert_text_to_csv(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    conversations = []
    current_conversation = []
    current_speaker = None
    
    for line in lines:
        line = line.strip()
        if line.startswith("Anonymous"):
            if current_speaker == "ChatGPT":
                conversations.append((" ".join(current_conversation), ""))
                current_conversation = []
            current_speaker = "Anonymous"
        elif line.startswith("ChatGPT"):
            if current_speaker == "Anonymous":
                conversations.append(("", " ".join(current_conversation)))
                current_conversation = []
            current_speaker = "ChatGPT"
        else:
            current_conversation.append(line)
    
    # Add the last conversation
    if current_speaker == "Anonymous":
        conversations.append((" ".join(current_conversation), ""))
    elif current_speaker == "ChatGPT":
        conversations.append(("", " ".join(current_conversation)))
    
    # Write to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Anonymous", "ChatGPT"])
        for conversation in conversations:
            writer.writerow(conversation)

def save_to_file(data, filename, foldername=None):
    """
    Lưu trữ dữ liệu vào tệp tin và trả về đường dẫn của tệp.
    """
    # Xác định đường dẫn của tệp tin
    if foldername:
        # Kiểm tra và tạo thư mục đích nếu nó không tồn tại
        if not os.path.exists(foldername):
            os.makedirs(foldername)

        filepath = os.path.join(foldername, filename)
    else:
        filepath = filename

    # Kiểm tra sự tồn tại của tệp tin
    file_exists = os.path.exists(filepath)

    # Mở tệp tin ở chế độ 'a' để ghi tiếp vào cuối tệp, hoặc 'w' nếu tệp không tồn tại
    with open(filepath, 'a' if file_exists else 'w', encoding="utf-8") as file:
        # Ghi mỗi mục trong dữ liệu vào tệp tin, mỗi mục trên một dòng
        for item in data:
            file.write(item + '\n')
    
    file_path = os.path.abspath(filepath)

    return file_path

# Sử dụng hàm để chuyển đổi từ file text sang file CSV
# convert_text_to_csv("conversation.txt", "conversation.csv")
