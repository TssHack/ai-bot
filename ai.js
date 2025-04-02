const express = require("express");
const { Telegraf, Markup } = require("telegraf");
const axios = require("axios");
const bodyParser = require("body-parser");

const app = express();

// مقادیر API خود را اینجا وارد کنید
const botToken = "7000850548:AAEZ1JJfZ6QhNwe8Z9qsrGzd9hHZBp_iIno";
const adminId = 6856915102;

const bot = new Telegraf(botToken);

// Middleware برای پردازش داده‌های JSON
app.use(bodyParser.json());

// تابع ارسال درخواست به API هوش مصنوعی
async function chatWithAI(query, userId) {
  try {
    const url = "https://api.binjie.fun/api/generateStream";
    const headers = {
      "authority": "api.binjie.fun",
      "accept": "application/json, text/plain, */*",
      "accept-language": "en-US,en;q=0.9",
      "origin": "https://chat18.aichatos.xyz",
      "referer": "https://chat18.aichatos.xyz/",
      "user-agent": "Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
      "Content-Type": "application/json"
    };

    const data = {
      prompt: query,
      userId: String(userId),
      network: true,
      system: "",
      withoutContext: false,
      stream: false
    };

    const response = await axios.post(url, data, { headers });
    return response.data || "متاسفم، پاسخ مناسبی دریافت نشد.";
  } catch (error) {
    console.error("❌ خطا در ارتباط با API:", error);
    return "❌ خطایی رخ داد، لطفاً مجدداً تلاش کنید.";
  }
}

// رویداد /start
bot.start(async (ctx) => {
  const user = ctx.from;
  const startText = `🤖 **به ربات هوش مصنوعی خوش آمدید!**\n\n`
    + `📌 **نحوه استفاده:**\n`
    + `1️⃣ پیام خود را ارسال کنید.\n`
    + `2️⃣ ربات پاسخ شما را می‌دهد.\n`
    + `🚀 **برای شروع، پیام خود را ارسال کنید!**`;

  await ctx.reply(startText, {
    parse_mode: "Markdown",
    ...Markup.inlineKeyboard([
      Markup.button.url("✍️ نویسنده: احسان فضلی", "https://t.me/abj0o"),
    ])
  });

  // ارسال پیام به ادمین
  const adminMessage = `🚀 **یک کاربر جدید ربات را استارت کرد!**\n\n`
    + `👤 نام: ${user.first_name}\n`
    + `🆔 آیدی: \`${user.id}\``;

  if (adminId) {
    try {
      await bot.telegram.sendMessage(adminId, adminMessage, { parse_mode: "Markdown" });
    } catch (error) {
      console.error("⚠️ خطا در ارسال پیام به ادمین:", error);
    }
  }
});

// هندل پیام‌های ورودی
bot.on("text", async (ctx) => {
  const userMessage = ctx.message.text;
  const userId = ctx.from.id;
  const chatId = ctx.chat.id;

  try {
    await ctx.sendChatAction("typing");
    const responseText = await chatWithAI(userMessage, userId);

    await ctx.reply(responseText, {
      ...Markup.inlineKeyboard([
        Markup.button.callback("🥰", "love"),
      ])
    });
  } catch (error) {
    console.error("خطا در پردازش پیام:", error);
  }
});

// پاسخ به کلیک روی دکمه 🥰
bot.action("love", async (ctx) => {
  await ctx.answerCbQuery("❤️ ممنون از من استفاده می‌کنید، امیدوارم کمک‌رسان خوبی باشم!", { show_alert: true });
});

// Webhook handler
app.post(`/webhook/${botToken}`, async (req, res) => {
  const update = req.body;
  try {
    await bot.handleUpdate(update);
    res.sendStatus(200);
  } catch (error) {
    console.error("خطا در پردازش Webhook:", error);
    res.sendStatus(500);
  }
});

// پیکربندی Webhook
bot.telegram.setWebhook(`https://<your-vercel-url>/api/bot/webhook/${botToken}`);

// اجرای سرور
app.listen(3000, () => {
  console.log("✅ ربات در حال اجرا است...");
});
