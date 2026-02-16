import requests
import json

# Константы из вашего файла коды.txt
SELLER_ID = "1439429"
AGENT_ID = "1439429"
API_KEY = "7757E1B2A8B74B11ADD1403764506273"

def get_products():
    url = "https://api.digiseller.ru/api/goods/list"
    params = {"seller_id": SELLER_ID, "currency": "RUR", "lang": "ru-RU", "rows": 100}
    headers = {"token": API_KEY, "Accept": "application/json"}

    try:
        r = requests.get(url, params=params, headers=headers, timeout=20)
        data = r.json()
        rows = data.get('rows', [])
        products = []
        for item in rows:
            products.append({
                "id": str(item['id']),
                "name": item['name'],
                "price": int(item['price_rur']),
                "cat": "games", # Можно добавить логику сортировки по имени
                "img": item.get('preview_img_url') or "https://placehold.co/500x300",
                "link": f"https://www.digiseller.market/asp2/pay_wm.asp?id_d={item['id']}&ai={AGENT_ID}"
            })
        return products
    except Exception as e:
        print(f"Ошибка API: {e}")
        return []

if __name__ == "__main__":
    items = get_products()
    if items:
        with open('products.json', 'w', encoding='utf-8') as f:
            json.dump(items, f, ensure_ascii=False, indent=4)
        print(f"Обновлено: {len(items)} товаров.")
