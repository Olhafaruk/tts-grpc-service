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
