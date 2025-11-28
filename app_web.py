import pandas as pd
import streamlit as st
from urllib.parse import quote_plus
from streamlit_autorefresh import st_autorefresh  # 🔁 自動重新整理用
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

/* 手機版按鈕縮小 */
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

/* 跑馬燈文字動畫 */
.marquee-text {
    display: inline-block;
    padding-left: 100%;
    animation: marquee 18s linear infinite;
    font-size: 14px;
}

/* 手機上文字大一點 */
@media (max-width: 600px) {
    .marquee-text {
        font-size: 15px;
    }
}

/* 左往右滾動效果 */
@keyframes marquee {
    0%   { transform: translate(0, 0); }
    100% { transform: translate(-100%, 0); }
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# ===============================
# 💡 肌肉小知識 / 冷笑話清單
# ===============================
MUSCLE_TRIVIA = [
    "💡 小知識：人體大概有超過 600 塊骨骼肌，全部背完的人可以自稱『人體字典』 📚",
    "😆 冷笑話：為什麼肱二頭肌很愛照鏡子？因為它一直想確認自己有沒有『二心』（二頭）💘",
    "💡 小知識：臀大肌是人體最大的肌肉，負責站起來、走路、上樓梯，久坐會讓它生氣 🍑",
    "😆 冷笑話：肌肉跟成績很像，不練就會流失，不讀就會消失 📉",
    "💡 小知識：心臟也是一種肌肉（心肌），一天大概跳 10 萬次，自動幫你複習 ❤️",
    "💡 小知識：外眼肌讓你快速轉動眼球，上課偷看投影片超順暢 👀",
    "😆 冷笑話：今天不訓練的肌肉，明天就會變成你討厭的體脂肪 🍟",
    "💡 小知識：咀嚼肌群（像 masseter 咬肌）非常有力，可以咬碎很多東西…包括考前焦慮？🦷",
    "💡 小知識：前鋸肌（Serratus anterior）因形狀被叫做『拳擊肌』，出拳時會用到 👊",
    "😆 冷笑話：為什麼物治系的學生肌肉都很聰明？因為他們每天都在『用腦記肌』🧠"
]

# ===============================
# 📁 永遠讀 GitHub 最新 CSV
# ===============================
df = pd.read_csv(
    "https://raw.githubusercontent.com/chenyouhui0729/muscle-helper/main/muscles.csv"
)
# 避免 NaN 影響顯示
df = df.fillna("（未填寫）")

# ===============================
# 🔍 肌肉搜尋功能
# ===============================
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

# ===============================
# 🔗 KenHub 搜尋按鈕（自動帶入肌肉名稱）
# ===============================
def kenhub_button(muscle):
    eng = quote_plus(muscle["english_name"])
    query = f"site:kenhub.com {eng}"
    url = f"https://www.google.com/search?tbm=isch&q={query}"

    st.markdown(
        f'<a href="{url}" target="_blank" class="big-btn">🔍 點我開啟網站看圖片</a>',
        unsafe_allow_html=True
    )

# ===============================
# 🎲 產生一題隨機測驗
# ===============================
QUIZ_FIELD_MAP = {
    "origin": "起點 Origin",
    "insertion": "終點 Insertion",
    "innervation": "神經 Innervation",
    "actions": "動作 Actions",
}

def generate_quiz(df, field_key):
    # 從有資料的列中抽
    valid_df = df[df[field_key].notna() & (df[field_key] != "（未填寫）")]
    if valid_df.empty:
        return None

    # 隨機抽一塊肌肉
    muscle = valid_df.sample(1).iloc[0]
    correct_answer = muscle[field_key]

    # 產生錯誤選項
    all_candidates = (
        valid_df[field_key]
        .dropna()
        .unique()
        .tolist()
    )
    all_candidates = [c for c in all_candidates if c != correct_answer]

    if len(all_candidates) >= 3:
        distractors = random.sample(all_candidates, 3)
    else:
        distractors = all_candidates

    options = [correct_answer] + distractors
    random.shuffle(options)

    return {
        "muscle_ch": muscle["chinese_name"],
        "muscle_en": muscle["english_name"],
        "field_key": field_key,
        "field_label": QUIZ_FIELD_MAP[field_key],
        "correct": correct_answer,
        "options": options,
    }

# ===============================
# 🧠 主程式
# ===============================
def main():
    st.title("🐥 肌智救星 - 肌肉學習助手（網頁版 Prototype）")

    # 🔁 每 60 秒自動刷新一次，用來輪播小知識 / 冷笑話
    count = st_autorefresh(interval=60 * 1000, key="trivia_refresh")
    idx = count % len(MUSCLE_TRIVIA)

    # 📰 跑馬燈顯示小知識 / 冷笑話
    trivia_text = MUSCLE_TRIVIA[idx]
    st.markdown(
        f"""
        <div class="marquee-container">
            <div class="marquee-text">{trivia_text}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 也給使用者一個手動換一句的按鈕
    if st.button("換一句小知識 / 冷笑話 🔄"):
        st.session_state["trivia_refresh"] = st.session_state.get("trivia_refresh", 0) + 1
        st.experimental_rerun()

    # =======================
    # 🔎 肌肉查詢區
    # =======================
    st.subheader("🔍 肌肉資料查詢")
    keyword = st.text_input("👉 請輸入肌肉名稱（中/英文）：", "")

    if keyword:
        muscle = find_muscle(df, keyword)
        if muscle is not None:

            st.markdown(f"### 💪 {muscle['chinese_name']} / {muscle['english_name']}")

            # 🔗 KenHub 搜尋按鈕
            kenhub_button(muscle)

            st.write("---")

            # 📌 肌肉資訊
            st.write(f"📍 **起點 Origin：** {muscle['origin']}")
            st.write(f"🎯 **終點 Insertion：** {muscle['insertion']}")
            st.write(f"⚡ **神經 Innervation：** {muscle['innervation']}")
            st.write(f"🩸 **血管 Blood supply：** {muscle['blood_supply']}")
            st.write(f"🏃 **動作 Actions：** {muscle['actions']}")

        else:
            st.error("找不到這塊肌肉 😢 請換另一個關鍵字試試看！")

    st.info("✨ 提示：可輸入：肱二頭肌、三角肌、biceps、deltoid…")

    st.write("---")

    # =======================
    # 🎲 隨機抽考區塊
    # =======================
    st.subheader("🎲 隨機抽考 - 肌肉小測驗")

    # 選擇考題類型
    quiz_field = st.selectbox(
        "想被考哪一個項目？",
        options=list(QUIZ_FIELD_MAP.keys()),
        format_func=lambda k: QUIZ_FIELD_MAP[k],
    )

    # 初始化 session_state
    if "quiz" not in st.session_state:
        st.session_state["quiz"] = None
    if "quiz_answer" not in st.session_state:
        st.session_state["quiz_answer"] = None

    col_q1, col_q2 = st.columns([1, 1])

    with col_q1:
        if st.button("出一題 🎲"):
            quiz = generate_quiz(df, quiz_field)
            if quiz is None:
                st.warning("目前這個欄位沒有足夠的資料可以出題 🥲")
            else:
                st.session_state["quiz"] = quiz
                st.session_state["quiz_answer"] = None

    with col_q2:
        if st.button("清除本題 ↩️"):
            st.session_state["quiz"] = None
            st.session_state["quiz_answer"] = None

    quiz = st.session_state.get("quiz", None)

    if quiz is not None:
        st.markdown(
            f"**題目：** 請問 **{quiz['muscle_ch']} / {quiz['muscle_en']}** 的 **{quiz['field_label']}** 是哪一個？"
        )

        # 選項
        chosen = st.radio(
            "請選出正確答案：",
            quiz["options"],
            index=0 if st.session_state["quiz_answer"] is None else quiz["options"].index(
                st.session_state["quiz_answer"]
            ) if st.session_state["quiz_answer"] in quiz["options"] else 0,
        )

        if st.button("提交答案 ✅"):
            st.session_state["quiz_answer"] = chosen
            if chosen == quiz["correct"]:
                st.success("答對了！🎉 你的肌肉記憶正在變強 💪")
            else:
                st.error("答錯了 😢 再試試看！")
                st.info(f"✅ 正確答案是：{quiz['correct']}")

            # 額外顯示該肌肉完整資訊
            # 從 df 查回完整那一列
            muscle_row = df[
                (df["english_name"] == quiz["muscle_en"])
                & (df["chinese_name"] == quiz["muscle_ch"])
            ]
            if not muscle_row.empty:
                m = muscle_row.iloc[0]
                st.write("---")
                st.markdown(f"**📚 額外複習：{m['chinese_name']} / {m['english_name']}**")
                st.write(f"📍 起點 Origin：{m['origin']}")
                st.write(f"🎯 終點 Insertion：{m['insertion']}")
                st.write(f"⚡ 神經 Innervation：{m['innervation']}")
                st.write(f"🩸 血管 Blood supply：{m['blood_supply']}")
                st.write(f"🏃 動作 Actions：{m['actions']}")

    else:
        st.caption("按「出一題 🎲」開始測驗吧！")

# ===============================
if __name__ == "__main__":
    main()
