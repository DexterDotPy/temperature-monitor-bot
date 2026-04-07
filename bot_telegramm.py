#!/usr/bin/env python3

import serial
import telebot
from config import bot
from datetime import datetime

# Настройки
port = "/dev/ttyACM0"
baudrate = 115200

keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
button_check = telebot.types.KeyboardButton('/start')
button_subscrib = telebot.types.KeyboardButton('/subscrib')
keyboard.add(button_check, button_subscrib)
            
# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_temp(message):
    try:
        # Опрос датчика
        ser = serial.Serial(port, baudrate, timeout=1)
        ser.write(b"~G")
        data = ser.readline().decode().strip()
        
        if data.startswith('~G'):
            subscribe = check_subscribe(message.chat.id)
            temp = float(data[2:])
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
            if temp>25.0:
                emoji = "\U0001F525"
            else:
                emoji = "\u2744\uFE0F"   
                
            response = f"Датчик работает!\n{current_time}\n{emoji} {temp}°C {emoji}\n{subscribe} Подписка {subscribe}"
            bot.send_message(message.chat.id, response, reply_markup=keyboard)  
            
        else:
            bot.send_message(message.chat.id, f"Ошибка: получен неверный ответ - {data}", reply_markup=keyboard) 
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}", reply_markup=keyboard)
       
# Обработчик текстовых сообщений
@bot.message_handler(commands=['subscrib'])
def subscrib(message):
    result = toggle_info_in_file(message.chat.id)
    bot.send_message(message.chat.id,result,reply_markup=keyboard)
       
# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def echo_handler(message):
    bot.send_message(message.chat.id, message.text)

def toggle_info_in_file(info_to_toggle):
    try:
        filename = '/root/temp/subscribers.txt'
        # Преобразуем info_to_toggle в строку для сравнения
        info_str = str(info_to_toggle)
        
        # Читаем весь файл
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Проверяем наличие информации (теперь обе стороны - строки)
        if info_str in content:
            # Удаляем информацию
            new_content = content.replace(info_str, '')
            # Очищаем от лишних переносов строк
            new_content = '\n'.join([line for line in new_content.split('\n') if line.strip()])
            action = "Подписка удалена"
        else:
            # Добавляем информацию с переносом строки
            new_content = content + ('\n' if content else '') + info_str
            action = "Подписка оформлена"
        
        # Записываем обратно
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(new_content)
        
        return action
        
    except FileNotFoundError:
        # Если файла нет - создаем и записываем информацию
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(str(info_to_toggle))
        return "Подписка оформлена (файл создан)"

def check_subscribe(info_to_toggle):
    filename = '/root/temp/subscribers.txt'
    info_str = str(info_to_toggle)
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
    if info_str in content:
        subscribe = "\u2705"
    else:
        subscribe = "\u274C"
    return subscribe    


# Запускаем бота
if __name__ == '__main__':
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
    
