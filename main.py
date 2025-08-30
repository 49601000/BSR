import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import requests
import pandas as pd
import streamlit as st
from utils.timezone import convert_to_utc_range
from ui.date_selector import date_range_selector
from ui.result_display import show_results
from ui.result_display import show_results
from ui.category_ui import category_selector
from services.square_api import fetch_categories


# 🔐 認証情報を secrets から取得
ACCESS_TOKEN = st.secrets["ACCESS_TOKEN"]
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

# ✅ 任意の日付範囲を指定（同日でもOK）
start_date, end_date = date_range_selector()

# ✅ 日付設定（JST → UTC変換）
if start_date and end_date:
    begin_time, end_time = convert_to_utc_range(start_date, end_date)
    st.write(f"🔁 UTC範囲: {begin_time} ～ {end_time}")
    

# データ取得
categories = fetch_categories(headers)
item_map, variation_map = fetch_item_variation_map(headers, categories)
df = fetch_sales(headers, begin_time, end_time, item_map, variation_map)

# カテゴリ一覧を取得
categories = fetch_categories(headers)
category_list = sorted(set(categories.values()))

# UIでカテゴリ選択
selected_category = category_selector(category_list)

# 売上データ取得＆ランキング生成
df = fetch_sales(headers, begin_time, end_time, item_map, variation_map)
ranking = generate_ranking(df)

# フィルタリング（main.pyで処理）
if selected_category != "すべて":
    ranking = ranking[ranking["カテゴリ"] == selected_category]

# 表示
show_results(ranking)

# Excel保存（必要なら）
# csv_data = ranking.to_csv(index=False, encoding="utf-8-sig")
# with open("ranking.csv", "w", encoding="utf-8-sig") as f:
#     f.write(csv_data)


# ranking.to_excel(f"ranking_{target_date}.xlsx", index=False)









