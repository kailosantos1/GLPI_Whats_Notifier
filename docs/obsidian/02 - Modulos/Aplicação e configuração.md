# Aplicação e configuração

## Aplicação HTTP

Em [`main.py`](../../../main.py), `app = FastAPI()` cria a aplicação ASGI e `handle_webhook` é registrado em `POST /webhook`. O bloco `if __name__ == "__main__"` executa `uvicorn.run` em `0.0.0.0:8000` com `access_log=False`.

## Configuração

`load_dotenv` procura `.env` em `BASE_DIR`, calculado a partir de `sys.argv[0]`, e não do diretório de trabalho atual. A aplicação lê os seguintes nomes de variáveis, sem que seus valores sejam reproduzidos nesta documentação:

| Variável | Uso observado | Valor padrão no código |
|---|---|---|
| `GLPI_URL` | URL base usada para consultar o GLPI | Nenhum |
| `GLPI_APP_TOKEN` | Cabeçalho `App-Token` | Nenhum |
| `GLPI_USER_TOKEN` | Autorização `user_token` ao abrir sessão | Nenhum |
| `EVOLUTION_URL` | URL base da Evolution API | Nenhum |
| `EVOLUTION_API_KEY` | Cabeçalho `apikey` | Nenhum |
| `EVOLUTION_INSTANCE` | Segmento da instância no endpoint de envio | Nenhum |
| `GRUPO_TI_ID` | Identificador do grupo de TI usado no filtro | `9` |
| `WHATS_GRUPO_TI` | Destinatário passado como `number` | Nenhum |
| `BOTS_USER_IDS` | IDs separados por vírgula excluídos como requerentes | `282,286` |

O código converte `GRUPO_TI_ID` e cada item de `BOTS_USER_IDS` para inteiro durante a importação do módulo. Valores inválidos podem impedir a inicialização. Não existe arquivo de exemplo de configuração rastreado; consulte também [[06 - Desenvolvimento/Ambiente e execução|Ambiente e execução]].

## Logging

Um `RotatingFileHandler` grava `app.log` ao lado do script/executável: cada arquivo pode atingir 5 MiB e são mantidos três backups. O logger é configurado no nível `INFO`. O código registra detalhes do chamado, título, nome do usuário e respostas de erro da Evolution API; esses logs podem conter dados pessoais ou dados operacionais.

← [[02 - Modulos/Índice|Índice de Módulos]] · [[04 - Dados/Payload e estado|Dados]]
