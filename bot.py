import asyncio
import random
import sqlite3
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests

TELEGRAM_TOKEN = "8360793640:AAFq5Zf4I6hiKaIndCjWcmDr8zUDbD9GIxw"
WEATHER_API = "9b53439a2715a6b9947c894646e85111"
ADMIN_ID = 8741323897
CHANNEL_LINK = "https://t.me/diiyor4"

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

conn = sqlite3.connect("users.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    referrer_id INTEGER,
    referral_count INTEGER DEFAULT 0
)
""")
conn.commit()

MOTIVATIONS = [
    "🌟 Har bir kun yangi imkoniyat!",
    "💪 Maqsadingga ishon, oldinga yur!",
    "🚀 Bugun qilgan harakat ertangi muvaffaqiyat!",
    "🎯 Hech qachon taslim bo'lma!",
    "⭐ Sen buni uddalay olasan!",
    "🔥 Katta orzular katta harakatlar talab qiladi!",
    "🏆 G'alaba qozonish uchun avval harakat qil!",
    "💡 Har qanday muammo yechimga ega!",
]

def main_menu():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📚 IELTS PREPARE", callback_data="ielts")],
        [InlineKeyboardButton(text="💰 EARN MONEY", callback_data="earn")],
        [InlineKeyboardButton(text="🚀 FUTURE", callback_data="future")],
        [InlineKeyboardButton(text="🌤 OB-HAVO", callback_data="weather")],
        [InlineKeyboardButton(text="🎯 MOTIVATSIYA", callback_data="motivation")],
        [InlineKeyboardButton(text="📝 FIKR QOLDIRISH", callback_data="feedback")],
    ])
    return keyboard

@dp.message(Command("start"))
async def start(message: types.Message):
    user_id = message.from_user.id
    args = message.text.split()
    
    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    user = cursor.fetchone()
    
    if not user:
        referrer_id = None
        if len(args) > 1 and args[1].startswith("ref_"):
            referrer_id = int(args[1].split("_")[1])
        cursor.execute("INSERT INTO users (user_id, referrer_id) VALUES (?, ?)", (user_id, referrer_id))
        conn.commit()
        
        if referrer_id:
            cursor.execute("UPDATE users SET referral_count = referral_count + 1 WHERE user_id=?", (referrer_id,))
            conn.commit()
            cursor.execute("SELECT referral_count FROM users WHERE user_id=?", (referrer_id,))
            count = cursor.fetchone()[0]
            if count >= 5:
                await bot.send_message(referrer_id, f"🎉 Tabrik! 5 ta do'st taklif qildingiz!\n\n🔐 Maxfiy kanal: {CHANNEL_LINK}")
            else:
                await bot.send_message(referrer_id, f"✅ Yangi do'st qo'shildi! {count}/5")

    await message.answer(
        "👋 Salom! Men Diyor AI man!\n\nQuyidagi bo'limlardan birini tanlang:",
        reply_markup=main_menu()
    )

@dp.callback_query(lambda c: c.data == "ielts")
async def ielts(callback: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌐 IELTS.org (Rasmiy)", url="https://www.ielts.org")],
        [InlineKeyboardButton(text="📖 British Council", url="https://www.britishcouncil.org/exam/ielts")],
        [InlineKeyboardButton(text="✏️ IELTS Liz", url="https://ieltsliz.com")],
        [InlineKeyboardButton(text="🎓 Magoosh IELTS", url="https://magoosh.com/ielts")],
        [InlineKeyboardButton(text="📝 IELTS Buddy", url="https://www.ielts-buddy.com")],
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back")]
    ])
    await callback.message.edit_text(
        "📚 IELTS tayyorgarlik uchun eng yaxshi 5 ta sayt:",
        reply_markup=keyboard
    )

@dp.callback_query(lambda c: c.data == "earn")
async def earn(callback: types.CallbackQuery):
    user_id = callback.from_user.id
 bot_username = (await bot.get_me()).username
    ref_link = f"https://t.me/{bot_username}?start=ref_{user_id}"
    cursor.execute("SELECT referral_count FROM users WHERE user_id=?", (user_id,))
    row = cursor.fetchone()
    count = row[0] if row else 0
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back")]
    ])
    await callback.message.edit_text(
        f"💰 EARN MONEY\n\n"
        f"Do'stlaringizni taklif qiling va maxfiy kanalga kiring!\n\n"
        f"📎 Sizning referral havolangiz:\n{ref_link}\n\n"
        f"✅ 5 ta do'st taklif qilsangiz — maxfiy kanal linki yuboriladi!\n\n"
        f"👥 Hozircha taklif qilganlar: {count}/5",
        reply_markup=keyboard
    )

@dp.callback_query(lambda c: c.data == "future")
async def future(callback: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📩 Murojaat", url="https://t.me/diiyor4")],
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back")]
    ])
    await callback.message.edit_text(
        "🚀 FUTURE\n\n"
        "Salom! Bu bot Diyor Raxmatov tomonidan yaratildi.\n\n"
        "Agar sizga ham shunday bot kerak bo'lsa murojaat qiling👇",
        reply_markup=keyboard
    )

@dp.callback_query(lambda c: c.data == "weather")
async def weather(callback: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back")]
    ])
    await callback.message.edit_text(
        "🌤 Shahar nomini yozing!\nMasalan: Toshkent",
        reply_markup=keyboard
    )

@dp.callback_query(lambda c: c.data == "motivation")
async def motivation(callback: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Yana bittasi", callback_data="motivation")],
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back")]
    ])
    await callback.message.edit_text(
        f"🎯 Kunlik motivatsiya:\n\n{random.choice(MOTIVATIONS)}",
        reply_markup=keyboard
    )

@dp.callback_query(lambda c: c.data == "feedback")
async def feedback(callback: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back")]
    ])
    await callback.message.edit_text(
        "📝 Fikringizni yozing!\nXabaringiz adminga yuboriladi.",
        reply_markup=keyboard
    )

@dp.message()
async def handle_message(message: types.Message):
    text = message.text
    url = f"http://api.openweathermap.org/data/2.5/weather?q={text}&appid={WEATHER_API}&units=metric&lang=ru"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        city = data["name"]
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        await message.answer(
            f"🌤 {city} ob-havosi:\n\n"
            f"🌡 Harorat: {temp}°C\n"
            f"💧 Namlik: {humidity}%\n"
            f"📋 Holat: {desc}",
            reply_markup=main_menu()
        )
    else:
        await bot.send_message(
            ADMIN_ID,
            f"📝 Yangi fikr:\n\nFoydalanuvchi: @{message.from_user.username}\n\nXabar: {text}"
        )
        await message.answer(
            "✅ Fikringiz adminga yuborildi! Rahmat!",
            reply_markup=main_menu()
        )

@dp.callback_query(lambda c: c.data == "back")
async def back(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "👋 Salom! Men Diyor AI man!\n\nQuyidagi bo'limlardan birini tanlang:",
        reply_markup=main_menu()
    )

async def main():
    await dp.start_polling(bot)

if name == "main":
    asyncio.run(main())
