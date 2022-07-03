from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import re
import pandas as pd
import os
import os
from dotenv import load_dotenv

load_dotenv()

PRE_LINK = os.environ.get('LINK', "default_value")
TOKEN = os.environ.get('TOKEN', "default_value")

def start(update, context):
    update.message.reply_text("Assalamu alaykum jo'rajon")

def help(update, context):
    update.message.reply_text('''
    Quyidagi buyruqlar mavjud:

    /start -> Salomlashuv
    /help -> Shu xabar
    /link -> fayldagi linkni o'zgartirib beradi
    ''')

def send_document(update, context):
    chat_id = update.message.chat_id
    document = open('items.csv', 'rb')
    context.bot.send_document(chat_id, document)

def downloader(update, context):
    # writing to a custom file
    with open("items.csv", 'wb') as f:
        context.bot.get_file(update.message.document).download(out=f)

    try:
        df = pd.read_csv('items.csv', sep=';')

        for index, row in df.iterrows():
            try:
                link = row['preview_link']
                file_id = re.search('d/(.*)/view?', link).group(1)
                
                df.iloc[index, 4] = PRE_LINK + file_id
            except Exception as ins:
                pass

    except Exception as inst:
        print("wrong")    # the exception instance
    finally:
        df.to_csv("items.csv", sep=';')  
        send_document(update, context)


updater = Updater(TOKEN, use_context=True)
disp = updater.dispatcher

disp.add_handler(MessageHandler(Filters.document, downloader))
disp.add_handler(CommandHandler("start", start))
disp.add_handler(CommandHandler("help", help))

updater.start_polling()
updater.idle()
