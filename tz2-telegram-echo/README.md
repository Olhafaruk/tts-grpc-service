# Telegram Echo User-Bot

Лёгкий Telegram-клиент, который эхо-отвечает на любые входящие сообщения от лица обычного пользователя. 
Построен с учётом принципов чистой архитектуры и полностью контейнеризован.

---

## Основные возможности

- Эхо-ответ: повторяет любой текст входящего сообщения  
- Работает как пользовательский бот (Telethon), обходя 2FA через заранее сгенерированный Session String  
- Структура по DDD/Clean Architecture: разделение на domain, repository, services, server  
- Запуск в один шаг через Docker Compose

---

## Быстрый старт

1. Клонировать репозиторий и перейти в папку проекта  
   ```bash
   git clone https://github.com/Olhafaruk/tts-grpc-service.git
   cd tts-grpc-service/tz2-telegram-echo
   ```

2. Скопировать пример env-файла и заполнить переменные  
   ```bash
   cp .env.example .env
   # В .env указать:
   # API_ID, API_HASH — из my.telegram.org
   #PHONE=+71234567890  
   #SESSION_NAME=echo 
   #Затем получить через `python generate_session.py  SESSION_STRING и вписать в .env
   #после чего PHONE и SESSION_NAME=echo можно удалить
   
   ```

3. Собрать и запустить контейнеры  
   ```bash
   docker-compose up --build
   ```

4. Отправить любое сообщение в чат с аккаунтом — бот-клиент тут же эхо-ответит.

---

## Структура проекта

```
.
├── domain/           # Сущности (Message, ChatSession и т.п.)
├── repository/       # Инициализация Telethon Client
├── services/         # Бизнес-логика эха
├── server/           # Обработчик событий NewMessage
├── generate_session.py  # Скрипт для создания SESSION_STRING
├── .env.example      # Пример переменных окружения
├── Dockerfile
└── docker-compose.yml
```

---

## Зависимости

- Python 3.11  
- telethon  
- docker, docker-compose  

---
## Автор Olha Faruk
