import streamlit as st
import pandas as pd
from datetime import date

def show_results(ranking: pd.DataFrame):
    st.subheader("🏆 カテゴリ × 商品 × バリエーション別売上ランキング")

    if ranking.empty:
        st.info("該当期間の売上データはありませんでした。")
    else:
        st.dataframe(ranking, use_container_width=True, height=500)

        st.markdown("### 💾 売上ランキングをCSV形式で保存できます")

        csv = ranking.to_csv(index=False, encoding="utf-8-sig")
        filename = f"ranking_{date.today().isoformat()}.csv"
        st.download_button(
            label="📥 CSVファイルをダウンロードする",
            data=csv,
            file_name=filename,
            mime="text/csv"
        )
