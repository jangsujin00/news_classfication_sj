from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pandas as pd
import re
import time
import datetime

category = ['politics', 'Economic', 'Social', 'Culture', 'World','IT']
pages = [101, 101, 101, 71, 94, 73]          # page = [167, 377, 505, 71, 94, 73] 데이터 맞춰줘야 함. 적은 걸 늘리던가, 많은 걸 줄이던가
                                             # (많은 건 100, 적은 건 하나 줄여서 놓고 for문 돌릴 때 index에 하나 추가 해야 하므로 +1 더해줌)
url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100#&date=%2000:00:00&page=2'

options = webdriver.ChromeOptions()
# options.add_argument('hardless')          # 창 실행되는데 보이지는 않게
options.add_argument('lang=kr_KR')
driver = webdriver.Chrome('./chromedriver', options=options)
df_title = pd.DataFrame()

for i in range(0, 6):                       # section
    titles = []
    for j in range(1, 11):            # page
        url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=10{}#&date=%2000:00:00&page={}'.format(i, j)
        driver.get(url)
        time.sleep(0.2)
        for k in range(1, 5):       # x_path
            for l in range(1, 6):   # x_path
                x_path = '//*[@id="section_body"]/ul[{}]/li[{}]/dl/dt[2]/a'.format(k, l)
                try:
                    title = driver.find_element('xpath', x_path).text
                    title = re.compile('[^가-힣]').sub(' ', title)
                    titles.append(title)
                except NoSuchElementException as e:
                    x_path = '//*[@id="section_body"]/ul[{}]/li[{}]/dl/dt/a'.format(k, l)
                    title = driver.find_element('xpath', x_path).text
                    title = re.compile('[^가-힣]').sub(' ', title)
                    titles.append(title)
                except:
                    print('error', i, j, k, l)

        if j % 10 == 0:
            df_section_title = pd.DataFrame(titles, columns=['titles'])
            df_section_title['category'] = category[i]
            df_title = pd.concat([df_title, df_section_title], ignore_index=True)
            df_title.to_csv('./crawling_data/crawling_data{}_{}.csv'.format(category[i], j))
            titles = []

    df_section_title = pd.DataFrame(titles, columns=['titles'])
    df_section_title['category'] = category[i]
    df_title = pd.concat([df_title, df_section_title], ignore_index=True)
print(df_title.head())
print(df_title.category.value_counts())