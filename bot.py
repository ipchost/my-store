import requests
import json
import os

# Твои настройки из файла коды.txt
SELLER_ID = "1439429"
AGENT_ID = "1439429"

def get_products():
    print("Запрос товаров из Digiseller...")
    # Используем API для получения списка товаров продавца
    url = f"https://api.digiseller.ru/api/seller-goods.ashx?seller_id={SELLER_ID}&rows=100&lang=ru-RU"
    
    try:
        headers = {'Accept': 'application/json', 'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status()
        
        data = r.json()
        rows = data.get('rows', [])
        
        products = []
        for item in rows:
            p_id = str(item['id'])
            # Определяем категорию (логика авто-назначения)
            name_lower = item['name'].lower()
            category = "games"
            if "wallet" in name_lower or "пополнение" in name_lower or "card" in name_lower:
                category = "wallets"
            elif "chatgpt" in name_lower or "midjourney" in name_lower or "ai" in name_lower:
                category = "ai"
            elif "vpn" in name_lower or "office" in name_lower or "key" in name_lower:
                category = "soft"

            products.append({
                "id": p_id,
                "name": item['name'],
                "price": int(item['price_rur']),
                "cat": category,
                "img": item['preview_img_url'] if item['preview_img_url'] else "https://placehold.co/500x300",
                "link": f"https://www.digiseller.market/asp2/pay_wm.asp?id_d={p_id}&ai={AGENT_ID}"
            })
        
        print(f"Успешно получено: {len(products)} товаров")
        return products
    except Exception as e:
        print(f"Ошибка: {e}")
        return []

def main():
    items = get_products()
    if items:
        # Сохраняем результат в products.json для сайта
        with open('products.json', 'w', encoding='utf-8') as f:
            json.dump(items, f, ensure_ascii=False, indent=4)
        print("Данные синхронизированы с products.json")
    else:
        print("Обновление не удалось.")

if __name__ == "__main__":
    main()
