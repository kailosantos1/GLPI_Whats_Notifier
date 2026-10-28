# Payload e estado

## Entrada do webhook

O handler lê JSON ou formulário e procura um identificador por `ticket_id`, com fallback para `Chamado`. Não há esquema Pydantic nem validação tipada do corpo declarada no código. Após a leitura, o ID é tratado como texto e zeros iniciais são removidos.

## Dados consultados e saída

Para decidir e compor a mensagem, o serviço consulta:

- Ticket: `name` (título) e `date` (data de abertura).
- Associação de grupos: `type` e `groups_id`; o primeiro item de tipo `2` é usado como grupo técnico.
- Associação de usuários: `type` e `users_id`; considera requerente (`type == 1`) que não seja um bot configurado.
- Usuário: `firstname` e `realname`.
- Mensagem de saída: destinatário `WHATS_GRUPO_TI` e texto com usuário, ticket, título e data.

Esses campos são acessados diretamente pelo código, sem definição de um modelo de domínio separado.

## Persistência e deduplicação

Não há banco de dados ou persistência durável observada. `ultimos_chamados` é uma lista global, limitada aos 100 IDs mais recentes dentro do processo. O conteúdo é perdido ao reiniciar; a estrutura não fornece deduplicação distribuída entre instâncias.

Os nomes das variáveis de configuração, sem valores de segredo, estão em [[02 - Modulos/Aplicação e configuração|Aplicação e configuração]]. O formato de entrada é descrito em [[05 - Interfaces e Integrações/Webhook de entrada|Webhook de entrada]].

← [[04 - Dados/Índice|Índice de Dados]]
