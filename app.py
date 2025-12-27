import streamlit as st
import os
from PIL import Image
import random

st.set_page_config(page_title="AI PK IVE", layout="centered")
st.title("AI PK IVE")
st.write("隨機顯示 IVE 成員圖片，作為 AI 圖像展示示範 App")

IMAGE_DIR = "photos"

def load_images(image_dir):
    if not os.path.exists(image_dir):
        return []
    return [os.path.join(image_dir, f) for f in os.listdir(image_dir) if f.lower().endswith((".jpg", ".png", ".jpeg"))]

images = load_images(IMAGE_DIR)

if not images:
    st.error("找不到任何圖片，請確認 photos 資料夾內有圖片檔案。")
else:
    if "current_image" not in st.session_state:
        st.session_state.current_image = random.choice(images)

    def next_image():
        st.session_state.current_image = random.choice(images)

    try:
        img = Image.open(st.session_state.current_image)
        st.image(img, caption=os.path.basename(st.session_state.current_image), use_column_width=True)
    except Exception as e:
        st.error(f"無法載入圖片: {st.session_state.current_image}\n錯誤訊息: {e}")

    st.button("下一張", on_click=next_image)
