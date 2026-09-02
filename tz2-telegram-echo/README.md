# Telegram Echo User-Bot

A lightweight Telegram client that echoes any incoming messages as a regular user.
Built with Clean Architecture principles and fully containerized.

---

## Features

- Echo response: repeats any incoming message text
- Works as a user bot (Telethon), bypassing 2FA via a pre-generated Session String
- Structured with DDD/Clean Architecture: separated into domain, repository, services, server 
- One-step launch via Docker Compose

---

## Quick Start

1. Clone the repository and navigate to the project folder 
   ```bash
   git clone https://github.com/Olhafaruk/tts-grpc-service.git
   cd tts-grpc-service/tz2-telegram-echo
   ```

2. Copy the example env file and fill in the variables 
   ```bash
   cp .env.example .env
   # In .env specify:
   # API_ID, API_HASH — from my.telegram.org
   #PHONE=+71234567890  
   #SESSION_NAME=echo 
   # Then generate SESSION_STRING via `python generate_session.py` and paste it into .env
   # After that, PHONE and SESSION_NAME=echo can be removed
   
   ```

3. Build and start the containers
   ```bash
   docker-compose up --build
   ```

4. Send any message to the account — the bot client will immediately echo it back.

---

## Project Structure

```
.
├── domain/             # Entities (Message, ChatSession, etc.)
├── repository/         # Telethon Client initialization
├── services/           # Echo business logic
├── server/             # NewMessage event handler
├── generate_session.py # Script to create SESSION_STRING
├── .env.example        # Example environment variables
├── Dockerfile
└── docker-compose.yml

```

---

## Dependencies

- Python 3.11  
- telethon  
- docker, docker-compose  

---
## Author Olha Faruk
