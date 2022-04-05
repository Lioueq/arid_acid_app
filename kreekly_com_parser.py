from bs4 import BeautifulSoup
import requests

"""Парсер сайта kreekly.com. Обновляет пары слов в word_couples.txt"""


def word_couples_updater():
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/91.0.4472.164 Safari/537.3'
    }
    url = 'https://kreekly.com/random/'

    word_couples = []

    for cycle_count in range(2):
        src = requests.get(url=url, headers=headers).text
        soup = BeautifulSoup(src, 'lxml')
        word_container_block = soup.find('div', class_='list-words view-card').find_all('div', class_='dict-word')
        for word_couple_data in word_container_block:
            en_word = word_couple_data.find('span', class_='eng').text
            ru_word = word_couple_data.find('span', class_='rus').text
            if len(en_word.split()) > 1 or len(ru_word.split()) > 1:
                continue
            word_couple = f'{en_word} - {ru_word}\n'
            if len(word_couple[:-2]) <= 20:
                word_couples.append(word_couple)

    with open('data/word_couples.txt', encoding='utf-8', mode='w') as file:
        file.writelines(word_couples)
