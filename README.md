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
python -m tts_grpc_service.client.test_grpc

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

## 🧹 Линтинг и форматирование

Проект использует [`pre-commit`](https://pre-commit.com) для автоматической проверки качества кода. Включены следующие инструменты:

- [`black`](https://github.com/psf/black) — автоформатирование Python-кода  
- [`isort`](https://github.com/PyCQA/isort) — сортировка импортов  
- [`flake8`](https://github.com/PyCQA/flake8) — проверка стиля и ошибок  

### 🚀 Запуск линтеров через Docker

```bash
# Собрать образ линтера (если менялся Dockerfile)
docker compose -f docker-compose.lint.yaml build lint

# Или подтянуть готовый образ
docker compose -f docker-compose.lint.yaml pull lint

# Прогнать линтеры по всем файлам
docker compose -f docker-compose.lint.yaml run --rm lint
```

📌 По умолчанию запускается:
```bash
pre-commit run --all-files --show-diff-on-failure
```

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
cmd/                       # Точка входа приложения
src/tts_grpc_service/      # Исходный код сервиса
├── client/                # gRPC-клиент
├── domain/                # Модели и доменная логика
├── grpc/                  # gRPC сгенерированные файлы
├── repository/            # Провайдеры и работа с внешними API
├── services/              # Бизнес-логика
├── grpc_server.py         # Запуск gRPC сервера
tests/                     # Тесты
├── domain/                # Тесты доменной логики
├── repository/            # Тесты репозиториев
├── services/              # Тесты сервисов
└── integration/           # Интеграционные тесты


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




