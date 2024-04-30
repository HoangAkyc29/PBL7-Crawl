from textblob import TextBlob

review = "it's great"
review2 = "it's kind"
review3 = "Everyone know it's good"
review4 = "it's thoughtful"

blob = TextBlob(review)
blob2 = TextBlob(review2)
blob3 = TextBlob(review3)
blob4 = TextBlob(review4)
blob.sentiment
print(blob.sentiment)
print(blob2.sentiment)
print(blob3.sentiment)
print(blob4.sentiment)