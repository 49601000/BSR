import streamlit as st
import pandas as pd

def show_results(df: pd.DataFrame):
    st.subheader("📊 データ出力")
    if df.empty:
        st.info("該当期間のデータはありませんでした。")
    else:
        st.dataframe(df)
        st.download_button("CSVでダウンロード", df.to_csv(index=False), file_name="result.csv", mime="text/csv")
