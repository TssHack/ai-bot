import asyncio
import aiohttp
from telethon import TelegramClient, events, Button
from telethon.tl.types import InputBotInlineResult, InputWebDocument

# مقادیر API خود را اینجا وارد کنید
api_id = '18377832'
api_hash = 'ed8556c450c6d0fd68912423325dd09c'
bot_token = '7000850548:AAEZ1JJfZ6QhNwe8Z9qsrGzd9hHZBp_iIno'

# ایجاد نمونه ربات
client = TelegramClient('bot_session', api_id, api_hash).start(bot_token=bot_token)


async def fetch_api(url, json_data, headers):
    """ارسال درخواست به API هوش مصنوعی"""
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=json_data, headers=headers) as response:
            # دریافت محتوای پاسخ به صورت متنی
            text_response = await response.text()
            return text_response


async def chat_with_ai(query, user_id):
    """ارسال پیام کاربر به API و دریافت پاسخ"""
    url = "https://api.binjie.fun/api/generateStream"
    headers = {
        "authority": "api.binjie.fun",
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "origin": "https://chat18.aichatos.xyz",
        "referer": "https://chat18.aichatos.xyz/",
        "user-agent": "Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
        "Content-Type": "application/json"
    }
    data = {
        "prompt": query,
        "userId": str(user_id),
        "network": True,
        "system": "",
        "withoutContext": False,
        "stream": False
    }
    response_text = await fetch_api(url, json_data=data, headers=headers)
    return response_text if response_text else "متاسفم، پاسخ مناسبی دریافت نشد."


@client.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    """ارسال پیام راهنما هنگام استارت ربات"""
    start_text = (
        "🤖 **به ربات هوش مصنوعی خوش آمدید!**\n\n"
        "📌 **نحوه استفاده:**\n"
        "1️⃣ پیام خود را ارسال کنید.\n"
        "2️⃣ ربات پاسخ شما را می‌دهد.\n"
        "🚀 **برای شروع، پیام خود را ارسال کنید!**"
    )

    # ارسال پیام با دکمه اینلاین
    await event.reply(
        start_text,
        buttons=[Button.url("✍️ نویسنده: احسان فضلی", "https://t.me/abj0o")],
        link_preview=False
    )


@client.on(events.NewMessage)
async def handler(event):
    """دریافت پیام کاربر و پردازش آن"""
    user_message = event.message.message
    user_id = event.sender_id

    # ارسال واکنش به پیام کاربر با ایموجی 👍
    try:
        async with client.action(chat_id, "typing"):
    # دریافت پاسخ از API هوش مصنوعی
        response_text = await chat_with_ai(user_message, user_id)

    # ارسال پاسخ به عنوان ریپلای همراه با دکمه اینلاین 🥰
        await event.reply(
            response_text,
            buttons=[Button.inline("🥰", b"love")]
        )


@client.on(events.CallbackQuery(data=b"love"))
async def love_callback(event):
    """پاسخ به کلیک روی دکمه 🥰"""
    await event.answer("❤️ ممنون از من استفاده می کنید امید وار کمک رسان خوبی به شما باشم !", alert=True)


# شروع ربات
client.start()
print("ربات فعال است...")
client.run_until_disconnected()
