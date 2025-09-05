# 🐼 x-pandas-chatbot  
CI Status

Сервис интеллектуальной работы с таблицами на базе FastAPI, Pandas и OpenAI. 
Архитектура построена по принципам DDD, с тестами, Docker-инфраструктурой и поддержкой HTTP/gRPC-интерфейсов.

---

## 📦 Установка

```bash
git clone https://github.com/Olhafaruk/tts-grpc-service/tree/main/x-pandas-chatbot.git
cd x-pandas-chatbot
pip install -r requirements.txt
```

Создай `.env` файл:

```env

OPENAI_API_KEY=your key
OPENAI_API_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_TEMPERATURE=0.7
OPENAI_MAX_TOKENS=1024

WEAVIATE_URL=http://weaviate:8080
SANDBOX_IMAGE=python:3.10-slim
SANDBOX_MEMORY_LIMIT=512m
SANDBOX_CPU_LIMIT=0.5
LOG_LEVEL=INFO

DEBUG_ENV=loaded
```

---

## 🐳 Запуск сервера

```bash
docker-compose up --build
```

📍 HTTP-сервер стартует на `localhost:8000`  
📍 Swagger UI доступен по адресу: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 💬 Примеры запросов к функциям

| 🔧 Функция               | 📄 Описание действия                                      | 🧾 Аргументы (ключи)                                                                 | 🧪 Пример запроса JSON |
|-------------------------|-----------------------------------------------------------|--------------------------------------------------------------------------------------|------------------------|
| `merge_tables`          | Объединяет две таблицы по колонке                         | `table1_id`, `table2_id`, `on`, `how`                                               | `{ "function": "merge_tables", "arguments": { "table1_id": "...", "table2_id": "...", "on": ["Currency"], "how": "inner" } }` |
| `rename_column`         | Переименовывает колонку                                   | `table_id`, `old_name`, `new_name`                                                  | `{ "function": "rename_column", "arguments": { "table_id": "...", "old_name": "Rate", "new_name": "Exchange Rate" } }` |
| `filter_rows`           | Фильтрует строки по значению в колонке                    | `table_id`, `column`, `value`, `n_rows` (опц.)                                      | `{ "function": "filter_rows", "arguments": { "table_id": "...", "column": "Country", "value": "Japan", "n_rows": 5 } }` |
| `convert_currency`      | Конвертирует валюту по курсу на указанную дату            | `table_id`, `currency`, `amount`, `date`                                            | `{ "function": "convert_currency", "arguments": { "table_id": "...", "currency": "EUR", "amount": 100, "date": "2025-01-01" } }` |
| `scale_column_by_rate`  | Умножает значения колонки на коэффициент                  | `table_id`, `column`, `exchange_rate`                                               | `{ "function": "scale_column_by_rate", "arguments": { "table_id": "...", "column": "Rate to USD", "exchange_rate": 1.2 } }` |
| `aggregate_column`      | Агрегирует значения по колонке (с группировкой или без)   | `table_id`, `column`, `agg`, `group_by` (опц.)                                      | `{ "function": "aggregate_column", "arguments": { "table_id": "...", "column": "Rate to USD", "agg": "mean", "group_by": "Country" } }` |
| `compare_rows`          | Сравнивает курсы двух валют на одну дату                  | `table_id`, `currency1`, `currency2`, `date`                                        | `{ "function": "compare_rows", "arguments": { "table_id": "...", "currency1": "EUR", "currency2": "GBP", "date": "2025-01-01" } }` |
| `show_table`            | Показывает первые строки таблицы                          | `table_id`, `n_rows` (опц.)                                                          | `{ "function": "show_table", "arguments": { "table_id": "...", "n_rows": 5 } }` |
| `get_column_stats`      | Выводит статистику по колонке                             | `table_id`, `column`                                                                 | `{ "function": "get_column_stats", "arguments": { "table_id": "...", "column": "Rate to USD" } }` |
| `list_columns`          | Возвращает список колонок таблицы                         | `table_id`                                                                           | `{ "function": "list_columns", "arguments": { "table_id": "..." } }` |

---

📌 Все запросы отправляются на эндпоинт:

```
POST /execute
Content-Type: application/json
```

## 🧠 Архитектура и интеллект

Проект использует несколько ключевых компонентов:

- **LLM (Large Language Model)** — OpenAI GPT-3.5-turbo интерпретирует пользовательские запросы и автоматически выбирает подходящую функцию.
- **Weaviate** — векторная база данных для поиска релевантных таблиц по смыслу запроса.
- **RAG (Retrieval-Augmented Generation)** — связка Weaviate + LLM: сначала извлекаются таблицы, затем LLM генерирует ответ на основе их содержимого.

📌 Это делает сервис полноценным ассистентом по данным, а не просто API.

---

## 🧪 Тесты

✅ Модульные  
```bash
pytest
docker-compose exec pandas-http pytest
docker-compose exec pandas-grpc pytest
```

📎 Покрываются все ключевые функции: загрузка, фильтрация, агрегация, переименование, объединение.

---

## 🧹 Линтинг и форматирование

Проект использует `pre-commit` для автоматической проверки качества кода. Включены:

- `black` — автоформатирование Python-кода  
- `isort` — сортировка импортов  
- `flake8` — проверка стиля и ошибок  

🚀 Запуск линтеров через Docker:

```bash
docker compose -f docker-compose.lint.yaml build lint
docker compose -f docker-compose.lint.yaml run --rm lint
```

📌 По умолчанию запускается:

```bash
pre-commit run --all-files --show-diff-on-failure
```

---



## 🧰 Технологии

🐍 Python 3.11  
⚡ FastAPI  
📊 Pandas  
🧠 OpenAI API  
🧬 Weaviate  
🔍 RAG (Retrieval-Augmented Generation)  
🐳 Docker / docker-compose  
🧪 pytest  
🔄 GitHub Actions  

---

## 📂 Структура проекта

```text
x-pandas-chatbot/
├── Dockerfile
├── docker-compose.yml
├── logs/
├── proto/
├── samples/
├── src/
│   ├── assistant/
│   │   ├── application/
│   │   │   ├── action_handlers.py
│   │   │   ├── execution_service.py
│   │   │   ├── function_registry.py
│   │   │   ├── index_service.py
│   │   │   ├── query_service.py
│   │   │   ├── shared_services.py
│   │   │   └── table_store.py
│   │   ├── domain/
│   │   │   ├── question.py
│   │   │   └── table.py
│   │   ├── infrastructure/
│   │   │   ├── openai_provider.py
│   │   │   ├── sandbox_executor.py
│   │   │   └── weaviate_client.py
│   │   ├── interface/
│   │   │   ├── grpc/
│   │   │   │   ├── assistant_pb2.py
│   │   │   │   ├── assistant_pb2_grpc.py
│   │   │   │   └── server.py
│   │   │   └── http/
│   │   │       ├── models.py
│   │   │       ├── openapi_config.py
│   │   │       └── server.py
│   │   └── main.py
├── tests/
│   ├── application/
│   ├── domain/
│   ├── infrastructure/
│   └── interface/
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
✨ Добавлена автоматизация, тесты, структура и интеллектуальная логика

---

