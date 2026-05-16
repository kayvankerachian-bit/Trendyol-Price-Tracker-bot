from playwright.sync_api import sync_playwright
import requests
import time
import random
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

CHAT_IDS = ["97362428", "104973163"]

TASKS = [

    {
        "name": "Orasense Cream",
        "url": "https://www.trendyol.com/sr?pr=4.5&rd=true&hsm=true&fc=true&qt=nemlendirici%20y%C3%BCz%20kremi&st=nemlendirici%20y%C3%BCz%20kremi&os=1&q=nemlendirici%20y%C3%BCz%20kremi&pi=3",
        "keyword": "safran özlü"
    },

    {
        "name": "Goz Krem",
        "url": "https://www.trendyol.com/sr?wc=144686&pr=4.5&lc=144686&rd=true&hsm=true&fc=true&os=1",
        "keyword": "%1 safran özü"
    },

    {
        "name": "Mask",
        "url": "https://www.trendyol.com/sr?pr=4.5&rd=true&hsm=true&fc=true&qt=y%C3%BCz%20maskesi&st=y%C3%BCz%20maskesi&os=1&q=y%C3%BCz%20maskesi&pi=2",
        "keyword": "%5 safran özü"
    },

    {
        "name": "Yuz Temizleme Jeli",
        "url": "https://www.trendyol.com/sr?pr=4.5&hsm=true&rd=true&fc=true&qt=y%C3%BCz%20temizleme%20jeli&st=y%C3%BCz%20temizleme%20jeli&os=1&q=y%C3%BCz%20temizleme%20jeli&pi=3",
        "keyword": "%0.3 safran özü"
    },

    {
        "name": "Serum",
        "url": "https://www.trendyol.com/sr?pr=4.5&rd=true&hsm=true&fc=true&qt=y%C3%BCz%20serumu&st=y%C3%BCz%20serumu&os=1&q=y%C3%BCz%20serumu&pi=4",
        "keyword": "safran özlü"
    },

    {
        "name": "Set",
        "url": "https://www.trendyol.com/sr?pr=4.5&rd=true&hsm=true&fc=true&qt=bak%C4%B1m%20seti&st=bak%C4%B1m%20seti&os=1&q=bak%C4%B1m%20seti",
        "keyword": "safran özlü"
    }

]


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


def check_product(page, task):

    page.goto(task["url"])

    time.sleep(random.uniform(5, 8))

    # human-like mouse move
    page.mouse.move(
        random.randint(100, 500),
        random.randint(100, 500)
    )

    # stronger scrolling
    for i in range(15):

        page.mouse.wheel(0, 2500)

        print(f"{task['name']} Scroll {i+1}")

        page.wait_for_timeout(
            random.randint(2000, 4000)
        )

    page.wait_for_timeout(5000)

    # get product cards
    cards = page.locator(
        '[data-testid="product-card"]'
    )

    count = cards.count()

    print(f"{count} cards found")

    for i in range(count):

        try:

            card_text = cards.nth(i).inner_text().lower()

            print(card_text)

            if task["keyword"].lower() in card_text:

                print(f"✅ {task['name']} FOUND")

                return True

        except Exception as e:

            print(e)

    print(f"❌ {task['name']} NOT FOUND")

    return False


while True:

    results = []

    with sync_playwright() as p:

        browser = p.chromium.launch(

            headless=True,

            args=[
                "--no-sandbox",
                "--disable-blink-features=AutomationControlled"
            ]
        )

        page = browser.new_page(

            viewport={
                "width": 1280,
                "height": 900
            },

            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )

        for task in TASKS:

            try:

                found = check_product(page, task)

                if found:

                    results.append(
                        f"✅ {task['name']}"
                    )

                else:

                    results.append(
                        f"❌ {task['name']}"
                    )

                # pause between tasks
                time.sleep(
                    random.uniform(15, 30)
                )

            except Exception as e:

                print(e)

                results.append(
                    f"⚠️ ERROR - {task['name']}"
                )
        browser.close()

    final_message = "📊 Trendyol Monitor Report\n\n"

    final_message += "\n".join(results)

    send_telegram(final_message)

    print(final_message)

    print("⏳ Waiting 2 hours...")

    time.sleep(7200)