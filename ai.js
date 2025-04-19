const express = require("express");
const { Telegraf, Markup } = require("telegraf");
const axios = require("axios");
const bodyParser = require("body-parser");

const app = express();
app.use(bodyParser.json());

// مقادیر خود را جایگزین کنید
const botToken = "7000850548:AAH5oF7R6AYdDp5RJCaPiK2-bx5EwygoaG4";
const adminId = 6856915102;

const bot = new Telegraf(botToken);

// Webhook endpoint
app.use(bot.webhookCallback("/bot"));

// تنظیم وبهوک (تنها در اولین اجرای deploy روی Vercel یا به‌صورت دستی با curl)
bot.telegram.setWebhook("https://ai-bot-ehsan.vercel.app/bot");

// تابع تماس با API هوش مصنوعی
async function chatWithAI(query, userId) {
  try {
    const url = "https://api.binjie.fun/api/generateStream";
    const headers = {
      "authority": "api.binjie.fun",
      "accept": "application/json, text/plain, */*",
      "accept-language": "en-US,en;q=0.9",
      "origin": "https://chat18.aichatos.xyz",
      "referer": "https://chat18.aichatos.xyz/",
      "user-agent": "Mozilla/5.0",
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

// /start command
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

// هندل پیام‌ها
bot.on("text", async (ctx) => {
  const userMessage = ctx.message.text;
  const userId = ctx.from.id;

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

// پاسخ به دکمه
bot.action("love", async (ctx) => {
  await ctx.answerCbQuery("❤️ ممنون از من استفاده می‌کنید، امیدوارم کمک‌رسان خوبی باشم!", { show_alert: true });
});

module.exports = app;
