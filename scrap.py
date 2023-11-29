import os
import shutil

import requests
from bs4 import BeautifulSoup

import time
import random


def make_dataset(name: str) -> str:
    
    if os.path.exists(name):
        shutil.rmtree(name)    
    
    os.mkdir(name)
    
    for i in range(1, 6):
        os.mkdir(name + '/' + str(i))
    
    os.mkdir(name + '/' + "pagers")

    return name

def delete_sumbols(chars: str, stringe: str) -> str:

    str_2 = stringe
    
    for i in chars:
        str_2 = str_2.replace(i, '')
    
    return str_2 

def create_dataset(path_for_dataset:str): 

    dataset = make_dataset(path_for_dataset)

    a = b = c = d = f = 0

    dataset_folders = { '1': a ,'2':b, '3':c, '4':d, '5':f }

    headers = {"Accept": "*/*", "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0"}

    page = '2'

    while a < 1000 and b < 1000 and c < 1000 and d < 1000 and f < 1000:

        url = f"https://www.livelib.ru/reviews/~{page}#reviews"

        wait = random.randint(5, 15)
        
        print(f"\n{url} wait {wait} second page#{page}")
    
        page = str(int(page) + 1)
            
        time.sleep(wait)


        html_page = requests.get(url, headers=headers).content.decode('utf-8')
    
        soup = BeautifulSoup(html_page, 'lxml')

        #зафиксировать результат
        with open(f"{dataset}/pagers/{str(int(page) - 1)}.html", 'w') as file:
            file.write(soup.prettify())

        data_reviews = soup.find_all('div', class_="lenta-card")

        for lenta_card in data_reviews:
        
            stars = lenta_card.find('span', class_="lenta-card__mymark")

            review = lenta_card.find('div', class_="lenta-card__text without-readmore")

#Сссылка раскрывается при открытии скрипта:
#<a href="javascript:void(0);" class="read-more__link" data-rand_id="3297640" data-object_alias="review" data-object_id="3680323" data-object_text_action="expand" onclick="feed_object_text_show_link_process($(this));">Развернуть</a>
#Спросить с помощью чего открывать подобные ссылки или узнать самому

        #review = lenta_card.find('div', class_="lenta-card__text-review-full")
        
            if not stars or not review:
                continue
        
            stars = delete_sumbols("йцукенгшщзхъфывапролджэячсмитьбюЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ \t\n", stars.text)

            review = review.text.strip()

            for i in dataset_folders:
                if i == str(int(float(stars))):
                    path = dataset + '/' + i + '/' + str(dataset_folders[i]).rjust(4, '0')

                    with open(path, 'w') as file:
                        file.write(review)

                    dataset_folders[i] += 1            


if __name__ == '__main__':
    print("Web scraping")
