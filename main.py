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
from services.ctg_dic import category_map
from services.square_api import (
    fetch_item_variation_map,
    fetch_sales,
    generate_ranking
)


# 🔐 認証情報を secrets から取得
access_token = st.secrets["api"]["access_token"]
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# ✅ 任意の日付範囲を指定（同日でもOK）
start_date, end_date = date_range_selector()

# ✅ 日付設定（JST → UTC変換）
if start_date and end_date:
    begin_time, end_time = convert_to_utc_range(start_date, end_date)
    st.write(f"🔁 UTC範囲: {begin_time} ～ {end_time}")
    
# データ取得
item_map, variation_map = fetch_item_variation_map(headers)
df = fetch_sales(headers, begin_time, end_time, item_map, variation_map)

# ✅ カテゴリ一覧を取得（None除外済み）
category_list = sorted({v for v in category_map.values() if v})
# ✅ Streamlit UIで選択肢として表示
selected_category = st.selectbox("カテゴリを選択", category_list)

# 📊 ランキング生成（選択されたカテゴリでデータをフィルタ）
filtered_df = df[df["カテゴリ"] == selected_category]
st.dataframe(filtered_df)
ranking = generate_ranking(filtered_df)

# フィルタリング（main.pyで処理）
if selected_category != "すべて":
    ranking = ranking[ranking["カテゴリ"] == selected_category]

# 表示
show_results(ranking, category_list)

# Excel保存（必要なら）
# csv_data = ranking.to_csv(index=False, encoding="utf-8-sig")
# with open("ranking.csv", "w", encoding="utf-8-sig") as f:
#     f.write(csv_data)


# ranking.to_excel(f"ranking_{target_date}.xlsx", index=False)




































