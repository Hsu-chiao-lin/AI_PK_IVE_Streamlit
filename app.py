import streamlit as st
import os
from PIL import Image
import random

# -------------------------
# 基本設定
# -------------------------
st.set_page_config(
    page_title="AI PK IVE",
    layout="centered"
)

st.title("AI PK IVE Member Recognition")
st.write("""
本專案是一個基於 **DeepFace** 的臉部辨識應用，使用 **Streamlit** 開發。
上傳照片後，系統會比對與 IVE 成員的相似度，並呈現辨識結果。
操作簡單直覺，支援快速切換圖片。
""")

# -------------------------
# 讀取圖片資料
# -------------------------
IMAGE_DIR = "photos"

def load_images(image_dir):
    if not os.path.exists(image_dir):
        return []
    return [
        os.path.join(image_dir, f)
        for f in os.listdir(image_dir)
        if f.lower().endswith((".jpg", ".png", ".jpeg"))
    ]

images = load_images(IMAGE_DIR)

# -------------------------
# UI 顯示邏輯
# -------------------------
if not images:
    st.error("找不到任何圖片，請確認 photos 資料夾內有圖片檔案。")
else:
    if "current_image" not in st.session_state:
        st.session_state.current_image = random.choice(images)

    def next_image():
        st.session_state.current_image = random.choice(images)

    # 安全載入圖片
    try:
        img = Image.open(st.session_state.current_image)
        st.image(
            img,
            caption=os.path.basename(st.session_state.current_image),
            use_column_width=True  # 舊版本 Streamlit 適用
        )
    except Exception as e:
        st.error(f"無法載入圖片: {st.session_state.current_image}\n錯誤訊息: {e}")

    st.button("下一張", on_click=next_image)
