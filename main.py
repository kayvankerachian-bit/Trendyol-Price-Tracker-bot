from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import requests
import time

CATEGORY_URL = "https://www.trendyol.com/sr?pr=4.5&rd=true&hsm=true&fc=true&qt=nemlendirici%20y%C3%BCz%20kremi&st=nemlendirici%20y%C3%BCz%20kremi&os=1&q=nemlendirici%20y%C3%BCz%20kremi&pi=3"

TARGET_PRODUCT_ID = "757559672"

TOKEN = "8646827527:AAFtIPqJiG78Hw2ragVaDSTEhd82SCgD5lg"
CHAT_IDS = ["97362428","104973163"]


def send_telegram(message):

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    for chat_id in CHAT_IDS:

        requests.post(url, data={
            "chat_id": chat_id,
            "text": message
        })


def check_product():

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install())
    )

    driver.get(CATEGORY_URL)

    time.sleep(5)

    # 10 scroll
    import random

    for i in range(10):

        for _ in range(5):

            driver.execute_script(
            f"window.scrollBy(0, 300);"
        )
            time.sleep(random.uniform(0.3,0.8))

    print(f"Scroll {i+1}")

    time.sleep(random.uniform(2, 4))

    products = driver.find_elements(By.TAG_NAME, "a")

    found = False

    for product in products:

        href = product.get_attribute("href")

        print(href)

        if href and TARGET_PRODUCT_ID in href:

            found = True

            print("✅ Product Found")

            break

    if not found:

        print("⚠️ Product NOT Found")

        send_telegram(
            "⚠️ Orasense محصول از 10 اسکرول اول خارج شد"
        )

    driver.quit()


while True:

    check_product()

    print("⏳ Waiting 2 hours...")

    time.sleep(7200)