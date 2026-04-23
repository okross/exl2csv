import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="AI 數據餵食轉換器", layout="centered")

st.title("🤖 AI 數據餵食轉換器")

category_map = {
    "關鍵字列表 (詞庫表現)": "Keyword_List",
    "關鍵字搜索結果表現 (賣家精靈分析)": "Keyword_res",
    "BSRTop 100結果表現 (類目分析)": "BSR_res",
    "產品Review (評論分析)": "P.Review"
}

selected_label = st.selectbox("請選擇檔案類型：", options=list(category_map.keys()))
category_prefix = category_map[selected_label]

uploaded_file = st.file_uploader("上傳 Excel 檔案", type=["xlsx", "xls"])

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file, sheet_name=0)
        df = df.dropna(how='all', axis=0).dropna(how='all', axis=1)
        
        # 固定使用 GMT+8 
        local_time = datetime.utcnow() + timedelta(hours=8)
        timestamp = local_time.strftime("%Y%m%d%H%M%S")
        new_filename = f"{category_prefix}_{timestamp}.csv"

        csv_data = df.to_csv(index=False, encoding='utf-8')

        st.download_button(
            label=f"📥 下載 {new_filename}",
            data=csv_data,
            file_name=new_filename,
            mime="text/csv",
        )
        st.success(f"轉換完成！檔名已校正為 GMT+8 時間。")
    except Exception as e:
        st.error(f"發生錯誤: {e}")
