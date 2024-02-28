from setup_crawl import get_free_proxies, connectdriver, headlessconnectdriver, defaultconnectdriver, get_extension_list, create_1D_csv_file
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
def scrape_tourist_destination_data(url):

    # subfolder = ["tourist_destination_data"]

    try:
        driver = headlessconnectdriver()

        driver.get(url)
        driver.implicitly_wait(5)  # Đợi 5 giây để load trang
        # Đặt điều kiện chờ (chờ tối đa 5 giây)
        wait = WebDriverWait(driver, 5)

        div_element = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "col-xs-12.text-center")))

        # Tìm nút trong thẻ div
        button = div_element.find_element(By.CLASS_NAME, "btn.btn-default.btn-more.btn-more-cruise")

        # Vòng lặp nhấn vào nút cho đến khi nút biến mất
        while button.is_displayed():
            try:
                button.click()
                time.sleep(2)
                div_element = wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "col-xs-12.text-center")))
                # Tìm nút trong thẻ div
                button = div_element.find_element(By.CLASS_NAME, "btn.btn-default.btn-more.btn-more-cruise")
            except Exception as e:
                break

        # Chờ cho thẻ div có class là list_search__item__img xuất hiện trên trang web
        # Tìm tất cả các thẻ div có class là list_search__item__img
        # div_elements = WebDriverWait(driver, 10).until(
        #     EC.presence_of_all_elements_located((By.CLASS_NAME, "list_search__item__img")))

        # # Lặp qua từng phần tử div và lấy nội dung của thuộc tính onclick
        # for div_element in div_elements:
        #     onclick_content = div_element.get_attribute("onclick")
        #     print("Nội dung của onclick:", onclick_content)

        # Chờ cho tất cả các thẻ div có class là "why_book collapsed" xuất hiện
        div_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.why_book.collapsed"))
        )

        # Vòng lặp nhấn vào tất cả các thẻ div
        for div_element in div_elements:
            try:
                div_element.click()
            except Exception as e:
                continue
        # Tìm tất cả các phần tử có class là "list_search__item__info__why_book panel-collapse collapse"
        why_book_elements = driver.find_elements(By.CLASS_NAME, "list_search__item__info__why_book.panel-collapse.collapse.in")

        # Khởi tạo danh sách để lưu trữ nội dung của các phần tử <li>
        text_content_list = []

        # Lặp qua từng phần tử why_book
        for why_book_element in why_book_elements:
            try:
                # Tìm tất cả các phần tử <li> bên trong phần tử why_book_element
                li_elements = why_book_element.find_elements(By.TAG_NAME, "li")
                
                # Lặp qua từng phần tử <li> và thêm nội dung của chúng vào danh sách
                for li_element in li_elements:
                    text_content_list.append(li_element.text.strip())
            except Exception as e:
                print("Đã xảy ra lỗi khi tìm phần tử <li>:", str(e))
                continue

        return text_content_list
            
    except Exception as e:
        print(f"Lỗi. {e}")
        driver.quit()
        return None

# print(scrape_tourist_destination_data("https://www.bestpricetravel.com/vietnam-tours"))
create_1D_csv_file(scrape_tourist_destination_data("https://www.bestpricetravel.com/vietnam-tours"))