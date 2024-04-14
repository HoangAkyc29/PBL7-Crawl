import requests
import json

TRANSLATION_ERROR = "Lỗi dịch"
TRANSLATION_PROVIDER = "Google Translate"
GET_API_KEY_FROM = "https://console.cloud.google.com/marketplace/product/google/translate.googleapis.com"

languages = [
    "Afrikaans", "Albanian", "Amharic", "Arabic", "Armenian", "Azerbaijani", "Basque", "Belarusian", "Bengali",
    "Bosnian", "Bulgarian", "Catalan", "Cebuano", "Chichewa", "Chinese (Simplified)", "Chinese (Traditional)",
    "Corsican", "Croatian", "Czech", "Danish", "Dutch", "English", "Esperanto", "Estonian", "Filipino", "Finnish",
    "French", "Frisian", "Galician", "Georgian", "German", "Greek", "Gujarati", "Haitian Creole", "Hausa",
    "Hawaiian", "Hebrew", "Hindi", "Hmong", "Hungarian", "Icelandic", "Igbo", "Indonesian", "Irish", "Italian",
    "Japanese", "Javanese", "Kannada", "Kazakh", "Khmer", "Kinyarwanda", "Korean", "Kurdish (Kurmanji)", "Kyrgyz",
    "Lao", "Latin", "Latvian", "Lithuanian", "Luxembourgish", "Macedonian", "Malagasy", "Malay", "Malayalam",
    "Maltese", "Maori", "Marathi", "Mongolian", "Myanmar (Burmese)", "Nepali", "Norwegian", "Odia (Oriya)", "Pashto",
    "Persian", "Polish", "Portuguese", "Punjabi", "Romanian", "Russian", "Samoan", "Scots Gaelic", "Serbian",
    "Sesotho", "Shona", "Sindhi", "Sinhala", "Slovak", "Slovenian", "Somali", "Spanish", "Sundanese", "Swahili",
    "Swedish", "Tajik", "Tamil", "Tatar", "Telugu", "Thai", "Turkish", "Turkmen", "Ukrainian", "Urdu", "Uyghur",
    "Uzbek", "Vietnamese", "Welsh", "Xhosa", "Yiddish", "Yoruba", "Zulu"
]

def translate_text(text, translate_from, translate_to, auth_key=None):
    if auth_key:
        url = f"https://translation.googleapis.com/language/translate/v2?format=text&target={translate_to}&key={auth_key}"
        data = {"q": [text], "source": translate_from}
        response = requests.post(url, json=data)
        if response.status_code == 200:
            translation = json.loads(response.text)["data"]["translations"][0]["translatedText"]
            return True, translation
        else:
            return False, f"{TRANSLATION_ERROR}: {response.text}"
    else:
        url = f"https://translate.google.com/m?sl={translate_from}&tl={translate_to}&q={text}"
        response = requests.get(url)
        if response.status_code == 200:
            start = response.text.find("result-container\">") + 18
            end = response.text.find('<', start)
            translation = response.text[start:end]
            return True, translation
        else:
            return False, f"{TRANSLATION_ERROR}: {response.text}"

def main():
    text_to_translate = "Hello, how are you ?"
    translate_from = "en"
    translate_to = "vi"
    auth_key = None  # Thay thế bằng khóa API của bạn nếu có
    success, translated_text = translate_text(text_to_translate, translate_from, translate_to, auth_key)
    if success:
        print("Câu đã dịch:", translated_text)
    else:
        print("Đã xảy ra lỗi:", translated_text)

if __name__ == "__main__":
    main()
