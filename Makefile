# Makefile — удобные команды для проекта

.PHONY: test client server clean

test:
    @echo " Запускаем pytest"
    pytest tests/

client:
    @echo " Запуск gRPC-клиента"
    python -m client.test_grpc

server:
    @echo " Запуск gRPC-сервера через Docker"
    docker-compose up -d

clean:
    @echo " Очистка временных файлов"
    find . -name '__pycache__' -type d -exec rm -r {} +
    find . -name '*.pyc' -delete

.PHONY: lint
lint:
    docker run --rm \
      -v "$(PWD)":/app \
      -w /app \
      python:3.11-slim \
      sh -c "\
        pip install pre-commit black isort flake8 && \
        pre-commit run --all-files"
