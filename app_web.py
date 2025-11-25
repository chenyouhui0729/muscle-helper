import pandas as pd
import streamlit as st

# 永遠讀 GitHub 上最新的 CSV
df = pd.read_csv(
    "https://raw.githubusercontent.com/chenyouhui0729/muscle-helper/main/muscles.csv"
)

def find_muscle(df, keyword):
    keyword = keyword.strip().lower()
    mask = (
        df["english_name"].str.lower().str.contains(keyword)
        | df["chinese_name"].str.contains(keyword)
    )
    results = df[mask]
    if len(results) > 0:
        return results.iloc[0]
    return None

def main():
    st.title("肌智救星 - 肌肉學習助手（網頁版 Prototype）")

    global df  # 使用上面 GitHub 載入的 df

    keyword = st.text_input("請輸入肌肉名稱（中/英文）：", "")

    if keyword:
        muscle = find_muscle(df, keyword)

        if muscle is not None:
            st.subheader(f"{muscle['chinese_name']} / {muscle['english_name']}")

            # ====== 顯示 image_url 內容，方便你確認 ======
            if "image_url" in muscle.index:
                st.write("image_url 欄位內容：", muscle["image_url"])
            else:
                st.write("⚠️ 這筆資料沒有找到 image_url 欄位（請檢查 CSV 欄位名稱）")

            # ====== 方法 2：一個欄位放多張圖，用分號 ; 分隔 ======
            urls_raw = str(muscle.get("image_url", "")).strip()

            # 避免出現 'nan' 或空字串
            if urls_raw and urls_raw.lower() != "nan":
                # 支援中英文分號；先把中文分號換成英文
                urls_raw = urls_raw.replace("；", ";")
                url_list = [
                    u.strip() for u in urls_raw.split(";") if u.strip() != ""
                ]

                # 逐一顯示圖片
                for url in url_list:
                    st.image(url, use_column_width=True)
            # ==============================================

            # 文字資訊
            st.write(f"**起點 Origin：** {muscle['origin']}")
            st.write(f"**終點 Insertion：** {muscle['insertion']}")
            st.write(f"**神經 Innervation：** {muscle['innervation']}")
            st.write(f"**血管 Blood supply：** {muscle['blood_supply']}")
            st.write(f"**動作 Actions：** {muscle['actions']}")

        else:
            st.error("找不到這塊肌肉，請確認關鍵字。")

    st.info("提示：可輸入：肱二頭肌、三角肌、biceps、deltoid…")

if __name__ == "__main__":
    main()
