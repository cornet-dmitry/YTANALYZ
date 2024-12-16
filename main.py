import shutil

import streamlit as st
import os

file_path = 'output.xlsx'

st.set_page_config(
    page_title="АНАЛИТИКА YouTube"
)

# Заранее заданные логины и пароли
USER_CREDENTIALS = {
    "admin": "1234",
    "user": "password"
}


def main():
    # Проверяем, авторизован ли пользователь
    if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
        show_login()
    else:

        st.title("АНАЛИТИКА—ХУИТИКА")

        col1, col2 = st.columns(2)
        col1.page_link("pages/2_full_videos.py", label="Полноформатные видео", icon="🎬")
        col2.page_link("pages/3_shorts_videos.py", label="Вертикальные видео", icon="🩳")

        if os.path.isfile(file_path):
            st.warning("Внимание! У вас уже имеется Excel таблица!\n"
                       "Новые видео будут добавляться в уже существующую таблицу!\n"
                       "Вы можете продолжить, либо удалить старую таблицу.")

            btn1, btn2 = st.columns(2)

            if btn2.button("Удалить таблицу"):
                vote()

            # Добавляем кнопку для скачивания Excel файла
            with open(file_path, 'rb') as f:
                download_data = f.read()

            if btn1.download_button(
                label="Скачать Excel файл",
                data=download_data,
                file_name=os.path.basename(file_path),
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            ):
                st.balloons()

        st.title("")

        st.subheader("ИСПРАВЛЕНИЯ И УЛУЧШЕНИЯ (на 17.12.2024)")
        st.write("❌ Временно заблокирован вывод данных из таблицы на страницу Полноформатные видео")
        st.write("1. ✅ Добавлена система авторизации пользователя по логину и паролю")
        st.write("2. ✅ Добавлен автоматический перевод названия видео на русский язык (гугл переводчик)")
        st.write("3. ✅ Реализован запрет на дубликат (повторение) ссылок с одним URL в таболице")


def show_login():
    st.title("Вход в систему")
    username = st.text_input("Логин")
    password = st.text_input("Пароль", type="password")
    if st.button("Войти"):
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state["authenticated"] = True
            st.query_params.clear()  # Очищаем параметры URL
            st.rerun()
        else:
            st.error("Неверный логин или пароль")


def logout():
    st.session_state["authenticated"] = False
    st.query_params.clear()  # Очищаем параметры URL
    st.rerun()  # Перезагружаем страницу после выхода


def clear_folder(folder_path):
    # Удаляем всю папку и её содержимое, затем создаем её заново
    try:
        shutil.rmtree(folder_path)  # Удаляем папку и её содержимое
        os.makedirs(folder_path)  # Создаем папку заново
    except Exception as e:
        print(f'Не удалось очистить папку {folder_path}. Причина: {e}')


@st.dialog("Подтвердите свой выбор")
def vote():
    st.write("Вы уверены, что хотите удалить таблицу? Восстановить её будет нельзя!")
    if st.button("Всё равно удалить"):
        os.remove("output.xlsx")
        clear_folder("previews")
        st.rerun()


if __name__ == "__main__":
    main()