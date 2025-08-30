import streamlit as st
from datetime import datetime

def date_range_selector():
    st.subheader("📅 期間を選択してください")
    start_date = st.date_input("開始日", value=datetime.today())
    end_date = st.date_input("終了日", value=datetime.today())

    if start_date > end_date:
        st.warning("開始日は終了日より前にしてください")
        return None, None

    return start_date, end_date
