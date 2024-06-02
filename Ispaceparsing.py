import sqlite3
import csv
import time
from bs4 import BeautifulSoup
import requests
import bs4.element


index = 1

while index < 11:

    url = f'https://ispace.ge/en/iphone?page={index}'
    response = requests.get(url)
    data = BeautifulSoup(response.text, 'html.parser')
    info = data.find('div', class_='row mb-12').ul
    phones = info.find_all('li')

    for phone in phones:
        model = phone.find('h2')

        if model is not None:
            details = model.text.split(',')
            model = details[0].strip()
            memory = details[1].strip()
            color = details[2].strip()
        else:
            continue

        product_code = phone.find("p", class_='mb-1 caption').text.strip().split(":")[1]
        new_price = phone.find("span", class_='price-text__value').text.strip()
        currency = phone.find('span', class_='price-text__currency').text.strip()
        condition = phone.find("span", class_='v-chip__content')

        if type(condition) == bs4.element.Tag:
            condition = condition.text.strip()
        else:
            condition = None

        conn = sqlite3.connect('Ispace.sqlite')
        cursor = conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Phones
        (Id INTEGER PRIMARY KEY AUTOINCREMENT, 
        Model VARCHAR(50), 
        Color VARCHAR(50), 
        Memory VARCHAR(50),
        Code VARCHAR(50), 
        NewPrice INTEGER, 
        Currency VARCHAR(50),
        Conndition VARCHAR(40)
        )
        ''')

        cursor.executemany('''
        INSERT INTO Phones 
        (Model, Color, Memory, Code,NewPrice,Currency, Conndition)
        VALUES (?,?,?,?,?,?,?)
        ''', [(model, color, memory, product_code, new_price, currency, condition)])
        conn.commit()

        with open('Ispace.csv','a', encoding='utf-8_sig', newline='\n') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([model, color, memory, product_code, new_price, currency, condition])

    index += 1
    time.sleep(15)
    conn.close()
