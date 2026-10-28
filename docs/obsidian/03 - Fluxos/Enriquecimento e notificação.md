# Enriquecimento e notificação

Após a decisão do grupo, o handler inicia `processar_chamado_em_background` em uma `threading.Thread` daemon. A resposta HTTP não aguarda as consultas do requerente nem o envio.

```mermaid
sequenceDiagram
    participant H as handle_webhook
    participant T as Thread daemon
    participant G as GLPI
    participant E as Evolution API
    H->>T: ticket_id, título, data
    T->>G: GET Ticket_User (até 10 tentativas)
    Note over T,G: Intervalo de 3 s entre tentativas; timeout de 10 s por chamada
    G-->>T: ator type 1 que não é bot
    T->>G: GET User/{id}
    G-->>T: firstname e realname
    T->>E: POST message/sendText/{instância}
    E-->>T: status HTTP registrado
```

Se nenhum requerente for obtido, o texto usa `Não identificado`. A consulta de requerente aceita status 200/206 e ignora usuários cujos IDs estejam em `BOTS_USER_IDS`. O comentário e os argumentos do código definem dez tentativas com três segundos entre elas; a duração real pode ser maior por causa do tempo das requisições. Se usuário é encontrado, uma consulta separada busca o nome.

O código tenta converter a data GLPI do formato `%Y-%m-%d %H:%M:%S`, subtrair três horas fixas e exibi-la como `%d/%m/%Y %H:%M`; se falhar, preserva o texto original. Isso é uma regra fixa no código, não uma conversão de fuso configurável.

A thread é daemon e o estado não é persistido. O comportamento em encerramento/reinício do processo e os limites de confiabilidade são anotados em [[08 - Pendências/Lacunas confirmadas|Lacunas confirmadas]].

Referências: [`main.py`](../../../main.py), funções `buscar_requerente_com_retry`, `processar_chamado_em_background` e `enviar_whatsapp`.

← [[03 - Fluxos/Índice|Índice de Fluxos]]
