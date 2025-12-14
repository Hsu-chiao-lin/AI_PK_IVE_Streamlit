# AI_PK IVE Member Recognition Streamlit App

這是一個基於 **DeepFace** 的臉部辨識專案，使用 **Streamlit** 開發，能夠與 IVE 成員照片比對，看看誰比較像誰。專案目標是將深度學習臉部辨識模型整合成互動 Web App。

---

## 功能

- 上傳照片，辨識與 IVE 成員最相似的對象  
- 顯示辨識結果與相似度  
- 遇到找不到相似成員時提示使用者檢查照片清晰度  
- 整合 Streamlit 介面，操作簡單直覺  

---

## 安裝與環境

建議使用 **Python 3.10 ~ 3.13**，並建立虛擬環境：

```bash
# 建立虛擬環境
python -m venv venv
# 啟動虛擬環境 (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# 安裝必要套件
pip install -r requirements.txt
