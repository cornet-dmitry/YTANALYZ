import os

from googleapiclient.discovery import build

import streamlit as st
import requests

import pandas as pd
import io

from colorstyle import color_style

from openpyxl import load_workbook
from openpyxl.drawing.image import Image
from openpyxl.styles import PatternFill


API_KEY = "AIzaSyA27hbQSvUhbU80GKf607Atnb0mk0dCCT4"
file_path = 'output.xlsx'
excel_pattern = 'pattern.xlsx'


def get_service():
    service = build('youtube', 'v3', developerKey=API_KEY)
    return service


def get_channel_subs_count(channel_id):
    r = get_service().channels().list(id=channel_id, part='snippet,statistics').execute()
    return r['items'][0]['statistics']['subscriberCount']


# Функция для добавления новой строки в Excel файл
def append_to_excel(file_path, data):

    if os.path.isfile(file_path) is False:
        # Загружаем оригинальный файл
        wb = load_workbook(excel_pattern)
        # Сохраняем его под новым именем
        wb.save(file_path)

    workbook = load_workbook(file_path)
    sheet = workbook.active

    max_rows = sheet.max_row
    target_row = max_rows + 1
    cell_value_id = sheet.cell(row=max_rows, column=1).value

    sheet.row_dimensions[target_row].height = 135

    sheet.cell(row=max_rows + 1, column=1, value=int(cell_value_id) + 1)
    sheet.cell(row=max_rows + 1, column=2, value=data[0])
    sheet.cell(row=max_rows + 1, column=3, value=data[1])

    # Вставьте изображение
    img = Image(data[2])
    # Установите анкор изображения в D и соответствующую строку
    img.anchor = f"D{target_row}"
    sheet.add_image(img)

    sheet.cell(row=max_rows + 1, column=5, value=data[3])
    sheet.cell(row=max_rows + 1, column=6, value=data[4])
    sheet.cell(row=max_rows + 1, column=7, value=data[5])
    sheet.cell(row=max_rows + 1, column=8, value=data[6])

    sheet.cell(row=max_rows + 1, column=9, value=data[7])
    sheet[f'I{target_row}'].fill = PatternFill(start_color=color_style[data[7].split('-')[0]],
                                               end_color=color_style[data[7].split('-')[0]],
                                               fill_type='solid')
    try:
        workbook.save(file_path)
    except Exception as ex:
        st.error(f"Возникла ошибка при сохранении таблицы: {ex}")

    st.success(f"Видео добавлено в таблицу! Всего строк в таблице: {max_rows - 1}")


def load_table_info(file_path):
    if os.path.isfile(file_path):
        try:
            data = pd.read_excel(file_path)
            st.dataframe(data[1:])  # Выводим таблицу на страницу
        except Exception as ex:
            st.error(f"Ошибка при загрузке файла: {ex}")


def get_video_info(video_id):
    #  snippet,statistics,contentDetails
    r = get_service().videos().list(id=video_id, part='snippet, statistics, contentDetails').execute()

    channelID = r['items'][0]['snippet']['channelId']
    channelSubsCount = get_channel_subs_count(channelID)

    videoTitle = r['items'][0]['snippet']['title']
    videoDatePublish = r['items'][0]['snippet']['publishedAt']
    videoViewsCount = r['items'][0]['statistics']['viewCount']

    videoDuration = r['items'][0]['contentDetails']['duration']
    duration = videoDuration.replace("PT", "").replace("S", "")
    duration_on_write = str(duration.split('M')[0] + ":" + duration.split('M')[1])

    urlPreview = r['items'][0]['snippet']['thumbnails']['medium']['url']
    p = requests.get(urlPreview)
    previewPath = f"previews\{video_id}.jpg"
    out = open(previewPath, "wb")
    out.write(p.content)
    out.close()

    videos_data = [f"https://www.youtube.com/watch?v={video_id}",
                   videoTitle,
                   previewPath,
                   videoViewsCount,
                   channelSubsCount,
                   duration_on_write,
                   round(int(videoViewsCount) / int(channelSubsCount), 2),
                   videoDatePublish.split('T')[0]]

    append_to_excel(file_path, videos_data)


def main():
    st.page_link("main.py", label="На главную", icon="⬅️")
    st.title("АНАЛИТИКА—ХУИТИКА | Полноформатные видео")

    yt_link = st.text_input("Ссылка на ютуб ролик")

    correct_link = str(yt_link.split('=')[-1])

    try:
        get_video_info(correct_link)
    except IndexError:
        if correct_link != "":
            st.error(f"Возникла ошибка: Неккоректно указана ссылка!")
    except PermissionError:
        st.error(f"Возникла ошибка: Возможно, у вас открыл Excel файл. Закройте его и повторите попытку")
    except Exception as ex:
        st.error(f"Возникла ошибка: {ex}")

    load_table_info(file_path)


if __name__ == "__main__":
    main()
