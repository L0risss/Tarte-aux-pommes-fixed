import requests
import json
import os

# Lire les variables d'environnement
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

print(f"[DEBUG] TELEGRAM_TOKEN: {TELEGRAM_TOKEN}")
print(f"[DEBUG] TELEGRAM_CHAT_ID: {TELEGRAM_CHAT_ID}")

# Fichier des filtres
FILTERS_FILE = "filters.json"
SEEN_FILE = "seen.json"

def load_filters():
    with open(FILTERS_FILE, "r") as f:
        return json.load(f)

def load_seen():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, "r") as f:
            return set(json.load(f))
    return set()

def save_seen(seen_ids):
    with open(SEEN_FILE, "w") as f:
        json.dump(list(seen_ids), f)

def send_telegram(message):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("[ERROR] Missing TELEGRAM_TOKEN or CHAT_ID")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"}

    print("[DEBUG] Sending Telegram message...")
    response = requests.post(url, data=data)
    print(f"[DEBUG] Telegram response: {response.status_code} {response.text}")

def fake_scrape(filter_data):
    return [{
        "id": f"{filter_data['keyword']}_test123",
        "title": f"Test - {filter_data['keyword']}",
        "price": "$1,000",
        "url": "https://facebook.com/marketplace/item/123456"
    }]

def run():
    filters = load_filters()
    seen_ids = load_seen()
    new_announcements = []

    for f in filters:
        results = fake_scrape(f)
        for item in results:
            if item["id"] not in seen_ids:
                seen_ids.add(item["id"])
                new_announcements.append(item)
                msg = f"<b>{item['title']}</b>\nPrix : {item['price']}\n<a href='{item['url']}'>Voir l'annonce</a>"
                send_telegram(msg)

    save_seen(seen_ids)

if __name__ == "__main__":
    run()
