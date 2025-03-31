import asyncio
import aiohttp
from telethon import TelegramClient, events
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
            return await response.json()


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
    response = await fetch_api(url, json_data=data, headers=headers)
    return response.get("text", "متاسفم، پاسخ مناسبی دریافت نشد.")


@client.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    """ارسال پیام راهنما هنگام استارت ربات"""
    start_text = (
        "🤖 **به ربات هوش مصنوعی خوش آمدید!**\n\n"
        "📌 **نحوه استفاده:**\n"
        "1️⃣ پیام خود را ارسال کنید.\n"
        "2️⃣ ربات پاسخ شما را می‌دهد.\n"
        "3️⃣ برای استفاده سریع، می‌توانید از اینلاین‌کوری هم استفاده کنید.\n\n"
        "✍️ **نویسنده:** [احسان فضلی](https://t.me/Ehsan_Fazli)\n"
        "🚀 **برای شروع، پیام خود را ارسال کنید!**"
    )
    await event.reply(start_text, link_preview=False)


@client.on(events.NewMessage)
async def handler(event):
    """دریافت پیام کاربر و پردازش آن"""
    user_message = event.message.message
    user_id = event.sender_id

    # واکنش به پیام کاربر با ایموجی 👍
    await event.message.react('👍')

    # دریافت پاسخ از API هوش مصنوعی
    response_text = await chat_with_ai(user_message, user_id)

    # ارسال پاسخ به عنوان ریپلای
    await event.reply(response_text)


@client.on(events.InlineQuery)
async def inline_query_handler(event):
    """پاسخ به اینلاین‌کوری‌ها"""
    query = event.text.strip()

    if not query:
        results = [
            InputBotInlineResult(
                id="1",
                type="article",
                title="🧠 هوش مصنوعی",
                description="یک پیام بفرستید تا پاسخ بگیرید!",
                thumb=InputWebDocument(
                    url="https://upload.wikimedia.org/wikipedia/commons/6/6f/Artificial_Intelligence_%26_AI_%26_Machine_Learning_-_30212411048.jpg",
                    size=1024,
                    mime_type="image/jpeg",
                    attributes=[]
                ),
                text="🤖 برای دریافت پاسخ، یک پیام ارسال کنید."
            )
        ]
    else:
        response_text = await chat_with_ai(query, event.sender_id)
        results = [
            InputBotInlineResult(
                id="2",
                type="article",
                title="📩 پاسخ دریافت شد!",
                description=response_text[:50] + "..." if len(response_text) > 50 else response_text,
                text=response_text
            )
        ]

    await event.answer(results, cache_time=0)


# شروع ربات
client.start()
print("ربات فعال است...")
client.run_until_disconnected()
