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

.marquee-container {
    overflow: hidden;
    white-space: nowrap;
    background: #ffe9f0;
    border-radius: 999px;
    padding: 8px 16px;
    border: 1px solid #ffb6c9;
    margin-bottom: 12px;
}

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
    "💡 小知識：咀嚼肌 Masseter 是全身最有力的肌肉之一 🦷",
    "💡 小知識：心肌一天跳 10 萬次，它比你更努力 ❤️",
]

# ===============================
# CSV
# ===============================
df = pd.read_csv(
    "https://raw.githubusercontent.com/chenyouhui0729/muscle-helper/main/muscles.csv"
).fillna("（未填寫）")

# ===============================
# 搜尋肌肉
# ===============================
def find_muscle(df, keyword):
    k = keyword.strip().lower()
    mask = df["english_name"].str.lower().str.contains(k) | df["chinese_name"].str.contains(keyword)
    return df[mask].iloc[0] if mask.any() else None

# ===============================
# KenHub 按鈕
# ===============================
def kenhub_button(muscle):
    eng = quote_plus(muscle["english_name"])
    url = f"https://www.google.com/search?tbm=isch&q=site:kenhub.com+{eng}"
    st.markdown(f'<a href="{url}" target="_blank" class="big-btn">🔍 點我開啟網站看圖片</a>', unsafe_allow_html=True)

# ===============================
# 小測驗
# ===============================
QUIZ_FIELD_MAP = {
    "origin": "起點 Origin",
    "insertion": "終點 Insertion",
    "innervation": "神經 Innervation",
    "actions": "動作 Actions",
}

def generate_quiz(df, field):
    valid = df[df[field] != "（未填寫）"]
    if valid.empty:
        return None

    muscle = valid.sample(1).iloc[0]
    correct = muscle[field]

    wrong = valid[field].unique().tolist()
    wrong = [w for w in wrong if w != correct]

    distractors = random.sample(wrong, min(3, len(wrong)))
    options = [correct] + distractors
    random.shuffle(options)

    return {
        "muscle_ch":_
