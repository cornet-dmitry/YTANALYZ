import shutil

import streamlit as st
import os

file_path = 'output.xlsx'

st.title("АНАЛИТИКА—ХУИТИКА")

col1, col2 = st.columns(2)
col1.page_link("pages/2_full_videos.py", label="Полноформатные видео", icon="🎬")
col2.page_link("pages/3_shorts_videos.py", label="Вертикальные видео", icon="🩳")


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

    btn1.download_button(
        label="Скачать Excel файл",
        data=download_data,
        file_name=os.path.basename(file_path),
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
