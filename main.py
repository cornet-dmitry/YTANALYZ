import shutil

import streamlit as st
import os
import config
from config import USER_CREDENTIALS


st.set_page_config(
    page_title="АНАЛИТИКА YouTube"
)


def main():
    # Инициализация session_state, если ключи ещё не созданы
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    if "username" not in st.session_state:
        st.session_state["username"] = None

    # Проверяем, авторизован ли пользователь
    if not st.session_state["authenticated"]:
        show_login()
    else:
        # Получаем имя пользователя и создаем уникальный файл для него
        username = st.session_state["username"]
        config.file_path = f"{username}_output.xlsx"
        st.success(f"Добро пожаловать, {username}! Хорошей и продуктивной вам работы!")

        st.title("АНАЛИТИКА—ХУИТИКА")

        col1, col2 = st.columns(2)
        col1.page_link("pages/2_full_videos.py", label="Полноформатные видео", icon="🎬")
        col2.page_link("pages/3_shorts_videos.py", label="Вертикальные видео", icon="🩳")

        if os.path.isfile(config.file_path):
            st.warning(f"Внимание! У вас уже имеется Excel таблица: `{config.file_path}`\n"
                       "Новые видео будут добавляться в уже существующую таблицу!\n"
                       "Вы можете продолжить, либо удалить старую таблицу.")

            btn1, btn2 = st.columns(2)

            if btn2.button("Удалить таблицу"):
                vote()

            # Добавляем кнопку для скачивания Excel файла
            with open(config.file_path, 'rb') as f:
                download_data = f.read()

            if btn1.download_button(
                label="Скачать Excel файл",
                data=download_data,
                file_name=os.path.basename(config.file_path),
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            ):
                st.balloons()

        st.title("")

        st.subheader("ИСПРАВЛЕНИЯ И УЛУЧШЕНИЯ (на 17.12.2024)")
        st.write("1. ✅ Добавлена система авторизации пользователя по логину и паролю")
        st.write("2. ✅ У каждого пользователя теперь своя активная таблица")
        st.write("3. ✅ Добавлен автоматический перевод названия видео на русский язык (гугл переводчик)")
        st.write("4. ✅ Реализован запрет на дубликат (повторение) ссылок с одним URL в таблице")
        st.write("5. ✅ Обновлено визуальное отображение данных из Excel таблицы на странице веб-приложения")
        st.write("6. ❌ Невозможно реализовать удаление конкретной строки из Excel таблицы в связи с техническими "
                 "особенностями самого Excel")


def show_login():
    st.title("Вход в систему")
    username = st.text_input("Логин")
    password = st.text_input("Пароль", type="password")

    if st.button("Войти"):
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state["authenticated"] = True
            st.session_state["username"] = username  # Сохраняем имя пользователя
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
        os.remove(config.file_path)
        clear_folder("previews")
        st.rerun()


if __name__ == "__main__":
    main()