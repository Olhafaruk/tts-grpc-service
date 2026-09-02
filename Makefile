# Makefile — удобные команды для проекта

.PHONY: test client server clean

test:
    @echo " Running pytest"
    pytest tests/

client:
    @echo " Running gRPC client"
    python -m client.test_grpc

server:
    @echo " Running gRPC server via Docker"
    docker-compose up -d

clean:
    @echo " Cleaning temporary files"
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
