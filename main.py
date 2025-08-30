import requests
import pandas as pd
import streamlit as st
from ui.date_selector import date_range_selector
from utils.timezone import convert_to_utc_range
from ui.result_display import show_results

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

# ランキング生成
ranking = generate_ranking(df)

# 表示（Streamlitなど）
show_results(ranking)

# Excel保存（必要なら）
# csv_data = ranking.to_csv(index=False, encoding="utf-8-sig")
# with open("ranking.csv", "w", encoding="utf-8-sig") as f:
#     f.write(csv_data)


# ranking.to_excel(f"ranking_{target_date}.xlsx", index=False)


