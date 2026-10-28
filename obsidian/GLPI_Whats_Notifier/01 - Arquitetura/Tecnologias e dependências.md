# Tecnologias e dependências

## Componentes usados no código

Em [`main.py`](../../../main.py) estão os imports de:

- **FastAPI** e **Starlette** (respostas e suporte HTTP), com **Uvicorn** como servidor ASGI.
- **Requests** para chamadas HTTP de saída ao GLPI e à Evolution API.
- **python-dotenv** para carregar variáveis do arquivo `.env`.
- Bibliotecas padrão: `logging`, `threading`, `datetime`, `os`, `sys` e `time`.
- `python-multipart` está listado no manifesto e o handler tenta ler formulário por `request.form()`.

## Manifesto

[`requirements.txt`](../../../requirements.txt) fixa versões para FastAPI, Requests, Uvicorn, python-dotenv, python-multipart e outras bibliotecas, incluindo dependências transitivas e pacotes relacionados ao PyInstaller. O arquivo está codificado em UTF-16LE; esse detalhe pode afetar ferramentas que esperam um manifesto UTF-8. A instalação com pip não foi executada nem validada.

O manifesto inclui PyInstaller e hooks, mas o repositório não contém `.spec` rastreado nem instrução de build. Sua presença, por si só, não confirma um processo de empacotamento suportado.

## Compatibilidade não declarada

Não há metadados de pacote que definam a versão mínima de Python. A versão de Python usada para desenvolvimento/produção também não está especificada nos arquivos rastreados.

← [[01 - Arquitetura/Índice|Índice de Arquitetura]] · [[06 - Desenvolvimento/Índice|Desenvolvimento]]
