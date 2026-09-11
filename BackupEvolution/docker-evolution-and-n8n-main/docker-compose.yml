version: '3.8'

services:
  # PostgreSQL Database
  postgres:
    image: postgres:16.4-alpine
    container_name: postgres
    restart: unless-stopped
    environment:
      # Credenciais do banco (altere se necessário)
      POSTGRES_USER: ${POSTGRES_USER:-postgres}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-postgres123}
      POSTGRES_DB: ${POSTGRES_DB:-n8n}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    networks:
      - app_network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis
  redis:
    image: redis:7.2-alpine
    container_name: redis
    restart: unless-stopped
    command: ["redis-server", "--appendonly", "yes", "--requirepass", "${REDIS_PASSWORD:-redis123}"]  # Senha do Redis (altere se necessário)
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"
    networks:
      - app_network
    healthcheck:
      test: ["CMD", "redis-cli", "-a", "${REDIS_PASSWORD:-redis123}", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  # n8n Main (recebe webhooks e gerencia workflows)
  n8n:
    image: n8nio/n8n:1.119.1
    container_name: n8n
    restart: unless-stopped
    environment:
      # Conexão com PostgreSQL (use as mesmas credenciais do postgres acima)
      - DB_TYPE=postgresdb
      - DB_POSTGRESDB_HOST=postgres
      - DB_POSTGRESDB_PORT=5432
      - DB_POSTGRESDB_DATABASE=${POSTGRES_DB:-n8n}
      - DB_POSTGRESDB_USER=${POSTGRES_USER:-postgres}
      - DB_POSTGRESDB_PASSWORD=${POSTGRES_PASSWORD:-postgres123}
      # Conexão com Redis (use a mesma senha do redis acima)
      - QUEUE_BULL_REDIS_HOST=redis
      - QUEUE_BULL_REDIS_PORT=6379
      - QUEUE_BULL_REDIS_PASSWORD=${REDIS_PASSWORD:-redis123}
      - EXECUTIONS_MODE=queue
      - N8N_HOST=${N8N_HOST:-host.docker.internal}
      - N8N_PORT=${N8N_PORT:-5678}
      - N8N_PROTOCOL=${N8N_PROTOCOL:-http}
      - WEBHOOK_URL=${N8N_WEBHOOK_URL:-http://host.docker.internal:5678/}
      - GENERIC_TIMEZONE=${N8N_TIMEZONE:-America/Sao_Paulo}
    ports:
      - "5678:5678"
    volumes:
      - n8n_data:/home/node/.n8n
    networks:
      - app_network
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy

  # n8n Worker (processa a fila de execuções)
  n8n-worker:
    image: n8nio/n8n:1.119.1
    container_name: n8n-worker
    restart: unless-stopped
    command: worker
    environment:
      - DB_TYPE=postgresdb
      - DB_POSTGRESDB_HOST=postgres
      - DB_POSTGRESDB_PORT=5432
      - DB_POSTGRESDB_DATABASE=${POSTGRES_DB:-n8n}
      - DB_POSTGRESDB_USER=${POSTGRES_USER:-postgres}
      - DB_POSTGRESDB_PASSWORD=${POSTGRES_PASSWORD:-postgres123}
      - QUEUE_BULL_REDIS_HOST=redis
      - QUEUE_BULL_REDIS_PORT=6379
      - QUEUE_BULL_REDIS_PASSWORD=${REDIS_PASSWORD:-redis123}
      - EXECUTIONS_MODE=queue
      - GENERIC_TIMEZONE=${N8N_TIMEZONE:-America/Sao_Paulo}
    volumes:
      - n8n_data:/home/node/.n8n
    networks:
      - app_network
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy

  # Evolution API
  evolution:
    image: evoapicloud/evolution-api:v2.3.6
    container_name: evolution_api
    restart: unless-stopped
    environment:
      - SERVER_TYPE=http
      - SERVER_PORT=${EVOLUTION_PORT:-8080}
      - SERVER_URL=${EVOLUTION_SERVER_URL:-}
      - LOG_LEVEL=${EVOLUTION_LOG_LEVEL:-ERROR,WARN,DEBUG,INFO}
      - LOG_COLOR=true
      - LOG_BAILEYS=error
      - CORS_ORIGIN=*
      - CORS_METHODS=GET,POST,PUT,DELETE
      - CORS_CREDENTIALS=true
      # Database (use as mesmas credenciais do postgres acima)
      - DATABASE_PROVIDER=postgresql
      - DATABASE_CONNECTION_URI=postgresql://${POSTGRES_USER:-postgres}:${POSTGRES_PASSWORD:-postgres123}@postgres:5432/${EVOLUTION_DB_NAME:-evolution}?schema=public
      - DATABASE_CONNECTION_CLIENT_NAME=evolution_api
      - DATABASE_SAVE_DATA_INSTANCE=true
      - DATABASE_SAVE_DATA_NEW_MESSAGE=true
      - DATABASE_SAVE_MESSAGE_UPDATE=true
      - DATABASE_SAVE_DATA_CONTACTS=true
      - DATABASE_SAVE_DATA_CHATS=true
      - DATABASE_SAVE_DATA_LABELS=true
      - DATABASE_SAVE_DATA_HISTORIC=true
      # Redis (use a mesma senha do redis acima)
      - CACHE_REDIS_ENABLED=true
      - CACHE_REDIS_URI=redis://:${REDIS_PASSWORD:-redis123}@redis:6379
      - CACHE_REDIS_PREFIX_KEY=${EVOLUTION_CACHE_REDIS_PREFIX_KEY:-evolution}
      - CACHE_REDIS_SAVE_INSTANCES=false
      - RABBITMQ_ENABLED=false
      - WEBSOCKET_ENABLED=false
      - WEBHOOK_GLOBAL_ENABLED=false
      - WEBHOOK_GLOBAL_URL=
      - WEBHOOK_EVENTS_QRCODE_UPDATED=true
      - WEBHOOK_EVENTS_MESSAGES_UPSERT=true
      - WEBHOOK_EVENTS_MESSAGES_UPDATE=true
      - WEBHOOK_EVENTS_CONNECTION_UPDATE=true
      - QRCODE_LIMIT=30
      - QRCODE_COLOR=#175197
      - CONFIG_SESSION_PHONE_CLIENT=Evolution API
      - CONFIG_SESSION_PHONE_NAME=Chrome
      # API Key (ALTERE AQUI - importante!)
      - AUTHENTICATION_API_KEY=${EVOLUTION_API_KEY:-evolution_api_key_12345}
      - AUTHENTICATION_EXPOSE_IN_FETCH_INSTANCES=true
      - TYPEBOT_ENABLED=false
      - CHATWOOT_ENABLED=false
      - OPENAI_ENABLED=false
      - DIFY_ENABLED=false
      - S3_ENABLED=false
      - TZ=America/Sao_Paulo
      - DEL_INSTANCE=false
    ports:
      - "8080:8080"
    volumes:
      - evolution_instances:/evolution/instances
      - evolution_store:/evolution/store
    networks:
      - app_network
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy

volumes:
  postgres_data:
    driver: local
  redis_data:
    driver: local
  n8n_data:
    driver: local
  evolution_instances:
    driver: local
  evolution_store:
    driver: local

networks:
  app_network:
    driver: bridge