# Lacunas confirmadas

Os itens abaixo não estão definidos nos arquivos rastreados consultados. São pontos que exigem confirmação antes de documentar uma implantação ou comportamento mais amplo.

## Ambiente e entrega

- Versão mínima de Python e sistemas operacionais suportados não declarados.
- `requirements.txt` está em UTF-16LE; o processo de instalação esperado não está documentado nem foi testado.
- PyInstaller aparece nas dependências, mas não há instrução de build ou configuração `.spec` rastreada.
- Não há configuração de container, serviço do sistema, proxy, deploy ou ambiente de produção.
- Não há exemplo de variáveis de ambiente; os valores efetivos são locais e foram deliberadamente excluídos desta análise.

## Comportamento e confiabilidade

- Não há testes automatizados ou pipeline de validação no repositório.
- Não foi configurada autenticação/assinatura no endpoint `/webhook` no código observado; não está documentado se a proteção ocorre em outra camada.
- A deduplicação existe somente em memória, guarda no máximo 100 IDs por processo e é adicionada antes de confirmar que o ticket existe.
- O trabalho ocorre em thread daemon, sem fila ou persistência durável; garantias de entrega durante reinício/encerramento não são especificadas.
- A maioria das chamadas HTTP de saída não declara timeout. A resposta da Evolution API é registrada, mas o código não confirma semanticamente a entrega.
- Não há instrução de operação para monitorar logs, retenção de dados neles, alertas, recuperação de falha ou rotação fora do handler local.
- A conversão de horário subtrai três horas fixas; não há política de fuso horário documentada.

Esses pontos são descrições de ausência no material examinado e não uma afirmação de que não existam controles externos ao repositório. Ver também [[06 - Desenvolvimento/Testes e build|Testes e build]] e [[03 - Fluxos/Enriquecimento e notificação|Enriquecimento e notificação]].

← [[08 - Pendências/Índice|Índice de Pendências]]
