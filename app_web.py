def main():
    st.title("🐥 肌智救星 - 肌肉學習助手（網頁版 Prototype）")

    # 🔁 每 60 秒自動刷新一次，用來輪播小知識 / 冷笑話
    # 🚨 改用不同的 key，避免跟 session_state 打架
    count = st_autorefresh(interval=60 * 1000, key="trivia_auto")

    # 手動換句數量（自己維護一個 clicks 計數器）
    if "trivia_clicks" not in st.session_state:
        st.session_state["trivia_clicks"] = 0

    # 目前要顯示第幾句：自動 + 手動
    idx = (count + st.session_state["trivia_clicks"]) % len(MUSCLE_TRIVIA)

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

    # 手動換一句的按鈕（不再改動 trivia_auto）
    if st.button("換一句小知識 / 冷笑話 🔄"):
        st.session_state["trivia_clicks"] += 1
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

    quiz_field = st.selectbox(
        "想被考哪一個項目？",
        options=list(QUIZ_FIELD_MAP.keys()),
        format_func=lambda k: QUIZ_FIELD_MAP[k],
    )

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
