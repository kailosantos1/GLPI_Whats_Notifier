# Evolution API

O código faz uma chamada de saída para enviar texto:

- Método: `POST`.
- Caminho: `/message/sendText/{EVOLUTION_INSTANCE}`.
- URL base: `EVOLUTION_URL`.
- Cabeçalhos: `apikey` e `Content-Type: application/json`.
- Corpo: `{"number": numero, "text": mensagem}`.
- Destinatário: valor de `WHATS_GRUPO_TI`.

`enviar_whatsapp` registra o status HTTP e o corpo da resposta em caso de status 400 ou superior. A implementação não interpreta um corpo de sucesso, não tenta novamente e não converte por conta própria um status de erro em exceção HTTP. Exceções de transporte podem ser registradas pelo tratamento da thread.

O serviço e a mensagem estão em [[02 - Modulos/Notificação WhatsApp|Notificação WhatsApp]]; os dados montados estão em [[04 - Dados/Payload e estado|Payload e estado]].

Referência: [`main.py`](../../../main.py), `enviar_whatsapp`.

← [[05 - Interfaces e Integrações/Índice|Índice de Interfaces e Integrações]]
