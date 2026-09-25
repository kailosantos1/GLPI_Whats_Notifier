# main.py
from fastapi import FastAPI, Request
from dotenv import load_dotenv
import requests
import uvicorn
import os
import time
import threading
from datetime import datetime, timedelta

load_dotenv()

app = FastAPI()

GLPI_URL = os.getenv("GLPI_URL")
GLPI_APP_TOKEN = os.getenv("GLPI_APP_TOKEN")
GLPI_USER_TOKEN = os.getenv("GLPI_USER_TOKEN")

EVOLUTION_URL = os.getenv("EVOLUTION_URL")
EVOLUTION_API_KEY = os.getenv("EVOLUTION_API_KEY")
EVOLUTION_INSTANCE = os.getenv("EVOLUTION_INSTANCE")

GRUPO_TI_ID = int(os.getenv("GRUPO_TI_ID", "9"))
WHATS_GRUPO_TI = os.getenv("WHATS_GRUPO_TI")

# IDs dos bots que precisam ser IGNORADOS como requerente.
# Vem do .env como "282,286" (separado por vírgula).
# 282 = bot.teams / 286 = bot.email
BOTS_USER_IDS = {
    int(x.strip())
    for x in os.getenv("BOTS_USER_IDS", "282,286").split(",")
    if x.strip()
}

ultimos_chamados = []


def criar_sessao_glpi():
    url = f"{GLPI_URL}/initSession"
    headers = {
        "App-Token": GLPI_APP_TOKEN,
        "Authorization": f"user_token {GLPI_USER_TOKEN}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["session_token"]
    raise Exception("Erro ao criar sessão GLPI")


def buscar_usuario(user_id):
    if not user_id:
        return "Não identificado"
    
    session_token = criar_sessao_glpi()
    url = f"{GLPI_URL}/User/{user_id}"
    headers = {
        "App-Token": GLPI_APP_TOKEN,
        "Session-Token": session_token
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        nome = f"{data.get('firstname', '')} {data.get('realname', '')}"
        return nome.strip()
    
    return "Não identificado"


def buscar_ticket(ticket_id):
    session_token = criar_sessao_glpi()
    url = f"{GLPI_URL}/Ticket/{ticket_id}"
    headers = {
        "App-Token": GLPI_APP_TOKEN,
        "Session-Token": session_token
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    
    return None


def buscar_grupo_ticket(ticket_id):
    session_token = criar_sessao_glpi()
    url = f"{GLPI_URL}/Ticket/{ticket_id}/Group_Ticket"
    headers = {
        "App-Token": GLPI_APP_TOKEN,
        "Session-Token": session_token
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    
    return []


def buscar_requerente_com_retry(ticket_id, max_tentativas=10, intervalo=3):
    """
    Busca o requerente com retry em background.
    Tenta 10 vezes com 3 segundos de intervalo (30 segundos total).
    Ignora qualquer ator que esteja em BOTS_USER_IDS.
    """
    session_token = criar_sessao_glpi()
    
    url = f"{GLPI_URL}/Ticket/{ticket_id}/Ticket_User"
    
    headers = {
        "App-Token": GLPI_APP_TOKEN,
        "Session-Token": session_token
    }
    
    for tentativa in range(1, max_tentativas + 1):
        print(f"🔍 Buscando requerente (tentativa {tentativa}/{max_tentativas})...")
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code in [200, 206]:
                atores = response.json()
                
                if isinstance(atores, list):
                    # Procura type=1 que NÃO seja nenhum dos bots
                    for ator in atores:
                        if isinstance(ator, dict):
                            user_id = ator.get("users_id")
                            tipo = ator.get("type")
                            
                            if tipo == 1 and user_id not in BOTS_USER_IDS:
                                print(f"✅ Requerente real encontrado: ID={user_id}")
                                return user_id
                    
                    print(f"⚠️ Só tem bots como requerente. Aguardando...")
            
        except Exception as e:
            print(f"Erro na tentativa {tentativa}: {e}")
        
        # Espera antes da próxima tentativa
        if tentativa < max_tentativas:
            time.sleep(intervalo)
    
    print("❌ Requerente não encontrado após todas as tentativas")
    return None


def enviar_whatsapp(numero, mensagem):
    url = f"{EVOLUTION_URL}/message/sendText/{EVOLUTION_INSTANCE}"
    headers = {
        "apikey": EVOLUTION_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {"number": numero, "text": mensagem}
    response = requests.post(url, json=payload, headers=headers)
    print(f"WhatsApp: Status {response.status_code}")


def processar_chamado_em_background(ticket_id, titulo, data_abertura):
    """
    Processa o chamado em background.
    Busca o requerente com retry e envia o WhatsApp.
    """
    print(f"\n⏳ Processando chamado {ticket_id} em background...")
    
    # Busca o requerente com até 30 segundos de espera
    usuario_id = buscar_requerente_com_retry(ticket_id, max_tentativas=10, intervalo=3)
    
    if usuario_id:
        usuario_nome = buscar_usuario(usuario_id)
    else:
        usuario_nome = "Não identificado"
    
    print(f"\n📋 Resultado final:")
    print(f"  Ticket: {ticket_id}")
    print(f"  Título: {titulo}")
    print(f"  Usuário: {usuario_nome}")
    print(f"  Data: {data_abertura}")
    
    mensagem = f"""
🚨 *Novo chamado aberto no GLPI*

👤 *Usuário:* {usuario_nome}

🎫 *Chamado:* {ticket_id}

📝 *Título:* {titulo}

📅 *Data:* {data_abertura}
"""
    
    enviar_whatsapp(WHATS_GRUPO_TI, mensagem)


@app.post("/webhook")
async def handle_webhook(request: Request):
    print("\n==============================")
    print("WEBHOOK RECEBIDO")
    print("==============================")
    
    body = {}
    
    try:
        body = await request.json()
    except:
        try:
            form = await request.form()
            body = dict(form)
        except:
            pass
    
    ticket_id = body.get("ticket_id") or body.get("Chamado")
    
    if ticket_id:
        ticket_id = str(ticket_id).lstrip("0")
    
    print(f"TICKET ID: {ticket_id}")
    
    if not ticket_id:
        return {"status": "erro", "motivo": "sem ticket_id"}
    
    if ticket_id in ultimos_chamados:
        print("DUPLICADO")
        return {"status": "duplicado"}
    
    ultimos_chamados.append(ticket_id)
    ultimos_chamados[:] = ultimos_chamados[-100:]
    
    # Busca o ticket
    ticket = buscar_ticket(ticket_id)
    
    if not ticket:
        return {"status": "erro", "motivo": "ticket não encontrado"}
    
    # Busca grupos
    grupos = buscar_grupo_ticket(ticket_id)
    
    grupo_tecnico = 0
    for grupo in grupos:
        if grupo.get("type") == 2:
            grupo_tecnico = grupo.get("groups_id")
            break
    
    titulo = ticket.get("name", "Sem título")
    
    # Ajusta data
    data_original = ticket.get("date", "")
    
    try:
        data_obj = datetime.strptime(data_original, "%Y-%m-%d %H:%M:%S")
        data_obj = data_obj - timedelta(hours=3)
        data_abertura = data_obj.strftime("%d/%m/%Y %H:%M")
    except:
        data_abertura = data_original
    
    print(f"\n📋 Dados iniciais:")
    print(f"  Ticket: {ticket_id}")
    print(f"  Título: {titulo}")
    print(f"  Grupo Técnico: {grupo_tecnico}")
    print(f"  Data: {data_abertura}")
    
    # Verifica se é do grupo TI
    if int(grupo_tecnico) == GRUPO_TI_ID:
        # Processa em background (não bloqueia o webhook)
        thread = threading.Thread(
            target=processar_chamado_em_background,
            args=(ticket_id, titulo, data_abertura),
            daemon=True
        )
        thread.start()
        
        print("✅ Processamento iniciado em background")
        
        return {"status": "ok", "processando": True}
    else:
        print("CHAMADO NÃO É DO GRUPO TI")
        return {"status": "ok", "ignorado": True}


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        access_log=False,
        log_config=None
    )