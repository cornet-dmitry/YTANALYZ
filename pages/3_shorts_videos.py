import streamlit as st


def main():
    # Проверка авторизации
    if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
        st.error("Доступ запрещен. Пожалуйста, войдите в систему на главной странице.")
        return

    st.set_page_config(
        page_title="АНАЛИТИКА YouTube"
    )
    st.page_link("main.py", label="На главную", icon="⬅️")
    st.title("АНАЛИТИКА—ХУИТИКА | Вертикальные видео")
    st.write("Не ну тут пока что ничего нет")
    st.write("А вы что думали? В сказку попали?")
    st.write("Нееее....")
    st.write("Такая жизнь.")
    st.write("Такая жизнь..")
    st.write("Такая жизнь...")


if __name__ == "__main__":
    main()