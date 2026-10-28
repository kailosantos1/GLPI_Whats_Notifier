# Webhook de entrada

## Contrato observado

- Método e rota: `POST /webhook`.
- Formatos tentados: JSON primeiro; se a leitura falhar, formulário.
- Chave de entrada: `ticket_id` ou, como alternativa, `Chamado`.
- Respostas construídas: `status=erro` para campo ausente ou ticket não encontrado; `status=duplicado`; `status=ok` com `processando=true` ou `ignorado=true`.
- Erros inesperados no handler: HTTP 500 com mensagem genérica; detalhes são escritos em `app.log`.

As respostas em dicionário não definem status HTTP próprio, então normalmente resultam em 200. O endpoint não declara autenticação, assinatura, segredo de webhook, modelo de validação ou filtro de origem no código observado. Isso descreve o que está implementado, não uma recomendação de exposição pública.

O processamento e o filtro de grupo estão detalhados em [[03 - Fluxos/Entrada e decisão|Entrada e decisão]].

Referência: [`main.py`](../../../main.py), `handle_webhook`.

← [[05 - Interfaces e Integrações/Índice|Índice de Interfaces e Integrações]]
