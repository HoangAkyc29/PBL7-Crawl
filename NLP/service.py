import csv

def save_to_csv(review_text, review_rating):
    # Mở hoặc tạo file CSV để ghi
    with open('reviews.csv', 'w', newline='', encoding='utf-8') as csvfile:
        # Định nghĩa các trường và viết tiêu đề
        fieldnames = ['Review Text', 'Review Rating']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Ghi dữ liệu từ các danh sách review_text và review_rating vào file CSV
        for text, rating in zip(review_text, review_rating):
            writer.writerow({'Review Text': text, 'Review Rating': rating})
