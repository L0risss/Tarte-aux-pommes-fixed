import requests
from bs4 import BeautifulSoup
import json
import os

# Variables Telegram
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Fichier des filtres
FILTERS_FILE = "filters.json"
SEEN_FILE = "seen.json"

# Lire les filtres
def load_filters():
    with open(FILTERS_FILE, "r") as f:
        return json.load(f)

# Lire les annonces déjà vues
def load_seen():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, "r") as f:
            return set(json.load(f))
    return set()

# Enregistrer les annonces vues
def save_seen(seen_ids):
    with open(SEEN_FILE, "w") as f:
        json.dump(list(seen_ids), f)

# Envoyer une alerte Telegram
def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"}
    requests.post(url, data=data)

# Fonction de scraping simulée (Facebook bloque le scraping direct)
def fake_scrape(filter_data):
    # Simule une nouvelle annonce
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
