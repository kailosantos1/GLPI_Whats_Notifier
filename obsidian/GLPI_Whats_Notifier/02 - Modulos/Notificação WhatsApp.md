# Notificação WhatsApp

O envio é realizado pela função `enviar_whatsapp(numero, mensagem)` em [`main.py`](../../../main.py). Ela envia `POST {EVOLUTION_URL}/message/sendText/{EVOLUTION_INSTANCE}` com cabeçalho `apikey`, tipo de conteúdo JSON e corpo com os campos `number` e `text`.

`processar_chamado_em_background` compõe uma mensagem em português com nome do requerente, número do chamado, título e data formatada. O destinatário é `WHATS_GRUPO_TI`. Esse valor é passado como número, embora o destino seja descrito como grupo no objetivo do projeto.

A função registra o status HTTP e, em status a partir de 400, o corpo de erro. No código observado, não há validação explícita de sucesso nem repetição do envio após erro HTTP. Exceções da rotina de background são registradas pelo logger.

O fluxo do worker está em [[03 - Fluxos/Enriquecimento e notificação|Enriquecimento e notificação]]; o contrato externo está em [[05 - Interfaces e Integrações/Evolution API|Evolution API]].

Referência: [`main.py`](../../../main.py), funções `enviar_whatsapp` e `processar_chamado_em_background`.

← [[02 - Modulos/Índice|Índice de Módulos]]
