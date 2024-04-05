import csv

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

# Sử dụng hàm để chuyển đổi từ file text sang file CSV
convert_text_to_csv("conversation.txt", "conversation.csv")
