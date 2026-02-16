import requests
import json
import os

# Ваши актуальные данные 
SELLER_ID = "1439429"
AGENT_ID = "1439429"
API_KEY = "7757E1B2A8B74B11ADD1403764506273"

def get_products():
    print("Подключение к актуальному API Digiseller...")
    # Правильный URL для получения списка товаров
    url = "https://api.digiseller.ru/api/goods/list"
    
    params = {
        "seller_id": SELLER_ID,
        "currency": "RUR",
        "lang": "ru-RU",
        "rows": 100,
        "order": "popular"
    }
    
    headers = {
        "token": API_KEY,
        "Accept": "application/json"
    }

    try:
        r = requests.get(url, params=params, headers=headers, timeout=30)
        r.raise_for_status()
        data = r.json()
        
        rows = data.get('rows', [])
        products = []
        
        for item in rows:
            name_lower = item['name'].lower()
            # Автоматическое распределение по вашим категориям в 7.html 
            category = "games"
            if any(x in name_lower for x in ["wallet", "пополнение", "card", "gift"]):
                category = "wallets"
            elif any(x in name_lower for x in ["chatgpt", "ai", "midjourney", "plus"]):
                category = "ai"
            elif any(x in name_lower for x in ["vpn", "office", "key", "windows"]):
                category = "soft"

            products.append({
                "id": str(item['id']),
                "name": item['name'],
                "price": int(item['price_rur']),
                "cat": category,
                "img": item.get('preview_img_url') or "https://placehold.co/500x300",
                "link": f"https://www.digiseller.market/asp2/pay_wm.asp?id_d={item['id']}&ai={AGENT_ID}"
            })
        
        print(f"Успешно обработано товаров: {len(products)}")
        return products
    except Exception as e:
        print(f"Ошибка при запросе к API: {e}")
        return []

def main():
    items = get_products()
    if items:
        # Сохраняем в JSON, который будет читать ваш сайт
        with open('products.json', 'w', encoding='utf-8') as f:
            json.dump(items, f, ensure_ascii=False, indent=4)
        print("Файл products.json успешно обновлен.")

if __name__ == "__main__":
    main()
