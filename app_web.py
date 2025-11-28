import pandas as pd
import streamlit as st
from urllib.parse import quote_plus
from streamlit_autorefresh import st_autorefresh
import random

# ===============================
# 🎨 背景 + 跑馬燈 CSS
# ===============================
page_bg = """
<style>
body {
    background: linear-gradient(135deg, #fff5f7, #e6f7ff);
}

/* 大按鈕 (KenHub) */
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

@media (max-width: 600px) {
    .big-btn {
        font-size: 16px;
        padding: 12px 18px;
    }
}

/* 跑馬燈外框 */
.marquee-container {
    overflow: hidden;
    white-space: nowrap;
    background: #ffe9f0;
    border-radius: 999px;
    padding: 8px 16px;
    border: 1px solid #ffb6c9;
    margin-bottom: 12px;
}

/* 跑馬燈文字 */
.marquee-text {
    display: inline-block;
    padding-left: 100%;
    animation: marquee 18s linear infinite;
    font-size: 14px;
}

@media (max-width: 600px) {
    .marquee-text {
        font-size: 15px;
    }
}

@keyframes marquee {
    0%   { transform: translate(0, 0); }
    100% { transform: translate(-100%, 0); }
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# ===============================
# 💡 小知識 / 冷笑話
# ===============================
MUSCLE_TRIVIA = [
    "💡 小知識：人體超過 600 塊骨骼肌，你現在正在背其中一塊！📚",
    "😆 冷笑話：為什麼肱二頭肌很愛照鏡子？因為它怕自己變成肱一頭肌 💘",
    "💡 小知識：臀大肌是人體最大肌肉，負責站起來和走路 🍑",
    "😆 冷笑話：肌肉不會背叛你，但你會背叛它（不練就沒了）📉",
    "💡 小知識：咀嚼肌 masseter 是全身最有力的肌肉之一 🦷",
    "💡 小知識：心肌一天大概跳 10 萬次，比你還會複習 ❤️",
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
def find_muscle(df, keyword: str):
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
def kenhub_button(muscle):
    eng = quote_plus(muscle["english_name"])
    url = f"https://www.google.com/search?tbm=isch&q=site:kenhub.com+{eng}"
    st.markdown(
        f'<a href="{url}" target="_blank" class="big-btn">🔍 點我開啟網站看圖片</a>',
        unsafe_allow_html=True,
    )

# ===============================
# 測驗用設定
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

    # 產生錯誤選項
    pool = valid[field].unique().tolist()
    pool = [p for p in pool if p != correct]

    if len(pool) >= 3:
        distractors = random.sample(pool, 3)
    else:
        distractors = pool

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

    # ---- 跑馬燈（自動 + 手動）----
    auto_counter = st_autorefresh(interval=60_000, key="auto_marquee")

    if "manual_clicks" not in st.session_state:
        st.session_state["manual_clicks"] = 0

    idx = (auto_counter + st.session_state["manual_clicks"]) % len(MUSCLE_TRIVIA)

    st.markdown(
        f"""
        <div class="marquee-container">
            <div class="marquee-text">{MUSCLE_TRIVIA[idx]}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("換一句小知識 / 冷笑話 🔄"):
        st.session_state["manual_clicks"] += 1
        st.experimental_rerun()

    # ---- 肌肉查詢 ----
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

    # ---- 隨機抽考 ----
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

# ===============================
if __name__ == "__main__":
    main()
