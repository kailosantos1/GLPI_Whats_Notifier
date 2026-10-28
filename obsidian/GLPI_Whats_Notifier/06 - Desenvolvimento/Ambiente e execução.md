# Ambiente e execução

## Configuração necessária

O código espera `.env` ao lado de `main.py` (ou do executável), conforme descrito em [[02 - Modulos/Aplicação e configuração|Aplicação e configuração]]. O repositório não fornece `.env.example`; use os nomes documentados sem inserir credenciais no vault. O `.gitignore` exclui `.env`.

## Comandos

Não há scripts de instalação ou execução definidos. O bloco principal em [`main.py`](../../../main.py) contém um caminho de execução direta; o seguinte comando é **identificado no código, mas não foi executado nesta análise**:

```bash
python main.py
```

Esse caminho chama Uvicorn em `0.0.0.0:8000`, com access log desativado. Isso vincula o servidor a todas as interfaces de rede disponíveis; o código não configura TLS ou autenticação do webhook.

Um fluxo usual de ambiente virtual e instalação seria:

```bash
python -m venv .venv
python -m pip install -r requirements.txt
python main.py
```

Esse fluxo é **sugerido, não verificado pelo projeto**. Em particular, `requirements.txt` está codificado em UTF-16LE e pode não ser aceito diretamente por ferramentas que esperam UTF-8; a instalação não foi tentada. Não existe declaração de versão mínima de Python.

## Logs

O processo grava `app.log` junto ao script/executável e mantém rotação limitada. Garanta que o diretório seja gravável e considere que títulos e nomes de usuários podem ser registrados. Mais detalhes em [[02 - Modulos/Aplicação e configuração|Aplicação e configuração]].

← [[06 - Desenvolvimento/Índice|Índice de Desenvolvimento]]
