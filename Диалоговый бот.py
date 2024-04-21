import logging
from telegram.ext import Application, MessageHandler, CommandHandler, ConversationHandler, filters
from config import BOT_TOKEN

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


async def start(update, context):
    await update.message.reply_text(
        "Привет. Пройдите небольшой опрос, пожалуйста!\n"
        "Вы можете прервать опрос, послав команду /stop.\n"
        "В каком городе Вы живёте?\n"
        "Вы можете пропустить вопрос с помощью команды /skip")
    return 1


async def first_response(update, context):
    locality = update.message.text
    await update.message.reply_text(f"Какая погода в городе {locality}?")
    return 2


async def second_response(update, context):
    weather = update.message.text
    logger.info(weather)
    await update.message.reply_text("Спасибо за участие в опросе! Всего доброго!")
    return ConversationHandler.END


async def skip(update, context):
    await update.message.reply_text('Какая погода у Вас за окном?')
    return 2


async def stop(update, context):
    await update.message.reply_text("Всего доброго!")
    return ConversationHandler.END


application = Application.builder().token(BOT_TOKEN).build()
conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        1: [MessageHandler(filters.TEXT & ~filters.COMMAND, first_response)],
        2: [MessageHandler(filters.TEXT & ~filters.COMMAND, second_response)]
     },
    fallbacks=[CommandHandler('stop', stop), CommandHandler('skip', skip)]
)
application.add_handler(conv_handler)
application.run_polling()