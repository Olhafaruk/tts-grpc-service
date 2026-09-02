# 🗣️ TTS gRPC Service

[![CI Status](https://github.com/Olhafaruk/tts-grpc-service/actions/workflows/test.yml/badge.svg)](https://github.com/Olhafaruk/tts-grpc-service/actions/workflows/test.yml)

A text-to-speech service built with DDD architecture. gRPC. tests. and Docker infrastructure.

---

## 📦 Installation

```bash
git clone https://github.com/Olhafaruk/tts-grpc-service.git
cd tts-grpc-service
pip install -r requirements.txt
```

---

## 🐳 Running the Server

```bash
docker-compose up --build
```

📍 The gRPC server starts at `localhost:50051`

---

## 🎧 Client

```bash
python -m tts_grpc_service.client.test_grpc

```

🔊 Saves an audio file `out.mp3` for the text `"Приветствую, Halli Hallo, gRPC!"`

---

## 🧪 Tests

### ✅ Unit Tests

```bash
pytest tests/domain tests/services tests/repository
```

### 🔗 Integration Tests (if the server is running)

```bash
pytest tests/integration
```

📎 The entire gRPC flow is tested: client → server → provider → response

---

## 🧹 Linting and Formatting

The project uses [`pre-commit`](https://pre-commit.com) for automatic code quality checks. Included tools:

- [`black`](https://github.com/psf/black) — Python code auto-formatter 
- [`isort`](https://github.com/PyCQA/isort) — import sorting 
- [`flake8`](https://github.com/PyCQA/flake8) — style and error checking 

### 🚀 Running Linters via Docker

```bash
# Build the linter image (if Dockerfile changed)
docker compose -f docker-compose.lint.yaml build lint

# Or pull the ready-made image
docker compose -f docker-compose.lint.yaml pull lint

# Run linters on all files
docker compose -f docker-compose.lint.yaml run --rm lint
```

📌 By default, the following command runs:
```bash
pre-commit run --all-files --show-diff-on-failure
```

---


## ⚙️ Makefile Commands

| Command       | Description                       |
|---------------|-----------------------------------|
| `make test`   | Run all unit tests                |
| `make client` | Send a request and save `out.mp3` |
| `make server` | Start the server in Docker        |
| `make clean`  | Remove temporary files and caches |

---

## 🧠 Example Request

```text
SynthesisRequest(text="Hello, Bonjour, Привет")
```

🔁 Response: `audio` bytes → saved as mp3

---

## 🧰 Technologies

- 🐍 Python 3.11
- ⚡ gRPC / protobuf
- 🔊 gTTS (Google Text-to-Speech)
- 🐳 Docker / docker-compose
- 🧪 pytest
- 🔄 GitHub Actions

---

## 📂 Project Structure

```
cmd/                       # Application entry point
src/tts_grpc_service/      # Service source code
├── client/                # gRPC client
├── domain/                # Domain models and logic
├── grpc/                  # Generated gRPC files
├── repository/            # Providers and external API handling
├── services/              # Business logic
├── grpc_server.py         # gRPC server startup
tests/                     # Tests
├── domain/                # Domain logic tests
├── repository/            # Repository tests
├── services/              # Sevice tests
└── integration/           # Integration tests


---

## 🛠 CI/CD

GitHub Actions run on every push:
✅ Automatic unit test execution
🧪 Integration tests are executed locally (server required)

---

## 👩‍💻 Author

Developed by Olha Faruk  
📌 Project implemented according to a technical specification
✨ Automation, tests, structure, and client verification added




