import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="AI 數據餵食轉換器", layout="centered")

st.title("🤖 AI 數據餵食轉換器 (Excel to CSV)")
st.write("將賣家精靈或其他工具導出的 Excel 轉為 AI 最易讀的 CSV 格式。")

uploaded_file = st.file_uploader("上傳 Excel 檔案", type=["xlsx", "xls"])

if uploaded_file is not None:
    try:
        # 1. 讀取第一個 Sheet
        df = pd.read_excel(uploaded_file, sheet_name=0)
        
        # 2. 清理資料：移除全空的行與列，避免 AI 讀到多餘的逗號
        df = df.dropna(how='all', axis=0).dropna(how='all', axis=1)
        
        st.success(f"讀取成功！已自動清理空行，剩餘 {df.shape[0]} 列 x {df.shape[1]} 欄。")
        st.dataframe(df.head(3))

        # 3. 轉換為純 UTF-8 (不含 BOM，AI 讀取最順暢)
        # 為了確保 AI 好讀，我們保留標題 (index=False)
        csv_data = df.to_csv(index=False, encoding='utf-8')

        st.download_button(
            label="📥 下載 AI 專用 CSV",
            data=csv_data,
            file_name=f"{uploaded_file.name.rsplit('.', 1)[0]}_for_AI.csv",
            mime="text/csv",
        )
    except Exception as e:
        st.error(f"發生錯誤: {e}")
