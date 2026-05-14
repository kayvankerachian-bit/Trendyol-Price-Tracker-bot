from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import requests
import time
import random
import os
from dotenv import load_dotenv

load_dotenv()

CATEGORY_URL = "https://www.trendyol.com/sr?pr=4.5&rd=true&hsm=true&fc=true&qt=nemlendirici%20y%C3%BCz%20kremi&st=nemlendirici%20y%C3%BCz%20kremi&os=1&q=nemlendirici%20y%C3%BCz%20kremi&pi=3"

TARGET_PRODUCT_ID = "757559672"

TOKEN = os.getenv("BOT_TOKEN")

CHAT_IDS = ["97362428", "104973163"]


def send_telegram(message):

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    for chat_id in CHAT_IDS:

        requests.post(
            url,
            data={
                "chat_id": chat_id,
                "text": message
            }
        )


def check_product():

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox"]
        )

        page = browser.new_page()

        page.goto(CATEGORY_URL)

        time.sleep(5)

        # 10 scroll
        for i in range(10):

            for _ in range(5):

                page.mouse.wheel(0, 300)

                time.sleep(random.uniform(0.3, 0.8))

            print(f"Scroll {i+1}")

            time.sleep(random.uniform(2, 4))

        html = page.content()

        soup = BeautifulSoup(html, "html.parser")

        products = soup.find_all("a")

        found = False

        for product in products:

            href = product.get("href")

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

        browser.close()


while True:

    check_product()

    print("⏳ Waiting 2 hours...")

    time.sleep(7200)