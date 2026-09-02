# 🐼 x-pandas-chatbot  
CI Status

An intelligent table-processing service built with FastAPI, Pandas, and OpenAI.
The architecture follows DDD principles, with tests, Docker infrastructure, and support for HTTP/gRPC interfaces.

---

## 📦 Installation

```bash
git clone https://github.com/Olhafaruk/tts-grpc-service/tree/main/x-pandas-chatbot.git
cd x-pandas-chatbot
pip install -r requirements.txt
```

Create a `.env` file:

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

## 🐳 Running the Server

```bash
docker-compose up --build
```

📍 HTTP server starts at `localhost:8000`  
📍 Swagger UI available at: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 💬 Function Call Examples

| 🔧 Function             | 📄 Description                                          | 🧾 Arguments (keys)                                | 🧪 Example JSON Request |
|-----------------|---------------------------------------------------------|----------------------------------------------------|-----|
| `merge_tables`  | Merges two tables by a column                 | `table1_id`, `table2_id`, `on`, `how`              | `{ "function": "merge_tables", "arguments": { "table1_id": "...", "table2_id": "...", "on": ["Currency"], "how": "inner" } }` |
| `rename_column` | Renames a column                               | `table_id`, `old_name`, `new_name`                 | `{ "function": "rename_column", "arguments": { "table_id": "...", "old_name": "Rate", "new_name": "Exchange Rate" } }` |
| `filter_rows`   | Filters rows by a column value               | `table_id`, `column`, `value`, `n_rows` (optional) | `{ "function": "filter_rows", "arguments": { "table_id": "...", "column": "Country", "value": "Japan", "n_rows": 5 } }` |
| `convert_currency` | Converts currency by rate on a given date       | `table_id`, `currency`, `amount`, `date`           | `{ "function": "convert_currency", "arguments": { "table_id": "...", "currency": "EUR", "amount": 100, "date": "2025-01-01" } }` |
| `scale_column_by_rate` | Multiplies column values by a coefficient              | `table_id`, `column`, `exchange_rate`              | `{ "function": "scale_column_by_rate", "arguments": { "table_id": "...", "column": "Rate to USD", "exchange_rate": 1.2 } }` |
| `aggregate_column` |  Aggregates values by column (with or without group)| `table_id`, `column`, `agg`, `group_by` (optional) | `{ "function": "aggregate_column", "arguments": { "table_id": "...", "column": "Rate to USD", "agg": "mean", "group_by": "Country" } }` |
| `compare_rows`  | Compares two currency rates on one date            | `table_id`, `currency1`, `currency2`, `date`       | `{ "function": "compare_rows", "arguments": { "table_id": "...", "currency1": "EUR", "currency2": "GBP", "date": "2025-01-01" } }` |
| `show_table`    |Displays first rows of a table                      | `table_id`, `n_rows` (optional)                    | `{ "function": "show_table", "arguments": { "table_id": "...", "n_rows": 5 } }` |
| `get_column_stats` | Outputs statistics for a column                          | `table_id`, `column`                               | `{ "function": "get_column_stats", "arguments": { "table_id": "...", "column": "Rate to USD" } }` |
| `list_columns`  | Returns list of table columns                     | `table_id`                                         | `{ "function": "list_columns", "arguments": { "table_id": "..." } }` |

---

📌  All requests go to the endpoint:

```
POST /execute
Content-Type: application/json
```

## 🧠 Architecture and Intelligence

The project uses several key components:

- **LLM (Large Language Model) — OpenAI GPT‑3.5‑turbo interprets user queries and automatically selects the right function.
- **Weaviate** — Weaviate — vector database for semantic table search.
- **RAG (Retrieval-Augmented Generation)** — Weaviate + LLM: first retrieves tables, then LLM generates answers based on their content.

📌 This makes the service a full data assistant, not just an API.

---

## 🧪 Tests

✅ Unit tests 
```bash
pytest
docker-compose exec pandas-http pytest
docker-compose exec pandas-grpc pytest
```

📎 Covers all key functions: loading, filtering, aggregation, renaming, merging.
---

## 🧹 Linting and Formatting

The project uses pre-commit for automatic code quality checks. Included:

- `black` — Python code auto‑formatter
- `isort` —  import sorting
- `flake8` — style and error checking 

🚀 Run linters via Docker:

```bash
docker compose -f docker-compose.lint.yaml build lint
docker compose -f docker-compose.lint.yaml run --rm lint
```

📌 By default:

```bash
pre-commit run --all-files --show-diff-on-failure
```

---



## 🧰 Technologies

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

## 📂 project Structure

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

GitHub Actions run on every push:
✅ Automatic unit test execution
🧪 Integration tests executed locally (server required)

---

## 👩‍💻 Author

Developed by **Olha Faruk**  
📌 Project implemented according to technical specification
✨ Added automation, tests, structure, and intelligent logic

---

