import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="跨境 AI 數據轉換器", layout="centered")

st.title("🤖 跨境電商數據轉換器 (AI 專用版)")
st.info("功能：將賣家精靈/亞馬遜 Excel 轉為 AI 最易讀的 CSV (UTF-8)")

# 1. 類別定義
category_map = {
    "關鍵字列表 (詞庫表現)": "Keyword_List",
    "關鍵字搜索結果表現 (賣家精靈分析)": "Keyword_res",
    "BSRTop 100結果表現 (類目分析)": "BSR_res",
    "產品Review (評論分析)": "P.Review"
}

selected_label = st.selectbox("第一步：請選擇檔案類型", options=list(category_map.keys()))
category_prefix = category_map[selected_label]

# 2. 檔案上傳
uploaded_file = st.file_uploader("第二步：上傳 Excel 檔案", type=["xlsx", "xls"])

if uploaded_file is not None:
    try:
        # 讀取第一個工作表
        df = pd.read_excel(uploaded_file, sheet_name=0)
        
        # 核心：自動移除全空行與列，確保 AI 讀到的是精華
        df = df.dropna(how='all', axis=0).dropna(how='all', axis=1)
        
        # 3. 處理檔名 (GMT+8)
        local_time = datetime.utcnow() + timedelta(hours=8)
        timestamp = local_time.strftime("%Y%m%d%H%M%S")
        new_filename = f"{category_prefix}_{timestamp}.csv"

        # 4. 預覽與轉換
        st.success(f"讀取成功！已過濾雜訊，剩餘 {df.shape[0]} 筆資料。")
        st.dataframe(df.head(3)) # 顯示前三列供確認

        # 轉換為純 UTF-8 (AI 專用，不帶 BOM)
        csv_data = df.to_csv(index=False, encoding='utf-8')

        st.download_button(
            label=f"📥 下載 {new_filename}",
            data=csv_data,
            file_name=new_filename,
            mime="text/csv",
        )
        
        st.caption("註：此檔案採用純 UTF-8 編碼。若用 Windows Excel 打開看到亂碼是正常的，但直接餵給 AI 讀會非常準確。")

    except Exception as e:
        st.error(f"檔案處理失敗，請檢查檔案格式是否正確。錯誤訊息: {e}")
