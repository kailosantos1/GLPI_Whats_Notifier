# 🚀 Docker Compose - n8n + Evolution API + PostgreSQL + Redis

## Visão geral rápida

- **n8n** `1.119.1` em `http://localhost:5678`
- **Evolution API** `v2.3.6` em `http://localhost:8080`
- **PostgreSQL** `16.4-alpine` (porta 5432) e **Redis** `7.2-alpine` (porta 6379)
- Use `localhost` para acessar via navegador no host. Use `host.docker.internal` quando um container (ex.: o próprio n8n) precisar chamar algo que roda no host ou em outro serviço exposto pelo compose.

## Como subir

```bash
# Edite o .env com suas credenciais (já há um modelo básico versionado)
docker-compose pull   # baixa/atualiza as imagens definidas nas tags
docker-compose up -d  # sobe os containers em background usando o .env
docker-compose ps     # mostra o status atual dos serviços
```

Para desligar: `docker-compose down`. Para apagar dados: `docker-compose down -v`.

## Credenciais padrão (ajuste no `.env`)

- PostgreSQL: `postgres` / `postgres123` (db `n8n`, `evolution`)
- Redis: `redis123`
- Evolution API Key: `evolution_api_key_12345`

⚠️ Troque tudo antes de qualquer uso público/produção.

## Dúvidas comuns
- **Como conectar um webhook ao n8n?** Na Evolution API, aponte o webhook para `http://host.docker.internal:5678/<sua-rota-webhook>` para que o tráfego chegue ao n8n em execução dentro do Docker.
- **Por que `host.docker.internal`?** Dentro dos containers `localhost` aponta para o próprio container. Configure webhooks/nodes do n8n para chamar `http://host.docker.internal:<porta>` e, ao testar no navegador do host, use `http://localhost:<porta>`.
- **Como atualizar versões?** Troque as tags das imagens no `docker-compose.yml`, rode `docker-compose pull` e suba de novo.
- **Problema com dados antigos do Postgres?** Remova o volume: `docker volume rm docker-evolution-and-n8n_postgres_data` (após `docker-compose down -v`).

Pronto para uso local de desenvolvimento. Apenas para fins educacionais. Contributions são bem-vindas. 