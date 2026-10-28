# GLPI REST API

A integração usa a URL base `GLPI_URL` e cabeçalhos configurados por variáveis de ambiente. O código não informa a versão da API nem documenta parâmetros adicionais.

| Método HTTP | Caminho relativo | Uso no código |
|---|---|---|
| GET | `/initSession` | Envia `App-Token` e `Authorization: user_token ...`; extrai `session_token` quando o status é 200. |
| GET | `/Ticket/{ticket_id}` | Lê ticket e campos `name` e `date`. |
| GET | `/Ticket/{ticket_id}/Group_Ticket` | Lê associações de grupos, incluindo `type` e `groups_id`. |
| GET | `/Ticket/{ticket_id}/Ticket_User` | Procura requerente; aceita status 200 ou 206; a rotina define timeout de 10 segundos e retry. |
| GET | `/User/{user_id}` | Obtém `firstname` e `realname` do requerente. |

As demais consultas iniciam uma sessão com `criar_sessao_glpi` e usam `Session-Token` junto a `App-Token`. Nos caminhos descritos, o código não define timeout para os `requests.get` além da busca `Ticket_User`, nem mostra encerramento da sessão.

A sequência de chamadas está em [[02 - Modulos/Integração GLPI|Integração GLPI]]; o fluxo está em [[03 - Fluxos/Enriquecimento e notificação|Enriquecimento e notificação]].

Referência: [`main.py`](../../../main.py).

← [[05 - Interfaces e Integrações/Índice|Índice de Interfaces e Integrações]]
