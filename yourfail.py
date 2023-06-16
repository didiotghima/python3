# from aiogram import Bot, Dispatcher, types, executor
# from aiogram.dispatcher.filters.state import State, StatesGroup
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from aiogram.dispatcher.storage import FSMContext
# from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
# from config import token


# bot = Bot(token)
# storage = MemoryStorage()
# dp = Dispatcher(bot, storage=storage)

# Keyboard_buttons = [
#     KeyboardButton('/start'),
#     KeyboardButton('/help'),
#     KeyboardButton('/milling'),
#     KeyboardButton('/test'),
#     KeyboardButton('Привет'),
#     KeyboardButton('привет'),
#     KeyboardButton('/About_Me')
# ]
# Keyboard_one = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(*Keyboard_buttons)

# @dp.message_handler(commands='start')
# async def start(message:types.Message):
#     await message.answer(f"Привет {message.from_user.full_name}!", reply_markup=Keyboard_one)
#     await message.answer(f"""Geeks готов к услугам
# команды которые существуют
# /test,/help
# {message.from_user.full_name}
#                          """)
    
# @dp.message_handler(commands='help')
# async def start(message:types.Message):
#     await message.answer("Чем я могу вам помочь?")
    
# @dp.message_handler(text='Привет')
# async def hello(message:types.Message):
#     await message.answer("Приветствую")
    
# @dp.message_handler(text='привет')
# async def hello(message:types.Message):
#     await message.reply("Приветствую")

# @dp.message_handler(commands='test')
# async def testing(message:types.Message):
#     await message.answer_dice()

# class MailingState(StatesGroup):
#     text = State()

# @dp.message_handler(commands='milling')
# async def milling(message:types.Message):
#     if message.from_user.id in [5771196980]:
#        await message.reply("Введите текст для рассылки:")
#        await MailingState.text.set()
#     else:
#         await message.answer("у тебя нету прав к этой функции")
       
# @dp.message_handler(state=MailingState.text)
# async def send_mailing_text(message:types.Message, state:FSMContext):
#     await message.answer("начинаю рассылку...")
#     await message.answer("Рассылка окончена!")
#     await state.finish() 

# @dp.message_handler(commands='About_Me')
# async def About_Me(message:types.Message):
#     await message.answer("Приветствую я телеграмм бот который может вам помоч в необходимой случий.")


# @dp.message_handler()
# async def not_foun(message:types.Message):
#      await message.answer("Я вас не понял введите /help")
    
# executor.start_polling(dp)
