import json
import sys
import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome import options
from selenium.webdriver.common.by import By
import math
from bs4 import BeautifulSoup as bs
import keyboard
import psycopg2
from psycopg2.extras import execute_batch


def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
    except psycopg2.OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection

def execute_query(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Query executed successfully")
    except psycopg2.OperationalError as e:
        print(f"The error '{e}' occurred")

def create_database(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Query executed successfully")
    except psycopg2.OperationalError as e:
        print(f"The error '{e}' occurred")

def delete_rows(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Query executed successfully")
    except psycopg2.OperationalError as e:
        print(f"The error '{e}' occurred")

connection = create_connection(
    "postgres", "postgres", "password", "192.168.3.19", "5432"
)

#Передаем имя БД в которую будут записываться данные
db_name = 'db_drom3'


create_database_query = "CREATE DATABASE " + str(db_name)
try:
    create_database(connection, create_database_query)
except psycopg2.errors.DuplicateDatabase:
    print('БД уже существует')

connection = create_connection(
    db_name, "postgres", "password", "192.168.3.19", "5432"
)

create_car_table = """
CREATE TABLE IF NOT EXISTS car_drom (
  id SERIAL PRIMARY KEY,
  url TEXT NOT NULL,
  year INTEGER,
  region_number INTEGER,
  name TEXT,
  price INTEGER,
  model TEXT,
  brand_name TEXT,
  name_and_yer TEXT,
  bodyType TEXT,
  color TEXT,
  vehicleTransmission TEXT,
  date_time TIMESTAMP
)
"""
execute_query(connection, create_car_table)


print(datetime.now())
start_time = datetime.now()
options = options.ChromiumOptions()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
browser = webdriver.Chrome(options=options)
browser.implicitly_wait(0.1)

#список марок машин которые нас интересуют
model_car_list = ['kia','lada','hyundai','renault','chery','audi','bmw','haval','chery','chevrolet','citroen','daewoo','dodge','ford','geely','honda','lexus','mazda','mercedes-benz','mitsubishi','opel','peugeot','renault','skoda','toyota','volkswagen','volvo']

break_out_flag = False
index_all_car = int(1)
list_all_car = []

region_number = sys.argv[1]
#region_number = 1
#проходим по регионам
#for region_number in range(15, 17):
index_region_car = int(1)
check_url_region_number = 'https://auto.drom.ru/region' + str(region_number)
r = requests.get(check_url_region_number)
if r.status_code == 200:
    for model_car in model_car_list:
        #формируем строку для региона и модели
        URL = str(check_url_region_number) + '/' + str(model_car) + '/all/?unsold=1'
        print(URL)
        browser.get(URL)
        # поиск информации об общем количестве объявлений для расчета количества страниц
        draft_pages = browser.find_elements(By.XPATH, "//div[contains(@class, 'css-1ksi09z eckkbc90')]")
        if len(draft_pages) == 1:
            draft_max_car = (draft_pages[0].text).split()
        elif len(draft_pages) == 0:
            draft_pages = browser.find_elements(By.XPATH, "//div[contains(@role, 'tablist')]")
            try:
                draft_max_car = (draft_pages[1].text).split()
            except IndexError:
                print('Объявления данной марки в выбранном регионе отсутствуют')
                continue
        print(draft_max_car)
        if len(draft_max_car) <= 4:  # значит количество объявлений меньше 1к
            max_car = str(draft_max_car[0])  # если количество объявлений меньше 1к
        if len(draft_max_car) >= 5:  # значит количество объявлений больше 1к
            max_car = str(draft_max_car[0]) + str(draft_max_car[1])  # если количество объявлений больше 1к

        print('Количество объявлений в регионе с номером', region_number, 'и марки', model_car, '=', max_car)
        num_pages = math.ceil(int(max_car) / 20)

        if int(max_car) > 2000:
            print("Присутствует ограничение на максимальное количество страниц для региона", region_number, 'и модели', model_car)
            num_pages = 100
        print('Количество просматриваемых страниц', num_pages)
        n_pages = 1
        index_model_car = int(1)
        while n_pages < num_pages:
            if keyboard.is_pressed("q"):  # Клавиша для остановки цикла
                break_out_flag = True
                break
            # получаем текущую html
            html = browser.page_source
            soup = bs(html, 'html.parser')
            application_json_list = ((str(soup)).split('<script type="application/ld+json">'))

            # 1 - это краткий список всех объявлений на данной странице
            # 2 - 21 это строки с предложениями машин
            # перебираем все объявления на странице
            draft_all_offers_page = application_json_list[1]
            s_all_offers = draft_all_offers_page[:-9]
            all_offers_page = json.loads(s_all_offers)

            data = all_offers_page['offers']['offers']
            draft_list_all_offer_page = []
            for i in data:
                b = {}
                update_string = (i['url']).replace('\/', '/')
                year = ((i['name']).split(', '))[1]
                brand = ((i['name']).split(', '))[0]
                draft_model = brand.split(' ')
                draft_model.pop(0)
                model = ' '.join(draft_model)
                i['url'] = update_string
                b['name'] = brand
                b['price'] = i['price']
                b['url'] = i['url']
                b['model'] = model
                b['year'] = year
                draft_list_all_offer_page.append(b)

            draft_list_car = []
            for i in range(2, len(application_json_list) - 1):
                b = {}
                draft_jsonstr = (application_json_list[i])[:-9]
                car_dict = json.loads(draft_jsonstr)
                b['brand_name'] = car_dict['brand']['name']
                b['name_and_yer'] = car_dict['name']
                b['bodyType'] = car_dict['bodyType']
                try:
                    b['color'] = car_dict['color']
                except KeyError:
                    b['color'] = 'хз'
                try:
                    b['vehicleTransmission'] = car_dict['vehicleTransmission']
                except:
                    b['vehicleTransmission'] = 'хз'
                draft_list_car.append(b)

            for i in range(0, len(draft_list_all_offer_page)):
                b = {}
                b['url'] = draft_list_all_offer_page[i]['url']
                b['year'] = draft_list_all_offer_page[i]['year']
                b['region_number'] = region_number
                b['name'] = draft_list_all_offer_page[i]['name']
                b['price'] = draft_list_all_offer_page[i]['price']
                b['model'] = draft_list_all_offer_page[i]['model']
                b['brand_name'] = draft_list_car[i]['brand_name']
                b['name_and_yer'] = draft_list_car[i]['name_and_yer']
                b['bodyType'] = draft_list_car[i]['bodyType']
                b['color'] = draft_list_car[i]['color']
                b['vehicleTransmission'] = draft_list_car[i]['vehicleTransmission']
                b['date_time'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
                list_all_car.append(b)
                index_model_car += 1
                index_region_car += 1
                index_all_car += 1

            n_pages += 1
            # клацаем на номер следующей страницы
            pg_link = browser.find_element(By.LINK_TEXT, str(n_pages))
            pg_link.click()
        if break_out_flag:
            break
            # парсим объявления с последней страницы
        if n_pages == num_pages:
            # break
            # данный фрагмент кода повторяется надо оформить его как отдельную функцию чтобы быть крутанским крутаном
            html = browser.page_source
            soup = bs(html, 'html.parser')
            application_json_list = ((str(soup)).split('<script type="application/ld+json">'))
            draft_all_offers_page = application_json_list[1]
            s_all_offers = draft_all_offers_page[:-9]
            all_offers_page = json.loads(s_all_offers)
            data = all_offers_page['offers']['offers']
            draft_list_all_offer_page = []
            for i in data:
                b = {}
                update_string = (i['url']).replace('\/', '/')
                i['url'] = update_string
                year = ((i['name']).split(', '))[1]
                brand = ((i['name']).split(', '))[0]
                draft_model = brand.split(' ')
                draft_model.pop(0)
                model = ' '.join(draft_model)
                b['name'] = brand
                b['price'] = i['price']
                b['url'] = i['url']
                b['model'] = model
                b['year'] = year
                draft_list_all_offer_page.append(b)
                if keyboard.is_pressed("q"):  # Клавиша для остановки цикла
                    break_out_flag = True
                    break
            draft_list_car = []
            for i in range(2, len(application_json_list) - 1):
                b = {}
                draft_jsonstr = (application_json_list[i])[:-9]
                car_dict = json.loads(draft_jsonstr)
                b['brand_name'] = car_dict['brand']['name']
                b['name_and_yer'] = car_dict['name']
                b['bodyType'] = car_dict['bodyType']
                try:
                    b['color'] = car_dict['color']
                except KeyError:
                    b['color'] = 'хз'
                try:
                    b['vehicleTransmission'] = car_dict['vehicleTransmission']
                except:
                    b['vehicleTransmission'] = 'хз'
                draft_list_car.append(b)
                if keyboard.is_pressed("q"):  # Клавиша для остановки цикла
                    break_out_flag = True
                    break
            for i in range(0, len(draft_list_all_offer_page)):
                b = {}
                b['url'] = draft_list_all_offer_page[i]['url']
                b['year'] = draft_list_all_offer_page[i]['year']
                b['region_number'] = region_number
                b['name'] = draft_list_all_offer_page[i]['name']
                b['price'] = draft_list_all_offer_page[i]['price']
                b['model'] = draft_list_all_offer_page[i]['model']
                b['brand_name'] = draft_list_car[i]['brand_name']
                b['name_and_yer'] = draft_list_car[i]['name_and_yer']
                b['bodyType'] = draft_list_car[i]['bodyType']
                b['color'] = draft_list_car[i]['color']
                b['vehicleTransmission'] = draft_list_car[i]['vehicleTransmission']
                b['date_time'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
                list_all_car.append(b)
                index_model_car += 1
                index_region_car += 1
                index_all_car += 1
                if keyboard.is_pressed("q"):  # Клавиша для остановки цикла
                    break_out_flag = True
                    break
        print('Выгружено объявлений для региона', region_number, 'и марки авто', model_car, index_model_car - 1, 'штук')

    print('Выгружено объявлений в регионе', region_number, index_region_car - 1)
    query = "INSERT INTO car_drom " \
        "(url, year, region_number, name, price, model, brand_name, name_and_yer, bodyType, color, vehicleTransmission, date_time) " \
        "VALUES " \
        "(%(url)s, %(year)s, %(region_number)s, %(name)s, %(price)s, %(model)s, %(brand_name)s, %(name_and_yer)s, " \
        "%(bodyType)s, %(color)s, %(vehicleTransmission)s, %(date_time)s)"
    execute_batch(connection.cursor(), query, list_all_car)
    connection.commit()

end_time = datetime.now()

#удаляем старые строки
delete_rows_query = """
DELETE FROM car_drom
WHERE date_time < (current_date - 30)
"""
delete_rows(connection,delete_rows_query)

print('Выгружено суммарно объявлений', index_all_car - 1, 'в регионе', region_number)
print('Время выполения скрипта', (end_time - start_time))
