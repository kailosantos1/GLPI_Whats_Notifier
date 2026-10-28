# Integração GLPI

A integração é implementada por funções síncronas em [`main.py`](../../../main.py), usando `requests`.

| Função | Operação observada |
|---|---|
| `criar_sessao_glpi()` | `GET {GLPI_URL}/initSession`, com `App-Token` e autorização `user_token`; retorna `session_token` em resposta 200. |
| `buscar_ticket(ticket_id)` | Abre uma sessão e consulta `GET /Ticket/{ticket_id}`. Retorna JSON em 200 ou `None`. |
| `buscar_grupo_ticket(ticket_id)` | Abre uma sessão e consulta `GET /Ticket/{ticket_id}/Group_Ticket`. Retorna JSON em 200 ou lista vazia. |
| `buscar_requerente_com_retry(ticket_id, ...)` | Consulta `GET /Ticket/{ticket_id}/Ticket_User` até dez tentativas, com três segundos de intervalo; aceita status 200 ou 206 e seleciona ator `type == 1` fora dos IDs de bots. |
| `buscar_usuario(user_id)` | Abre uma sessão e consulta `GET /User/{user_id}`; combina `firstname` e `realname` em caso de sucesso. |

O retry aplica timeout de 10 segundos somente à consulta `Ticket_User`. Os outros `requests.get` não definem timeout no código. Não há chamada observada para encerrar sessão GLPI. A autenticação usa tokens de configuração; os valores não são documentados aqui.

A detecção do grupo elegível e a ordem de chamadas estão em [[03 - Fluxos/Entrada e decisão|Entrada e decisão]] e [[03 - Fluxos/Enriquecimento e notificação|Enriquecimento e notificação]]. Contrato de endpoints: [[05 - Interfaces e Integrações/GLPI REST API|GLPI REST API]].

Referência de código: [`main.py`](../../../main.py), funções `criar_sessao_glpi`, `buscar_ticket`, `buscar_grupo_ticket`, `buscar_requerente_com_retry` e `buscar_usuario`.

← [[02 - Modulos/Índice|Índice de Módulos]]
