import streamlit as st
import pandas as pd

def category_selector(category_list: list) -> str:
    return st.radio("📂 表示するカテゴリを選んでください", ["すべて"] + category_list)
def show_results(ranking: pd.DataFrame):
    st.subheader("🏆 カテゴリ × 商品 × バリエーション別売上ランキング")

    if ranking.empty:
        st.info("該当期間の売上データはありませんでした。")
    else:
        st.dataframe(ranking, use_container_width=True)

        csv = ranking.to_csv(index=False, encoding="utf-8-sig")
        st.download_button(
            label="📥 CSVでダウンロード",
            data=csv,
            file_name="ranking.csv",
            mime="text/csv"
        )
