#!/usr/bin/python3

import serial
import telebot
from config import bot
from datetime import datetime

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

# Настройки
port = "/dev/ttyACM0"
baudrate = 115200

keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
button_check = telebot.types.KeyboardButton('/start')
button_subscrib = telebot.types.KeyboardButton('/subscrib')
keyboard.add(button_check, button_subscrib)

with open('/root/temp/subscribers.txt', 'r') as file:
    lines = file.readlines()

try:
    # Опрос датчика
    ser = serial.Serial(port, baudrate, timeout=1)
    ser.write(b"~G")
    data = ser.readline().decode().strip()
    
    if data.startswith('~G'):
        temp = float(data[2:])
        if temp>25.0:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
            for i in lines:
                subscribe = check_subscribe(i)
            
                response = f"Превышение температуры!\n{current_time}\n\U0001F525 {temp}°C \U0001F525\n{subscribe} Подписка {subscribe}"
            
                bot.send_message(i, response, reply_markup=keyboard)
               
        
    else:
        for i in lines:
            bot.send_message(i, f"Ошибка: получен неверный ответ - {data}", reply_markup=keyboard)  

except Exception as e:
    for i in lines:
        bot.send_message(i, f"Ошибка: {e}", reply_markup=keyboard)
    
    