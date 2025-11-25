import pandas as pd
import streamlit as st

# 永遠讀 GitHub CSV
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

    global df

    keyword = st.text_input("請輸入肌肉名稱（中/英文）：", "")

    if keyword:
        muscle = find_muscle(df, keyword)

        if muscle is not None:
            st.subheader(f"{muscle['chinese_name']} / {muscle['english_name']}")

            # ===========================
            # 顯示多張圖片（防呆版）
            # ===========================
            if "image_url" in muscle.index:
                urls_raw = str(muscle["image_url"]).strip()

                if urls_raw and urls_raw.lower() != "nan":
                    urls_raw = urls_raw.replace("；", ";")
                    url_list = [
                        u.strip() for u in urls_raw.split(";") if u.strip() != ""
                    ]
                    for url in url_list:
                        try:
                            st.image(url, use_column_width=True)
                        except Exception as e:
                            st.warning(f"⚠️ 無法載入圖片：{url}")
                            st.caption(f"錯誤訊息：{e}")
                else:
                    st.info("這個肌肉目前沒有圖片。")
            else:
                st.info("CSV 中沒有找到 image_url 欄位。")

            # ===========================
            # 文字內容完整顯示
            # ===========================
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
