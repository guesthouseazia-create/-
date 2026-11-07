import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📋 Прайс-лист и анализы", callback_data='price')],
        [InlineKeyboardButton("📍 Адрес и график работы", callback_data='info')],
        [InlineKeyboardButton("📞 Связаться с администратором", callback_data='contact')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = "Здравствуйте! Вас приветствует бот лаборатории.\nВыберите интересующий раздел:"
    
    if update.message:
        await update.message.reply_text(text, reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.message.reply_text(text, reply_markup=reply_markup)

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'price':
        await query.edit_message_text(
            "🩸 **Популярные анализы:**\n"
            "• Общий анализ крови (ОАК)\n"
            "• Биохимия крови\n"
            "• Анализ на сахар / Гликированный гемоглобин\n\n"
            "Для уточнения стоимости или записи напишите администратору.",
            parse_mode='Markdown'
        )
    elif query.data == 'info':
        await query.edit_message_text(
            "🏥 **Наш адрес и график:**\n"
            "⏰ Пн-Сб: с 08:00 до 17:00\n"
            "📍 г. Бухара\n"
            "Сбор анализов производится утром натощак."
        )
    elif query.data == 'contact':
        await query.edit_message_text(
            "📞 **Контакты:**\n"
            "Для записи и вопросов свяжитесь с нашим администратором по телефону или в Telegram."
        )

if __name__ == '__main__':
    # Токен подтягивается из защищенных настроек Render
    TOKEN = os.environ.get("BOT_TOKEN")

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(button_click))

    print("Бот успешно запущен на Render!")
    app.run_polling()
