import pandas as pd
import streamlit as st
from urllib.parse import quote_plus
import random

# ===============================
# 🎨 背景 CSS
# ===============================
page_bg = """
<style>
body {
    background: linear-gradient(135deg, #fff5f7, #e6f7ff);
}

/* KenHub 大按鈕 */
.big-btn {
    display: inline-block;
    padding: 14px 22px;
    background-color: #ff85a2;
    color: white !important;
    font-size: 18px;
    font-weight: bold;
    border-radius: 12px;
    text-align: center;
    text-decoration: none;
    transition: 0.2s;
}
.big-btn:hover {
    background-color: #ff668a;
}

/* 手機版按鈕縮小 */
@media (max-width: 600px) {
    .big-btn {
        font-size: 16px;
        padding: 12px 18px;
    }
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# ===============================
# 💡 肌肉小知識 / 冷笑話
# ===============================
MUSCLE_TRIVIA = [
    "💡 小知識：人體超過 600 塊骨骼肌，你現在正在背其中一塊！📚",
    "😆 冷笑話：思思的帳號被冒用，她的男友知道了以後很憤怒的說：             可...可惡...敢冒用思思⋯",
    "💡 小知識：臀大肌是人體最大肌肉，負責站起來和走路 🍑",
    "😆 冷笑話：木魚掉進水裡會變什麼？          濕木魚",
    "💡 小知識：咀嚼肌 masseter 是全身最有力的肌肉之一 🦷",
    "💡 小知識：心肌一天大概跳 10 萬次，比你還會複習 ❤️",
    "😆 冷笑話：大阪唸:Osaka  沖繩唸:Okinawa  京都唸:慈安川貝枇杷膏",
    "😆 冷知識：肉羹麵把湯倒掉之後，還是肉跟麵",
    "😆 冷笑話：S和M面對面喝茶 steam",
    "😆 冷笑話：警察生氣了會變成甚麼？   警報器",
    "😆 冷笑話：甚麼東西有四隻腳，而且綠綠毛毛的？   撞球桌",
    "😆 冷笑話：A和C誰比較高？答案：C，因為A比C低 (ABCD)",
    "😆 冷笑話：皮卡丘跑步會變成甚麼？皮卡乒乓乒乓",
    "😆 冷笑話：給大家科普一下辣的程度：
1級：微辣🌶
2級：中辣🌶🌶
3級：重辣🌶🌶🌶
4級：變態辣🌶🌶🌶🌶
10級：你又要一個人過聖誕辣",

]

# ===============================
# 讀取 CSV
# ===============================
df = pd.read_csv(
    "https://raw.githubusercontent.com/chenyouhui0729/muscle-helper/main/muscles.csv"
).fillna("（未填寫）")

# ===============================
# 搜尋肌肉
# ===============================
def find_muscle(df: pd.DataFrame, keyword: str):
    keyword = keyword.strip()
    if not keyword:
        return None
    k_lower = keyword.lower()
    mask = (
        df["english_name"].str.lower().str.contains(k_lower)
        | df["chinese_name"].str.contains(keyword)
    )
    if mask.any():
        return df[mask].iloc[0]
    return None

# ===============================
# KenHub 按鈕
# ===============================
def kenhub_button(muscle_row):
    eng = quote_plus(muscle_row["english_name"])
    url = f"https://www.google.com/search?tbm=isch&q=site:kenhub.com+{eng}"
    st.markdown(
        f'<a href="{url}" target="_blank" class="big-btn">🔍 點我開啟網站看圖片</a>',
        unsafe_allow_html=True,
    )

# ===============================
# 測驗設定
# ===============================
QUIZ_FIELD_MAP = {
    "origin": "起點 Origin",
    "insertion": "終點 Insertion",
    "innervation": "神經 Innervation",
    "actions": "動作 Actions",
}

def generate_quiz(df: pd.DataFrame, field: str):
    """從指定欄位產生一題隨機測驗"""
    valid = df[df[field] != "（未填寫）"]
    if valid.empty:
        return None

    muscle = valid.sample(1).iloc[0]
    correct = muscle[field]

    candidates = valid[field].unique().tolist()
    candidates = [c for c in candidates if c != correct]

    if len(candidates) >= 3:
        distractors = random.sample(candidates, 3)
    else:
        distractors = candidates

    options = [correct] + distractors
    random.shuffle(options)

    return {
        "muscle_ch": muscle["chinese_name"],
        "muscle_en": muscle["english_name"],
        "field": field,
        "correct": correct,
        "options": options,
    }

# ===============================
# 主程式
# ===============================
def main():
    st.title("🐥 肌智救星 - 肌肉學習助手（網頁版 Prototype）")

    # -----------------------
    # 🔍 肌肉搜尋區
    # -----------------------
    st.subheader("🔍 肌肉搜尋")
    keyword = st.text_input("輸入肌肉名稱（中/英文）：", "")

    if keyword:
        muscle = find_muscle(df, keyword)
        if muscle is not None:
            st.markdown(f"### 💪 {muscle['chinese_name']} / {muscle['english_name']}")
            kenhub_button(muscle)

            st.write("---")
            st.write(f"📍 **起點 Origin：** {muscle['origin']}")
            st.write(f"🎯 **終點 Insertion：** {muscle['insertion']}")
            st.write(f"⚡ **神經 Innervation：** {muscle['innervation']}")
            st.write(f"🩸 **血管 Blood supply：** {muscle['blood_supply']}")
            st.write(f"🏃 **動作 Actions：** {muscle['actions']}")
        else:
            st.error("找不到這塊肌肉 😢 請換另一個關鍵字試試看")

    st.info("✨ 提示：可輸入：肱二頭肌、三角肌、biceps、deltoid…")

    st.write("---")

    # -----------------------
    # 🎲 肌肉小測驗
    # -----------------------
    st.subheader("🎲 肌肉小測驗")

    field = st.selectbox(
        "想要被考哪一個項目？",
        list(QUIZ_FIELD_MAP.keys()),
        format_func=lambda k: QUIZ_FIELD_MAP[k],
    )

    if "quiz" not in st.session_state:
        st.session_state["quiz"] = None
    if "quiz_answer" not in st.session_state:
        st.session_state["quiz_answer"] = None

    col1, col2 = st.columns(2)

    with col1:
        if st.button("出一題 🎲"):
            st.session_state["quiz"] = generate_quiz(df, field)
            st.session_state["quiz_answer"] = None

    with col2:
        if st.button("清除本題 ↩️"):
            st.session_state["quiz"] = None
            st.session_state["quiz_answer"] = None

    quiz = st.session_state["quiz"]

    if quiz is not None:
        st.markdown(
            f"**題目：{quiz['muscle_ch']} / {quiz['muscle_en']} 的 {QUIZ_FIELD_MAP[field]} 是？**"
        )

        choice = st.radio("請選出正確答案：", quiz["options"])

        if st.button("提交答案 ✅"):
            st.session_state["quiz_answer"] = choice
            if choice == quiz["correct"]:
                st.success("答對了！🎉 你的肌肉記憶正在升級 💪")
            else:
                st.error("答錯了 😢 再複習一下！")
                st.info(f"✅ 正確答案是：{quiz['correct']}")

    else:
        st.caption("按「出一題 🎲」開始測驗吧！")

    st.write("---")

    # -----------------------
    # 📜 底部小知識（米白底 + 黑字）
    # 每次重新整理隨機顯示一則
    # -----------------------
    trivia_text = random.choice(MUSCLE_TRIVIA)
    st.markdown(
        "<div style='margin-top:16px; padding:10px 18px; "
        "background:#f9f5e9; color:#000; border-radius:999px; "
        "border:1px solid #d6c9a8; font-size:15px; text-align:center;'>"
        + trivia_text +
        "</div>",
        unsafe_allow_html=True,
    )

# ===============================
if __name__ == "__main__":
    main()

