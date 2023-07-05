import requests, os, logging
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv

load_dotenv('.env')

bot =Bot(os.environ.get('token'))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)

def get_exchange_rate(currency):
    url = 'https://www.nbkr.kg/index.jsp?lang=RUS'
    response = requests.get(url=url)
    soup = BeautifulSoup(response.text, 'lxml')
    info_tag = soup.find_all('td', class_="exrate")

    for row in info_tag:
        cells = row.find_all('td')
        if len(cells) >= 2 and cells[0].text.strip() == currency:
            return cells[1].text.strip()

    return None

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(f"Здраствйте {message.from_user.full_name}, если хотите обменят деньги то введите команду /exchange...")

@dp.message_handler(commands=['exchange'])
async def exchange(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton(text="USD", callback_data='USD'),
        InlineKeyboardButton(text="EUR", callback_data='EUR'),
        InlineKeyboardButton(text="RUB", callback_data='RUB'),
        InlineKeyboardButton(text="KZT", callback_data='KZT')
    ]
    keyboard.add(*buttons)
    await message.answer("Выберите валюту, которую нужно поменять:", reply_markup=keyboard)

@dp.callback_query_handler()
async def button_click(callback_query: types.CallbackQuery):
    currency = callback_query.data
    exchange_rate = get_exchange_rate(currency)
    await callback_query.message.answer(f"Курс {currency}: {exchange_rate}")

executor.start_polling(dp)
