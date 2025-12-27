import streamlit as st
import os
from PIL import Image
import random
from deepface import DeepFace

# -------------------------
# 基本設定
# -------------------------
st.set_page_config(page_title="AI PK IVE", layout="centered")
st.title("AI PK IVE Member Recognition")
st.write("""
上傳你的照片，系統會比對 IVE 成員照片，顯示最相似的成員及相似度。
操作簡單直覺，支援快速切換展示照片。
""")

# -------------------------
# 讀取 IVE 成員照片
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
# 顯示隨機 IVE 成員照片
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

    st.button("下一張", on_click=next_image)

# -------------------------
# 使用者上傳照片與比對
# -------------------------
uploaded_file = st.file_uploader("上傳你的照片以比對 IVE 成員", type=["jpg", "jpeg", "png"])

if uploaded_file:
    try:
        user_img = Image.open(uploaded_file)
        st.image(user_img, caption="你的上傳照片", use_column_width=True)

        # 進行 DeepFace 比對
        results = []
        for member_img_path in images:
            try:
                result = DeepFace.verify(
                    img1_path=uploaded_file,
                    img2_path=member_img_path,
                    enforce_detection=False
                )
                similarity = 1 - result["distance"]  # 相似度 0~1
                results.append((member_img_path, similarity))
            except Exception as e:
                continue  # 跳過比對失敗的圖片

        if results:
            # 依相似度排序，找最相似成員
            best_match = max(results, key=lambda x: x[1])
            st.success(f"最相似的 IVE 成員：{os.path.basename(best_match[0])}")
            st.info(f"相似度：{best_match[1]*100:.2f}%")

            # 顯示最相似成員照片
            best_img = Image.open(best_match[0])
            st.image(best_img, caption=f"比對結果：{os.path.basename(best_match[0])}", use_column_width=True)
        else:
            st.warning("無法比對，請確認照片清晰度。")

    except Exception as e:
        st.error(f"處理上傳照片時發生錯誤：{e}")
