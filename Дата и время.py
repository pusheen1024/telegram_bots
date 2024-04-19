from datetime import datetime
import logging
from telegram.ext import Application, MessageHandler, CommandHandler, filters
from config import BOT_TOKEN

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


async def start(update, context):
    user = update.effective_user
    await update.message.reply_html(
        rf"Здравствуйте, {user.mention_html()}! Я вежливый эхо-бот. Напишите мне что-нибудь, и я пришлю это назад!")


async def help_command(update, context):
    await update.message.reply_text("Я пока не умею помогать... Я только Ваше эхо.")


async def time_command(update, context):
    await update.message.reply_text(datetime.now().strftime("%X"))


async def date_command(update, context):
    await update.message.reply_text(datetime.now().strftime("%d-%m-%Y"))
    

async def echo(update, context):
    await update.message.reply_text(f'Я получил сообщение <{update.message.text}>')
    

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("time", time_command))
    application.add_handler(CommandHandler("date", date_command))    
    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, echo)
    application.add_handler(text_handler)
    application.run_polling()


if __name__ == '__main__':
    main()
