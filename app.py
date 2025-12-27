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

st.title("AI PK IVE")
st.write("隨機顯示 IVE 成員圖片，作為 AI 圖像展示示範 App")

# -------------------------
# 讀取圖片資料
# -------------------------
IMAGE_DIR = "photos"

def load_images(image_dir):
    if not os.path.exists(image_dir):
        return []

    images = []
    for file in os.listdir(image_dir):
        if file.lower().endswith((".jpg", ".png", ".jpeg")):
            images.append(os.path.join(image_dir, file))
    return images

images = load_images(IMAGE_DIR)

# -------------------------
# UI 顯示邏輯
# -------------------------
if not images:
    st.error("找不到任何圖片，請確認 photos 資料夾內有圖片檔案。")
else:
    if "current_image" not in st.session_state:
        st.session_state.current_image = random.choice(images)

    img = Image.open(st.session_state.current_image)
    st.image(img, caption=os.path.basename(st.session_state.current_image), use_container_width=True)

    if st.button("下一張"):
        st.session_state.current_image = random.choice(images)
        st.rerun()
