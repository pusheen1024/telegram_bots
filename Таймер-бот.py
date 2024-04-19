import logging
import pymorphy2
from telegram.ext import Application, MessageHandler, CommandHandler, filters
from config import BOT_TOKEN

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

user_settings = dict()
morph = pymorphy2.MorphAnalyzer()
word = morph.parse('секунда')[0]


def remove_job_if_exists(name, context):
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


async def set_timer(update, context):
    if len(context.args) != 1 or not context.args[0].isdigit():
        await update.effective_message.reply_text('Извините, не понимаю команду!')
        return
    TIMER = int(context.args[0])
    chat_id = update.effective_message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    context.job_queue.run_once(lambda context: task(update, context), TIMER, 
                               chat_id=chat_id, name=str(chat_id), data=TIMER)
    user_settings[update.effective_user] = TIMER
    new_word = word.inflect({"accs"}).make_agree_with_number(TIMER).word
    text = f'Вернусь через {TIMER} {new_word}!'
    if job_removed:
        text += ' Старая задача удалена.'
    await update.effective_message.reply_text(text)
    

async def unset(update, context):
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Таймер отменен!' if job_removed else 'У вас нет активных таймеров'
    await update.message.reply_text(text)
    

async def task(update, context):
    user = update.effective_user
    TIMER = user_settings[user]
    noun = word.make_agree_with_number(TIMER).word
    verb = 'прошла' if TIMER == 1 else 'прошли'
    await context.bot.send_message(context.job.chat_id, 
                                   text=f'КУКУ! {TIMER} {noun} {verb}!')
    
    
def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("set_timer", set_timer))
    application.add_handler(CommandHandler("unset", unset))    
    application.run_polling()


if __name__ == '__main__':
    main()