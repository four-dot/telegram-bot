import asyncio
import yt_dlp
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Send me a public video URL.")

@dp.message()
async def download(message: types.Message):
    url = message.text
    
    if not url.startswith("http"):
        await message.answer("Please send a valid URL.")
        return

    await message.answer("Downloading...")

    ydl_opts = {
        'outtmpl': '%(title)s.%(ext)s',
        'format': 'best',
        'quiet': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        video = FSInputFile(filename)
        await message.answer_video(video)

        os.remove(filename)

    except Exception as e:
        await message.answer(f"Error: {str(e)}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())