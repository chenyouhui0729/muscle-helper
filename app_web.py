import pandas as pd
import streamlit as st

# 只用 GitHub 最新 CSV
df = pd.read_csv("https://raw.githubusercontent.com/chenyouhui0729/muscle-helper/main/muscles.csv")

def find_muscle(df, keyword):
    keyword = keyword.strip().lower()
    mask = df["english_name"].str.lower().str.contains(keyword) | df["chinese_name"].str.contains(keyword)
    results = df[mask]
    if len(results) > 0:
        return results.iloc[0]   # 取第一筆
    return None

def main():
    st.title("肌智救星-肌肉學習助手（網頁版 Prototype）")

    # 使用最上面讀取到的 df（GitHub 版本）
global df


    keyword = st.text_input("請輸入肌肉名稱（中/英文）：" , "")

    if keyword:
        muscle = find_muscle(df, keyword)
        if muscle is not None:
            st.subheader(f"{muscle['chinese_name']} / {muscle['english_name']}")
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


