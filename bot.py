import requests
import json
import os

# [cite_start]Данные из вашего файла коды.txt [cite: 1, 3]
SELLER_ID = "1439429"
AGENT_ID = "1439429"
API_KEY = "7757E1B2A8B74B11ADD1403764506273"

def get_products():
    print("Запрос товаров из Digiseller (актуальный API)...")
    
    # Используем правильный endpoint API вместо устаревшего .ashx
    url = "https://api.digiseller.ru/api/goods/list"
    
    params = {
        "seller_id": SELLER_ID,
        "currency": "RUR",
        "lang": "ru-RU",
        "rows": 100,
        "order": "popular"
    }
    
    headers = {
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0',
        [cite_start]'token': API_KEY # Используем ваш API ключ [cite: 1]
    }

    try:
        r = requests.get(url, params=params, headers=headers, timeout=30)
        r.raise_for_status()
        
        data = r.json()
        rows = data.get('rows', []) or data.get('items', [])
        
        products = []
        for item in rows:
            p_id = str(item['id'])
            name_lower = item['name'].lower()
            
            # Логика категорий для вашего сайта
            category = "games"
            if any(word in name_lower for word in ["wallet", "пополнение", "card", "gift"]):
                category = "wallets"
            elif any(word in name_lower for word in ["chatgpt", "midjourney", "ai", "plus"]):
                category = "ai"
            elif any(word in name_lower for word in ["vpn", "office", "key", "windows"]):
                category = "soft"

            products.append({
                "id": p_id,
                "name": item['name'],
                "price": int(item['price_rur']),
                "cat": category,
                "img": item.get('preview_img_url') or "https://placehold.co/500x300",
                "link": f"https://www.digiseller.market/asp2/pay_wm.asp?id_d={p_id}&ai={AGENT_ID}"
            })
        
        print(f"Успешно получено: {len(products)} товаров")
        return products
    except Exception as e:
        print(f"Ошибка API: {e}")
        return []

def main():
    items = get_products()
    if items:
        with open('products.json', 'w', encoding='utf-8') as f:
            json.dump(items, f, ensure_ascii=False, indent=4)
        print("Файл products.json обновлен.")
    else:
        print("Данные не получены.")

if __name__ == "__main__":
    main()
