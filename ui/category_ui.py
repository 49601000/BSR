import streamlit as st

def category_selector(category_list):
    """
    Streamlit UIでカテゴリを選択するセレクトボックスを表示。
    
    Parameters:
        category_list (list): 表示するカテゴリのリスト
    
    Returns:
        str: 選択されたカテゴリ
    """
    selected = st.selectbox("📂 カテゴリを選択してください", category_list)
    return selected
