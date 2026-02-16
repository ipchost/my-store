import requests
import json
import os

# Данные из вашего файла коды.txt 
SELLER_ID = "1439429"
AGENT_ID = "1439429"
API_KEY = "7757E1B2A8B74B11ADD1403764506273"

def get_products():
    print("Запрос товаров из Digiseller (актуальный API)...")
    
    # Используем правильный endpoint API
    url = "https://api.digiseller.ru/api/goods/list"
    
    # Параметры запроса для получения популярных товаров 
    params = {
        "seller_id": SELLER_ID,
        "currency": "RUR",
        "lang": "ru-RU",
        "rows": 100,
        "order": "popular" # Сортировка по популярности для глобальных продаж
    }
    
    headers = {
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0'
    }

    try:
        r = requests.get(url, params=params, headers=headers, timeout=30)
        r.raise_for_status()
        
        data = r.json()
        # В новом API список товаров находится в ключе 'rows' или 'items'
        rows = data.get('rows', []) or data.get('items', [])
        
        products = []
        for item in rows:
            p_id = str(item['id'])
            name_lower = item['name'].lower()
            
            # Улучшенная логика категорий для вашего сайта
            category = "games"
            if any(word in name_lower for word in ["wallet", "пополнение", "card", "gift"]):
                category = "wallets"
            elif any(word in name_lower for word in ["chatgpt", "midjourney", "ai", "plus"]):
                category = "ai"
            elif any(word in name_lower for word in ["vpn", "office", "key", "windows", "софт"]):
                category = "soft"

            products.append({
                "id": p_id,
                "name": item['name'],
                "price": int(item['price_rur']),
                "cat": category,
                "img": item.get('preview_img_url') or "https://placehold.co/500x300",
                "link": f"https://www.digiseller.market/asp2/pay_wm.asp?id_d={p_id}&ai={AGENT_ID}"
            })
        
        print(f"Успешно получено и обработано: {len(products)} товаров")
        return products
    except Exception as e:
        print(f"Ошибка при запросе к API: {e}")
        return []

def main():
    items = get_products()
    if items:
        # Сохранение в файл products.json, который читает ваш index.html 
        with open('products.json', 'w', encoding='utf-8') as f:
            json.dump(items, f, ensure_ascii=False, indent=4)
        print("Файл products.json успешно обновлен для сайта.")
    else:
        print("Не удалось обновить данные. Проверьте настройки API.")

if __name__ == "__main__":
    main()
