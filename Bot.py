import datetime

import redis
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from dotenv import load_dotenv
from os import getenv
from YouTubeInformationService import YouTubeInfo
import Keyboards
from ProjectExceptions import *
from UserService import UserService
from ADownloader import AudioDownloader

load_dotenv()
bot_token = getenv("BOT_TOKEN")
bot = Bot(bot_token)
dp = Dispatcher(bot)
yt_info = YouTubeInfo(getenv("YTKEY"))
user_service = UserService(redis.Redis(host=getenv("REDIS_HOST"), port=int(getenv("REDIS_PORT")) ,decode_responses=True))
audio_downloader = AudioDownloader()


@dp.message_handler(commands=["start"])
async def starts(message: types.Message):
    await bot.send_message(message.chat.id,
                           "Я могу загрузить для тебя видео или музыку с YouTube, выбери что ты хочешь",
                           reply_markup=Keyboards.select_mode_keyboard)


@dp.message_handler(commands=["music"])
async def start_download_music(message: types.Message):
    user_id = message.chat.id

    if not user_service.is_in_download(user_id):
        user_service.register_user(user_id, action="music")
        await bot.send_message(message.chat.id, "Можешь присылать ссылки, я их все скачаю",
                               reply_markup=Keyboards.start_download_keyboard)
    else:
        await bot.send_message(message.chat.id,
                               "Вы уже начинали запрашивать загрузку, завершите ее или продлжите присылать мне ссылки",
                               reply_markup=Keyboards.start_download_keyboard)


@dp.message_handler(commands=["add_playlist"])
async def add_user_playlist(message: types.Message):
    await bot.send_message(message.chat.id, "Присылай мне ссылку на плейлист и я его добавлю в твою очередь загрузки",
                           reply_markup=Keyboards.start_download_keyboard)


@dp.message_handler(commands=["send"])
async def start_download_video(message: types.Message):
    await bot.send_message(message.chat.id, "Загружаю видео (поока не работает)")


@dp.message_handler(commands=["delete_urls"])
async def delete_urls(message: types.Message):
    if not user_service.is_in_download(message.chat.id):
        await bot.send_message(message.chat.id,
                               "У вас еще нет ссылок на загрузку, выберите что хотите загрузить",
                               reply_markup=Keyboards.select_mode_keyboard)
    else:
        user_service.delete_user_urls(message.chat.id)
        await bot.send_message(message.chat.id,
                               "Можете заново выбрать что загружать",
                               reply_markup=Keyboards.select_mode_keyboard)


@dp.message_handler()
async def handle_all(message: types.Message):
    user_id = message.chat.id
    txt = message.text
    print(f"[{datetime.datetime.now()}]: user[{user_id}] send: {txt}")
    if txt.startswith("https://") and not txt.__contains__("playlist"):
        try:
            user_service.add_url_to_user(user_id, url=txt)
            await bot.send_message(user_id, "Хорошо, можете отправить еще ссылку, или  загрузить уже имеющиеся",
                                   reply_markup=Keyboards.start_download_keyboard)

        except UserNoneException:
            await bot.send_message(user_id, "Вы еще не выбрали что хотите загружать видео или музыку!")
        except UrlAlreadyExcepted:
            await bot.send_message(user_id, "Такая ссылка уже есть!",
                                   reply_markup=Keyboards.start_download_keyboard)

    elif txt.startswith("https://") and txt.__contains__("playlist"):
        try:
            playlist_urls = yt_info.get_playlist_ids(txt)
            user_service.add_user_playlist(user_id, playlist_urls)
        except UserNoneException:
            await bot.send_message(user_id, "Вы еще не выбрали что хотите загружать видео или музыку!",
                                   reply_markup=Keyboards.select_mode_keyboard)
        except:
            await bot.send_message(user_id, "Упс... Что-то навернулось!")
        else:
            await bot.send_message(user_id, "Ваш плейлист добавлен")


    elif txt == "Музыка":
        await start_download_music(message)
    elif txt == "Видео":
        await start_download_video(message)
    elif txt == "Завершить и загрузить":
        await download_user_urls(user_id)
    else:
        await bot.send_message(user_id, "Я не знаю что ты от меня хочешь")


async def download_user_urls(user_id):
    user = user_service.get_user(user_id)
    if len(user["url_list"]) < 1:
        await bot.send_message(user_id,
                               f"Нет ссылок для скачивания")
        return
    else:
        await bot.send_message(user_id, "Загружаю",
                               reply_markup=Keyboards.select_mode_keyboard)
    if user["action"] == "music":

        for url in user["url_list"]:
            try:
                audio = audio_downloader.download(url)
                await bot.send_audio(user_id,
                                     types.InputFile(audio, filename=f"{audio_downloader.audio.title}.mp3"))
            except TooBigFileException:
                await bot.send_message(user_id,
                                       f"Не могу загрузить файл [{audio_downloader.audio.title}] он слишком большой")

    user_service.delete_user_urls(user_id)


def start_routing():
    executor.start_polling(dp)
