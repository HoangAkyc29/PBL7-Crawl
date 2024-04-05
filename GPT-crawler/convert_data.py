import csv

def convert_text_to_csv(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    conversations = []
    current_conversation = {"Anonymous": "", "ChatGPT": ""}
    
    for line in lines:
        line = line.strip()
        if line.startswith("Anonymous"):
            current_conversation["Anonymous"] = line.replace("Anonymous", "").strip()
        elif line.startswith("ChatGPT"):
            current_conversation["ChatGPT"] = line.replace("ChatGPT", "").strip()
            conversations.append((current_conversation["Anonymous"], current_conversation["ChatGPT"]))
            current_conversation = {"Anonymous": "", "ChatGPT": ""}
        else:
            if current_conversation["Anonymous"]:
                current_conversation["Anonymous"] += " " + line
            elif current_conversation["ChatGPT"]:
                current_conversation["ChatGPT"] += " " + line
    
    # Write to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Anonymous", "ChatGPT"])
        for conversation in conversations:
            writer.writerow(conversation)

# Sử dụng hàm để chuyển đổi từ file text sang file CSV
convert_text_to_csv("conversation.txt", "conversation.csv")
