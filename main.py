import telebot
import os
import logging


bot_token = YOUR_BOT_TOKEN
if not bot_token:
    logging.error("Bot token not provided. Make sure to set TELEGRAM_BOT_TOKEN environment variable.")
    exit()

bot = telebot.TeleBot(bot_token)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Я тебя не помню... Ты кто? Введи пароль: ')
    bot.register_next_step_handler(message, passdef)

def passdef(message):
    with open('FILE WITH PASSWORD', 'r') as passfile:
        passread = passfile.read().strip()
        try:
            if message.text == passread:
                bot.send_message(message.chat.id, 'Отлично! Сессия подтверждена. Добро пожаловать!')
                return
        except:
            pass
        bot.send_message(message.chat.id, 'Похоже что-то не сходится... Попробуй еще раз')
        bot.register_next_step_handler(message, passdef)

    bot.send_message(message.chat.id, 'Привет! Я могу напечатать твои PDF-файлы и изображения. Пришли мне файл, и я отправлю его на принтер.')

@bot.message_handler(content_types=['document'])
def print_file(message):
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open('file.pdf', 'wb') as new_file:
            new_file.write(downloaded_file)
        os.system('lp file.pdf')
        print('Получено изображение.Отправил на принтер...')
        bot.reply_to(message, 'Файл успешно отправлен на принтер!')
    except Exception as e:
        logging.error(f"Error printing file: {e}")
        bot.reply_to(message, 'Произошла ошибка при печати файла. Пожалуйста, попробуйте еще раз.')
        print('Произошла ошибка. Вообще хрен знает что случилось. Мб принтер выключен')

@bot.message_handler(content_types=['photo'])
def print_image(message):
    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open('file.jpg', 'wb') as new_file:
            new_file.write(downloaded_file)
        os.system('lp file.jpg')
        bot.reply_to(message, 'Изображение успешно отправлено на принтер!')
    except Exception as e:
        logging.error(f"Error printing image: {e}")
        bot.reply_to(message, 'Произошла ошибка при печати изображения. Пожалуйста, попробуйте еще раз.')
        print('Произошла ошибка. Вообще хрен знает что случилось. Мб принтер выключен')

@bot.message_handler(commands=['shtd'])
def shtd(message):
    bot.reply_to(message, 'Команда выключения отправлена!')
    os.system('sudo shutdown -h now')
    
@bot.message_handler(commands=['reboot'])
def shtd(message):
    bot.reply_to(message, 'Команда перезагрузки отправлена!')
    os.system('sudo shutdown -r now')

bot.polling()
