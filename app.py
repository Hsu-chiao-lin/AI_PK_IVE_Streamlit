import streamlit as st
from deepface import DeepFace
from pathlib import Path
import pandas as pd

st.title("AI PK - 認識 IVE 成員")

# 上傳圖片
uploaded_file = st.file_uploader("上傳你的照片", type=["jpg", "jpeg", "png"])

# 資料夾路徑
IVE_DIR = Path("photos")  # 請放所有 IVE 成員照片的資料夾
IVE_DIR.mkdir(exist_ok=True)

# 模型選擇
model_name = st.selectbox("選擇模型", ["VGG-Face", "Facenet", "ArcFace", "DeepFace"])

if uploaded_file:
    # 儲存上傳的臨時檔
    input_path = Path("temp_input.jpg")
    with open(input_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.image(input_path, caption="上傳的照片", use_column_width=True)

    if not any(IVE_DIR.iterdir()):
        st.warning("IVE 成員資料夾內沒有照片，請放入照片")
    else:
        try:
            # 使用 DeepFace 找相似
            results = DeepFace.find(
                img_path=str(input_path), 
                db_path=str(IVE_DIR), 
                model_name=model_name, 
                enforce_detection=False
            )

            # 判斷回傳型態
            if isinstance(results, list):
                if len(results) == 0:
                    st.warning("找不到相似成員，請確認照片清晰度。")
                    results_df = pd.DataFrame()
                else:
                    # DeepFace 新版回傳 list 可能只有一個 DataFrame
                    results_df = results[0]
            else:
                results_df = results

            if results_df.empty:
                st.warning("找不到相似成員，請確認照片清晰度。")
            else:
                # 找到數值型欄位 (相似度距離)
                distance_cols = [col for col in results_df.columns if results_df[col].dtype in ['float64','float32','int64','int32']]
                if not distance_cols:
                    st.error("找不到相似度欄位，請確認 DeepFace 模型與版本")
                else:
                    distance_col = distance_cols[0]

                    # 顯示前 3 名最相似成員
                    df_sorted = results_df.sort_values(by=distance_col, ascending=True).head(3)
                    st.subheader("最相似的成員")
                    for i, row in df_sorted.iterrows():
                        identity = Path(row["identity"]).name
                        distance = float(row[distance_col])
                        st.write(f"{i+1}. {identity} - 相似度: {distance:.4f}")
                        st.image(row["identity"], width=200)

        except Exception as e:
            st.error(f"辨識發生錯誤: {e}")
