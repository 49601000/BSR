import streamlit as st
from datetime import datetime, timedelta

def date_range_selector():
    st.subheader("📅 期間を選択してください")

    # 今日の日付（JST基準）
    today = datetime.now().date()

    # プリセット：8日前〜昨日
    default_start = today - timedelta(days=8)
    default_end = today - timedelta(days=1)

    # UI表示（ユーザーが変更可能）
    start_date = st.date_input("開始日", value=default_start)
    end_date = st.date_input("終了日", value=default_end)

    # バリデーション
    if start_date > end_date:
        st.warning("開始日は終了日より前にしてください")
        return None, None

    return start_date, end_date
