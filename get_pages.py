from bs4 import BeautifulSoup
import requests
import json
import time

def download_page(url):
    ''' Функция для скачивания интернет страницы '''
    # try:
    response = requests.get(url)
    if response.status_code != 200:
        time.sleep(0.01)
        return None
    return response.content

def get_text_from_html(html):
    ''' Функция для получения текста и заголока из html '''
    soup = BeautifulSoup(html, features="html.parser")
    texts = soup.find_all(class_="l-island-a")
    text = ""
    for part in texts:
        if(part.find("p") is None):
            continue
        text += part.find("p").get_text()

    title = soup.find('title').string
    text = " ".join(text.split("\n"))
    return {'title': title, 'text': text}

def collect_texts(corpus_size):
    ''' Функция для получения текстов для корпуса '''
    url_prefix = 'https://vc.ru/marketing/'
    page_num = 699132
    num_of_pages = 0
    texts = []
    while (num_of_pages < corpus_size):
        page_num -= 1
        url = url_prefix + str(page_num)
        html = download_page(url)
        if page_num % 50 == 0:
            print(page_num, num_of_pages)
        if html is None:
            continue
        time.sleep(0.3)
        text_info = get_text_from_html(html)
        text_info['url'] = url
        texts.append(text_info)
        num_of_pages += 1
    return texts

def make_texts_file(corpus_size):
    ''' Функция для получения json файла с текстами '''
    texts = collect_texts(corpus_size)
    with open('texts.json', 'w') as fp:
        json.dump(texts, fp)