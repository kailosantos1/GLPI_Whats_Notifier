# GLPI Whats Notifier

Este vault documenta o serviço Python que recebe notificações de chamados, consulta o GLPI e, para chamados atribuídos ao grupo de TI configurado, envia uma mensagem a um grupo pela Evolution API.

## Mapa do vault

- [[01 - Arquitetura/Índice|Arquitetura]] — desenho do sistema e tecnologias.
- [[02 - Modulos/Índice|Módulos]] — responsabilidades implementadas em `main.py`.
- [[03 - Fluxos/Índice|Fluxos]] — recepção, filtragem e notificação.
- [[04 - Dados/Índice|Dados]] — payload, dados consultados e estado em memória.
- [[05 - Interfaces e Integrações/Índice|Interfaces e integrações]] — webhook e APIs externas.
- [[06 - Desenvolvimento/Índice|Desenvolvimento]] — configuração, execução e limites de validação.
- [[08 - Pendências/Índice|Pendências e lacunas]] — itens não especificados ou não confirmados no repositório.

## Referência do projeto

O código executável está concentrado em [`main.py`](../../../main.py). O README existente descreve o objetivo em uma frase: [`README.md`](../../../README.md). O manifesto de dependências é [`requirements.txt`](../../../requirements.txt).

## Escopo e evidência

As notas descrevem o código e os arquivos rastreados no repositório. Não foram lidos arquivos `.env` nem valores de credenciais. O diretório contém um módulo Python principal, um README, um manifesto de dependências e um `.gitignore`; não foram encontrados testes, esquema de banco, documentação de API ou configuração de deploy. Ausências e inferências estão identificadas como tais nas notas.

---

Próximo: [[01 - Arquitetura/Índice|Arquitetura]].
