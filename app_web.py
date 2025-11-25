import pandas as pd
import streamlit as st

# 📌 永遠讀 GitHub 上最新的 CSV
df = pd.read_csv("https://raw.githubusercontent.com/chenyouhui0729/muscle-helper/main/muscles.csv")

# 📌 查詢肌肉
def find_muscle(df, keyword):
    keyword = keyword.strip().lower()
    mask = (
        df["english_name"].str.lower().str.contains(keyword) |
        df["chinese_name"].str.contains(keyword)
    )
    results = df[mask]
    if len(results) > 0:
        return results.iloc[0]
    return None

# 📌 Streamlit 主程式
def main():
    st.title("肌智救星 - 肌肉學習助手（網頁版 Prototype）")

    global df  # 使用 GitHub 版本的 df

    keyword = st.text_input("請輸入肌肉名稱（中/英文）：", "")

    if keyword:
        muscle = find_muscle(df, keyword)
        if muscle is not None:

            st.subheader(f"{muscle['chinese_name']} / {muscle['english_name']}")

            # -------------------------
            # 📌 方法 2：支援多張圖片用分號「;」分隔
            # -------------------------
            if "image_url" in muscle.index and pd.notna(muscle["image_url"]):
                url_list = [
                    url.strip()
                    for url in muscle["image_url"].split(";")
                    if url.strip() != ""
                ]
                for url in url_list:
                    st.image(url, use_column_width=True)
            # -------------------------

            # 文字資料輸出
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
