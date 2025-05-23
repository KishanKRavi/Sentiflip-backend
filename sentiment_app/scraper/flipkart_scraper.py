# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.by import By
# import time
# import json
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# def search_product(query):
#     options = webdriver.ChromeOptions()
#     options.add_argument('--headless')
#     options.add_argument('--no-sandbox')
#     options.add_argument('--disable-dev-shm-usage')

#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

#     try:
#         driver.get(f"https://www.flipkart.com/search?q={query}")

#         # Wait until at least one product loads (max 10 seconds)
#         WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.XPATH, '//*[contains(@class, "tUxRFH") or contains(@class,"_75nlfW")]'))
#         )

#         items = driver.find_elements(By.XPATH, '//*[contains(@class, "tUxRFH") or contains(@class,"_75nlfW")]')

#         products = []
#         seen = set()  # ✅ To keep track of (title, link) and avoid duplicates

#         for item in items:
#             title_elem = item.find_elements(By.XPATH, './/*[contains(@class, "KzDlHZ") or contains(@class, "wjcEIp") or contains(@class,"BwBZTg")]')
#             img_elem = item.find_elements(By.XPATH, './/*[contains(@class, "DByuf4") or contains(@class, "_53J4C-")]')
#             link_elem = item.find_elements(By.XPATH, './/*[contains(@class, "CGtC98") or contains(@class, "VJA3rP") or contains(@class,"rPDeLR")]')
#             price_elem = item.find_elements(By.XPATH, './/*[contains(@class, "Nx9bqj")]')
#             ratings_elem = item.find_elements(By.XPATH, './/*[contains(@class, "XQDdHH")]')
#             brandname_elem = item.find_elements(By.XPATH, './/*[contains(@class, "syl9yP")]')

#             if title_elem and price_elem and img_elem and link_elem:
#                 title = title_elem[0].text.strip()
#                 link = link_elem[0].get_attribute("href")

#                 if (title, link) not in seen:  # ✅ Only add if not seen before
#                     seen.add((title, link))

#                     product = {
#                         "Title": title,
#                         "Image": img_elem[0].get_attribute("src"),
#                         "Link": link,
#                         "Price": price_elem[0].text.strip(),
#                         "Ratings": ratings_elem[0].text.strip() if ratings_elem else "",
#                         "Brand": brandname_elem[0].text.strip() if brandname_elem else ""
#                     }
#                     products.append(product)

#         if products:
#             return products
#         else:
#             print("⚠️ No products found.")
#             return []

#     finally:
#         driver.quit()

# # /reviews scraping
# def safe_find_text(item, by, value):
#     try:
#         return item.find_element(by, value).text
#     except:
#         return ""

# def getReviews(driver, urls, page):
#     urls = urls.replace("/p/", "/product-reviews/")  
#     url = f"{urls}&page={page}"
#     print(f"Scraping URL: {url}")
#     driver.get(url)

#     reviews = []
#     items = driver.find_elements(By.XPATH, './/*[contains(@class, "EPCmJX")]')  

#     for item in items:
#         rating = safe_find_text(item, By.CLASS_NAME, "XQDdHH")
#         reviewHeading = safe_find_text(item, By.XPATH, './/div[contains(@class, "_11pzQk") or contains(@class,"z9E0IG")]')
#         reviewText = safe_find_text(item, By.CLASS_NAME, "ZmyHeo")
#         userName = safe_find_text(item, By.XPATH, './/p[contains(@class,"_2NsDsF") or contains(@class,"AwS1CA") or contains(@class,"MDcJkH")]')

#         if rating or reviewHeading or reviewText or userName:
#             reviews.append({
#                 "Rating": rating,
#                 "Review_Heading": reviewHeading,
#                 "Review_Text": reviewText,
#                 "User_Name": userName,
#             })

#     return reviews

# def reviewAllPages(urls, max_pages=5):
#     # Set up Chrome options
#     options = webdriver.ChromeOptions()
#     options.add_argument("--headless")  
#     options.add_argument("--disable-blink-features=AutomationControlled")
#     options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

#     # Initialize WebDriver once
#     service = Service(ChromeDriverManager().install())
#     driver = webdriver.Chrome(service=service, options=options)
    
#     all_reviews = []
#     for page in range(1, max_pages + 1):
#         reviews = getReviews(driver, urls, page)
#         if not reviews:
#             break  # Stop if no reviews found on a page
#         all_reviews.extend(reviews)

#     driver.quit()
#     print(f"Total reviews collected: {len(all_reviews)}")
#     return all_reviews


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

# Chrome binary paths (used in Docker/Render)
CHROMEDRIVER_PATH = "/usr/bin/chromedriver"
CHROME_BINARY_PATH = "/usr/bin/chromium"

def configure_driver():

    
    options = webdriver.ChromeOptions()
    options.binary_location = CHROME_BINARY_PATH
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=options)

def search_product(query):
    driver = configure_driver()

    try:
        driver.get(f"https://www.flipkart.com/search?q={query}")

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[contains(@class, "tUxRFH") or contains(@class,"_75nlfW")]'))
        )

        items = driver.find_elements(By.XPATH, '//*[contains(@class, "tUxRFH") or contains(@class,"_75nlfW")]')

        products = []
        seen = set()

        for item in items:
            title_elem = item.find_elements(By.XPATH, './/*[contains(@class, "KzDlHZ") or contains(@class, "wjcEIp") or contains(@class,"BwBZTg")]')
            img_elem = item.find_elements(By.XPATH, './/*[contains(@class, "DByuf4") or contains(@class, "_53J4C-")]')
            link_elem = item.find_elements(By.XPATH, './/*[contains(@class, "CGtC98") or contains(@class, "VJA3rP") or contains(@class,"rPDeLR")]')
            price_elem = item.find_elements(By.XPATH, './/*[contains(@class, "Nx9bqj")]')
            ratings_elem = item.find_elements(By.XPATH, './/*[contains(@class, "XQDdHH")]')
            brandname_elem = item.find_elements(By.XPATH, './/*[contains(@class, "syl9yP")]')

            if title_elem and price_elem and img_elem and link_elem:
                title = title_elem[0].text.strip()
                link = link_elem[0].get_attribute("href")

                if (title, link) not in seen:
                    seen.add((title, link))
                    product = {
                        "Title": title,
                        "Image": img_elem[0].get_attribute("src"),
                        "Link": link,
                        "Price": price_elem[0].text.strip(),
                        "Ratings": ratings_elem[0].text.strip() if ratings_elem else "",
                        "Brand": brandname_elem[0].text.strip() if brandname_elem else ""
                    }
                    products.append(product)

        return products if products else []

    finally:
        driver.quit()

def safe_find_text(item, by, value):
    try:
        return item.find_element(by, value).text
    except:
        return ""

def getReviews(driver, urls, page):
    urls = urls.replace("/p/", "/product-reviews/")
    url = f"{urls}&page={page}"
    print(f"Scraping URL: {url}")
    driver.get(url)

    reviews = []
    items = driver.find_elements(By.XPATH, './/*[contains(@class, "EPCmJX")]')

    for item in items:
        rating = safe_find_text(item, By.CLASS_NAME, "XQDdHH")
        reviewHeading = safe_find_text(item, By.XPATH, './/div[contains(@class, "_11pzQk") or contains(@class,"z9E0IG")]')
        reviewText = safe_find_text(item, By.CLASS_NAME, "ZmyHeo")
        userName = safe_find_text(item, By.XPATH, './/p[contains(@class,"_2NsDsF") or contains(@class,"AwS1CA") or contains(@class,"MDcJkH")]')

        if rating or reviewHeading or reviewText or userName:
            reviews.append({
                "Rating": rating,
                "Review_Heading": reviewHeading,
                "Review_Text": reviewText,
                "User_Name": userName,
            })

    return reviews

def reviewAllPages(urls, max_pages=5):
    driver = configure_driver()

    all_reviews = []
    for page in range(1, max_pages + 1):
        reviews = getReviews(driver, urls, page)
        if not reviews:
            break
        all_reviews.extend(reviews)

    driver.quit()
    print(f"Total reviews collected: {len(all_reviews)}")
    return all_reviews
