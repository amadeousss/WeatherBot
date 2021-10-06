import logging, requests, json
from aiogram import Bot, Dispatcher, executor, types
import sqlite3
from db import is_in_table, db_table_val, db_update_value

from open('tgtoken.txt', 'r') as f:
    API_TOKEN = f.read().strip()

from open('weathertoken.txt', 'r') as f:
    OPEN_WEATHER_TOKEN = '' = f.read().strip()

BASE_URL = 'https://api.openweathermap.org/data/2.5/weather?'
CITY = ''
CHANGING_CITY = 0
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_bot(message: types.Message):
    await message.reply('Привет, хочешь узнать погоду? Напиши /city чтобы ввести твой город')

@dp.message_handler(commands=['city'])
async def set_city(message: types.Message):
    global CHANGING_CITY
    CHANGING_CITY = 1
    await message.reply('Введи название твоего города')

@dp.message_handler(commands=['weather'])
async def get_weather(message: types.Message):
    try:
        URL = BASE_URL + 'q=' + CITY + '&appid=' + OPEN_WEATHER_TOKEN + '&units=metric&lang=ru'
        response = requests.get(URL)
        data = response.json()
        main = data['main']
        city = data['name']
        temperature = main['temp']
        humidity = main['humidity']
        report = data['weather']
        feels_like = main['feels_like']
        await message.answer((f'{city:-^30}\nТемпература: {round(temperature)}°\nОщущается как {round(feels_like)}°\nВлажность: {humidity}%\nПогода: {report[0]["description"]}'))
    except:
        await message.answer(f'Ошибка запроса')

@dp.message_handler()
async def check_city(message: types.Message):
    global CHANGING_CITY, CITY
    if message.text[0] == "/" or CHANGING_CITY == 0:
        return
    try:
        URL = BASE_URL + 'q=' + message.text + '&appid=' + OPEN_WEATHER_TOKEN + '&units=metric&lang=ru'
        response = requests.get(URL)
        if response.status_code == 200:
            CITY = message.text
            if is_in_table(message.from_user.id):
                db_update_value(message.from_user.id, message.text)
            else:
                db_table_val(message.from_user.id, message.from_user.username, message.text)
            CHANGING_CITY = 0
            await message.reply(f'{CITY} - город установлен! Напишите /weather')
        else:
            await message.reply('Проверьте название города')
    except:
        await message.reply('Error')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
