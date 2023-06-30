from aiogram import Bot, Dispatcher, types, executor 
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.storage import FSMContext
from email.message import EmailMessage
from pytube import YouTube
from dotenv import load_dotenv
import smtplib, sqlite3, logging, os, time

load_dotenv('.env')


bot = Bot(os.environ.get('token'))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)

inline_buttons = [
    InlineKeyboardButton('Скачать аудио', callback_data='audio'),
    InlineKeyboardButton('Скачать видео', callback_data='video'),
    InlineKeyboardButton('Информация о видео', callback_data='info'),
    InlineKeyboardButton('Введите email', callback_data='email')
]
inline_keyboard = InlineKeyboardMarkup().add(*inline_buttons)

database = sqlite3.connect('email.db')
cursor = database.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    user_id INT,
    chat_id INT,
    username VARCHAR(255),
    first_name VARCHAR(255),
    last_name VARCHAR(255)
);
""")
cursor.connection.commit()

class FormatState(StatesGroup):
    url = State()
    format_url = State()

class AudioState(StatesGroup):
    url = State()

class VideoState(StatesGroup):
    url = State()
    info = State()

class EmailState(StatesGroup):
    email = State()

@dp.message_handler(commands='start')
async def start(message:types.Message):
    cursor.execute(f"SELECT * FROM users WHERE user_id = {message.from_user.id};")
    result = cursor.fetchall()
    if result == []:
        cursor.execute(f"""INSERT INTO users (user_id, chat_id, username, first_name,
                    last_name) VALUES ({message.chat.id}, 
                    '{message.from_user.username}',
                    '{message.from_user.first_name}', 
                    '{message.from_user.last_name}',
                    '{time.ctime()}');
                    """)
    cursor.connection.commit()
    await message.answer(f"Привет {message.from_user.full_name}!\nЯ помогу тебе скачать видео или же аудио с ютуба. Просто отправь ссылку из ютуба, и отрпвлю на почту на кототорую вы отправили.)", reply_markup=inline_keyboard)

@dp.callback_query_handler(lambda call: call)
async def all_inline(call):
    if call.data == 'audio':
        await bot.send_message(call.message.chat.id, 'Отправьте ссылку на аудио')
        await AudioState.url.set()
    elif call.data == 'video':
        await bot.send_message(call.message.chat.id, 'Отправьте ссылку на видео')
        await VideoState.url.set()
    elif call.data == 'email':
        await bot.send_message(call.message.chat.id, 'Отправьте email на которую вы хотите отправить, видио или же аудио.')
        await EmailState.to_email.set()


class EmailState(StatesGroup):
    to_email = State()
    subject = State()
    message = State()
    audio = State()
    video = State()

# @dp.message_handler(commands='send')
# async def send_command(message:types.Message):
#     await message.answer('Введите почту на которую нужно отправить сообщение', reply_markup=inline_keyboard)
#     await EmailState.to_email.set()

@dp.message_handler(state=EmailState.to_email)
async def get_subject(message:types.Message, state:FSMContext):
    await state.update_data(to_email=message.text)
    await message.answer('Что вы хотите отрпавить на почту, видио или де аудио...')
    await EmailState.subject.set()

# @dp.message_handler(commands='dowloand')
# async def yt_get(message:types.Message, state:FSMContext):
#     await message.reply("Дайте ссылку на видио или же аудио...")

@dp.message_handler(state=AudioState.url)
async def download_audio(message:types.Message, state:FSMContext):
    yt = YouTube(message.text, use_oauth=True)
    await message.answer("Скачиваем аудио, ожидайте...")
    try:
        yt.streams.filter(only_audio=True).first().download('audio', f'{yt.title}.mp3')
        await message.answer("Скачалось, отправляю...")
        with open(f'audio/{yt.title}.mp3', 'rb') as audio:
            await bot.send_audio(message.chat.id, audio, reply_markup=inline_keyboard)
        os.remove(f'audio/{yt.title}.mp3')
    except:
        yt.streams.filter(only_audio=True).first().download('audio', f'{yt.author}.mp3')
        await message.answer("Скачалось, отправляю...")
        with open(f'audio/{yt.author}.mp3', 'rb') as audio:
            await bot.send_audio(message.chat.id, audio, reply_markup=inline_keyboard)
        os.remove(f'audio/{yt.author}.mp3')
    await state.finish()

@dp.message_handler(state=VideoState.url)
async def download_video(message:types.Message, state:FSMContext):
    yt = YouTube(message.text, use_oauth=True)
    await message.answer("Скачиваем видео...")
    try:
        yt.streams.filter(file_extension='mp4').first().download('video', f'{yt.title}.mp4')
        await message.answer("Скачалось, отправляю...")
        with open(f'video/{yt.title}.mp4', 'rb') as video:
            await bot.send_video(message.chat.id, video, reply_markup=inline_keyboard)
        os.remove(f'video/{yt.title}.mp4')
    except:
        yt.streams.filter(file_extension='mp4').first().download('video', f'{yt.author}.mp4')
        await message.answer("Скачалось, отправляю...")
        with open(f'video/{yt.author}.mp4', 'rb') as video:
            await bot.send_video(message.chat.id, video, reply_markup=inline_keyboard)
        os.remove(f'video/{yt.author}.mp4')
    await state.finish()
    await state.update_data(to_email=message.text)
    await EmailState.subject.set()

@dp.message_handler(state=EmailState.message)
async def send_message(message:types.Message, state:FSMContext):
    await state.update_data(message=message.text)
    await message.answer('Отправляем почту...')
    res = await storage.get_data(user=message.from_user.id)
    sender = os.environ.get('smtp_email')
    password = os.environ.get('smtp_email_password')

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    msg = EmailMessage()
    msg.set_content(res['message'])

    msg['Subject'] = res['subject']
    msg['From'] = os.environ.get('smtp_email')
    msg['To'] = res['to_email']

    try:
        server.login(sender, password)
        server.send_message(msg)
        await message.answer('Успешно отправлено!')
    except Exception as error:
        await message.answer(f'Произошла ошибка попробуйте позже\n{error}')
        await state.finish()

executor.start_polling(dp)