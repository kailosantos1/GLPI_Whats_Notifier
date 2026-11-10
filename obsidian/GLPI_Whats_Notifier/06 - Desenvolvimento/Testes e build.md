# Testes e build

## Evidência no repositório

Nos arquivos rastreados não há diretório ou arquivos de teste, configuração de pytest/unittest, scripts de lint/type-check, pipeline CI, Dockerfile, definição de build ou arquivo `.spec` do PyInstaller.

`requirements.txt` inclui PyInstaller e `main.py` contém tratamento para execução sem console, mas isso não documenta um comando de empacotamento reproduzível. O `.gitignore` exclui arquivos `.spec`, executáveis e saídas `build/`/`dist/`; não foi inferido um processo de release a partir dessas exclusões.

## Validação desta documentação

O código, manifesto e links foram inspecionados estaticamente. A aplicação e as chamadas a serviços externos não foram iniciadas; não foram encontrados testes automatizados existentes para executar. Veja as limitações em [[08 - Pendências/Lacunas confirmadas|Lacunas confirmadas]].

Referências: [`main.py`](../../../main.py), [`requirements.txt`](../../../requirements.txt), [`.gitignore`](../../../.gitignore).

← [[06 - Desenvolvimento/Índice|Índice de Desenvolvimento]]
