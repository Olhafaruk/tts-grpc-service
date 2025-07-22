# 🗣️ TTS gRPC Service

[![CI Status](https://github.com/Olhafaruk/tts-grpc-service/actions/workflows/test.yml/badge.svg)](https://github.com/Olhafaruk/tts-grpc-service/actions/workflows/test.yml)

Сервис синтеза речи с архитектурой DDD, gRPC, тестами и Docker-инфраструктурой.

---

## 📦 Установка

```bash
git clone https://github.com/Olhafaruk/tts-grpc-service.git
cd tts-grpc-service
pip install -r requirements.txt
```

---

## 🐳 Запуск сервера

```bash
docker-compose up --build
```

📍 gRPC-сервер стартует на `localhost:50051`

---

## 🎧 Клиент

```bash
python -m client.test_grpc
```

🔊 Сохранит аудиофайл `out.mp3` по тексту `"Приветствую, Halli Hallo, gRPC!"`

---

## 🧪 Тесты

### ✅ Модульные

```bash
pytest tests/domain tests/services tests/repository
```

### 🔗 Интеграционные (если сервер работает)

```bash
pytest tests/integration
```

📎 Проверяется весь gRPC-поток: клиент → сервер → провайдер → ответ

---

## ⚙️ Makefile команды

| Команда       | Описание                               |
|---------------|------------------------------------------|
| `make test`   | Запустить все модульные тесты            |
| `make client` | Отправить запрос и сохранить `out.mp3`   |
| `make server` | Поднять сервер в Docker                  |
| `make clean`  | Удалить временные файлы и кеши           |

---

## 🧠 Пример запроса

```text
SynthesisRequest(text="Hello, Bonjour, Привет")
```

🔁 Ответ: `audio` в байтах → сохраняется как mp3

---

## 🧰 Технологии

- 🐍 Python 3.11
- ⚡ gRPC / protobuf
- 🔊 gTTS (Google Text-to-Speech)
- 🐳 Docker / docker-compose
- 🧪 pytest
- 🔄 GitHub Actions

---

## 📂 Структура проекта

```
client/          # gRPC-клиент
domain/          # Модели запроса и ответа
repository/      # GTTS-провайдер
services/        # Бизнес-логика TTS
server/          # gRPC-сервер и protobuf-стабы
tests/           # Юнит- и интеграционные тесты
```

---

## 🛠 CI/CD

При каждом push запускается GitHub Actions:  
✅ Автоматическая проверка модульных тестов  
🧪 Интеграционные тесты выполняются локально (сервер необходим)

---

## 👩‍💻 Автор

Разработка: **Olha Faruk**  
📌 Проект выполнен по техническому заданию  
✨ Добавлена автоматизация, тесты, структура и клиентская проверка




