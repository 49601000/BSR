import requests
import pandas as pd

# 📦 カテゴリ一覧取得
def fetch_categories(headers):
    url = "https://connect.squareup.com/v2/catalog/list"
    params = {"types": "CATEGORY"}
    categories = {}

    while True:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        for obj in data.get("objects", []):
            if obj["type"] == "CATEGORY":
                cat_id = obj["id"]
                cat_name = obj["category_data"]["name"]
                categories[cat_id] = cat_name

        cursor = data.get("cursor")
        if cursor:
            params["cursor"] = cursor
        else:
            break

    return categories

# 🧩 商品・バリエーション情報取得
def fetch_item_variation_map(headers, categories):
    url = "https://connect.squareup.com/v2/catalog/list"
    params = {"types": "ITEM,ITEM_VARIATION"}
    item_map = {}
    variation_map = {}

    while True:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        objects = data.get("objects", [])

        for obj in objects:
            if obj["type"] == "ITEM":
                item_id = obj["id"]
                item_name = obj["item_data"]["name"]
                category_id = obj["item_data"].get("category_id", "")
                category_name = categories.get(category_id, "未分類")
                item_map[item_id] = {
                    "name": item_name,
                    "category": category_name
                }

            elif obj["type"] == "ITEM_VARIATION":
                var_id = obj["id"]
                var_name = obj["item_variation_data"]["name"]
                item_id = obj["item_variation_data"]["item_id"]
                variation_map[var_id] = {
                    "variation_name": var_name,
                    "item_id": item_id
                }

        cursor = data.get("cursor")
        if cursor:
            params["cursor"] = cursor
        else:
            break

    return item_map, variation_map


# 💰 売上データ取得
def fetch_sales(headers, begin_time, end_time, item_map, variation_map):
    payments_endpoint = "https://connect.squareup.com/v2/payments"
    params = {
        "begin_time": begin_time,
        "end_time": end_time,
        "limit": 100
    }

    results = []

    while True:
        response = requests.get(payments_endpoint, headers=headers, params=params)
        if response.status_code != 200:
            print(f"エラー: {response.status_code}")
            break

        data = response.json()
        payments = data.get("payments", [])

        for p in payments:
            created_at = p["created_at"][:10]
            order_id = p.get("order_id")
            if not order_id:
                continue

            order_url = f"https://connect.squareup.com/v2/orders/{order_id}"
            order_response = requests.get(order_url, headers=headers)
            if order_response.status_code != 200:
                continue
            order_data = order_response.json().get("order", {})
            line_items = order_data.get("line_items", [])

            for item in line_items:
                variation_id = item.get("catalog_object_id")
                quantity = int(item.get("quantity", "1"))

                variation_info = variation_map.get(variation_id, {})
                item_id = variation_info.get("item_id")
                item_info = item_map.get(item_id, {})

                results.append({
                    "日付": created_at,
                    "カテゴリ": item_info.get("category", "未分類"),
                    "商品名": item_info.get("name", "不明"),
                    "バリエーション": variation_info.get("variation_name", "不明"),
                    "販売個数": quantity
                })

        cursor = data.get("cursor")
        if cursor:
            params["cursor"] = cursor
        else:
            break

    return pd.DataFrame(results)

# 💰 ランキング生成
def generate_ranking(df):
    grouped = df.groupby(["カテゴリ", "商品名", "バリエーション"])["販売個数"].sum().reset_index()
    ranking = grouped.sort_values(by="販売個数", ascending=False)
    return ranking
