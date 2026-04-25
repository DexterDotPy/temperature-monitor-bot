# Telegram Bot for Temperature Monitoring

Бот для мониторинга температуры в серверной. Отправляет уведомление при превышении порога или резком изменении.

## Команды
- /start — подписаться на уведомления
- /stop — отписаться
- /temp — получить текущую температуру
- /history — показать последние 5 значений

## Установка и запуск

1. Клонировать репозиторий:
   git clone https://github.com/DexterDotPy/temperature-monitor-bot.git
   cd temperature-monitor-bot

2. Установить зависимости:
   pip install -r requirements.txt

3. Создать файл .env и добавить токен бота:
   BOT_TOKEN=ваш_токен_от_BotFather

4. Запустить бота:
   python bot_telegramm.py