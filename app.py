import streamlit as st
import os
from PIL import Image
import random

# -------------------------
# Streamlit 基本設定
# -------------------------
st.set_page_config(page_title="AI PK IVE Fun", layout="centered")
st.title("AI PK IVE Fun")
st.write("""
上傳你的照片，看看今天你最像哪位 IVE 成員！  
隨機趣味互動，完全不使用 AI 或 DeepFace。
""")

# -------------------------
# IVE 成員照片資料夾
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

if not images:
    st.error("找不到任何 IVE 成員照片，請確認 photos 資料夾內有圖片檔案。")

# -------------------------
# 隨機瀏覽 IVE 成員照片
# -------------------------
if images:
    if "current_image" not in st.session_state:
        st.session_state.current_image = random.choice(images)

    def next_image():
        st.session_state.current_image = random.choice(images)

    try:
        img = Image.open(st.session_state.current_image)
        st.image(img, caption=os.path.basename(st.session_state.current_image), use_column_width=True)
    except Exception as e:
        st.error(f"無法載入圖片: {st.session_state.current_image}\n錯誤訊息: {e}")

    st.button("下一張成員", on_click=next_image)

# -------------------------
# 上傳照片 + 趣味隨機比對
# -------------------------
uploaded_file = st.file_uploader("上傳你的照片，看看今天你最像哪位 IVE 成員", type=["jpg", "jpeg", "png"])

if uploaded_file and images:
    try:
        user_img = Image.open(uploaded_file)
        st.image(user_img, caption="你的上傳照片", use_column_width=True)

        # 隨機挑選一位成員
        matched_member = random.choice(images)
        matched_img = Image.open(matched_member)
        st.image(matched_img, caption=f"今天你最像：{os.path.basename(matched_member)} 🎉", use_column_width=True)

        # 顯示趣味文字
        fun_messages = [
            "完美搭配！",
            "你們氣質超像！",
            "眼神都很迷人～",
            "今天就是這位成員的翻版！",
            "你的笑容有對應的魅力！"
        ]
        st.success(random.choice(fun_messages))

    except Exception as e:
        st.error(f"處理上傳照片時發生錯誤：{e}")
