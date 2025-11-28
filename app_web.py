def main():
    st.title("🐥 肌智救星 - 肌肉學習助手（網頁版 Prototype）")

    # ---- 自動刷新跑馬燈 ----
    auto_counter = st_autorefresh(interval=60_000, key="auto_marquee")
    idx = auto_counter % len(MUSCLE_TRIVIA)

    # ---- 肌肉搜尋 ----
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

        choice = st.radio("請選擇正確答案：", quiz["options"])

        if st.button("提交答案 ✅"):
            st.session_state["quiz_answer"] = choice
            if choice == quiz["correct"]:
                st.success("答對了！🎉 肌肉記憶加 +1 💪")
            else:
                st.error("答錯了 😢 再接再厲！")
                st.info(f"正確答案：{quiz['correct']}")

    else:
        st.caption("按「出一題 🎲」開始測驗吧！")

    st.write("---")
    st.write("---")

    # ---- 跑馬燈放在最底部（米白色 + 黑字）----
    trivia_text = MUSCLE_TRIVIA[idx]
    st.markdown(
        f"""
        <div style="
            overflow:hidden;
            white-space:nowrap;
            background:#f9f5e9;
            border-radius:999px;
            padding:10px 20px;
            border:1px solid #d6c9a8;
        ">
            <div style="
                display:inline-block;
                padding-left:100%;
                animation: marquee 18s linear infinite;
                color:#000;
                font-size:15px;
            ">
                {trivia_text}
            </div>
        </div>

        <style>
            @keyframes marquee {{
                0% {{ transform: translate(0,0); }}
                100% {{ transform: translate(-100%,0); }}
            }}
        </style>
        """,
        unsafe_allow_html=True
    )
