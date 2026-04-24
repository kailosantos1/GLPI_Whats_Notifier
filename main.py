import os
import requests
import pytz
from fastapi import FastAPI, Request, BackgroundTasks
from datetime import datetime
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

app = FastAPI(title="GLPI Unified Bridge - SystemUp")

# --- FUNÇÃO 1: PROCESSAR NOVO CHAMADO (TI / FLEX) ---
def processar_novo_chamado(chamado_id):
    try:
        url_glpi = os.getenv("URL_GLPI")
        headers = {"App-Token": os.getenv("APP_TOKEN"), "Content-Type": "application/json"}
        
        # Autenticação
        auth_payload = {"Authorization": f"user_token {os.getenv('USER_TOKEN')}"}
        auth = requests.post(f"{url_glpi}initSession", headers={**headers, **auth_payload})
        headers["Session-Token"] = auth.json().get("session_token")

        # Busca dados do Chamado e Grupo
        ticket = requests.get(f"{url_glpi}Ticket/{chamado_id}", headers=headers).json()
        grupo_info = requests.get(f"{url_glpi}Ticket/{chamado_id}/Group_Ticket", headers=headers).json()
        
        grupo_id = str(grupo_info[0].get("groups_id")).strip() if grupo_info else ""
        id_flex = str(os.getenv("GRUPO_GLPI_FLEX")).strip()

        if grupo_id == id_flex:
            destino = os.getenv("WHATS_FLEX")
            setor = "FLEXSMART"
        else:
            destino = os.getenv("WHATS_TI")
            setor = "TI / MANUTENÇÃO"

        # Detalhes do Usuário
        user_id = ticket.get("users_id_recipient")
        user = requests.get(f"{url_glpi}User/{user_id}", headers=headers).json()
        nome_usuario = f"{user.get('firstname', '')} {user.get('realname', '')}"

        # Formatação
        id_limpo = str(int(chamado_id))
        dt_utc = datetime.strptime(ticket.get("date"), "%Y-%m-%d %H:%M:%S")
        dt_br = pytz.utc.localize(dt_utc).astimezone(pytz.timezone('America/Sao_Paulo'))
        data_fmt = dt_br.strftime("%d/%m/%Y %H:%M")

        mensagem = (f"🚨 *Novo chamado aberto no GLPI*\n\n"
                    f"👤 Usuário: *{nome_usuario}*\n"
                    f"🎫 Chamado: *{id_limpo}* foi aberto!!\n"
                    f"📝 *Título:* {ticket.get('name')}\n"
                    f"📅 *Data:* {data_fmt}\n\nAcesse o GLPI para verificar.")

        # Envio Evolution API
        evo_url = f"{os.getenv('URL_EVOLUTION')}/message/sendText/{os.getenv('NOME_INSTANCIA')}"
        requests.post(evo_url, headers={"apikey": os.getenv("API_KEY_EVO")},
                      json={"number": destino, "text": mensagem})
        
        print(f"✅ Notificação Novo Chamado: {setor} (ID: {id_limpo})")

    except Exception as e:
        print(f"❌ Erro no fluxo Novo Chamado: {e}")

# --- FUNÇÃO 2: PROCESSAR VALIDAÇÃO (LÍDERES) ---
def processar_validacao(form_answer_id):
    try:
        url_glpi = os.getenv("URL_GLPI")
        headers = {"App-Token": os.getenv("APP_TOKEN"), "Content-Type": "application/json"}
        
        # Autenticação
        auth = requests.post(f"{url_glpi}initSession", 
                             headers={**headers, "Authorization": f"user_token {os.getenv('USER_TOKEN')}"})
        headers["Session-Token"] = auth.json().get("session_token")

        # Buscar Respostas do FormCreator
        form_data = requests.get(f"{url_glpi}PluginFormcreatorFormAnswer/{form_answer_id}", headers=headers).json()
        
        # Filtro de Grupo (Líderes)
        grupo_validador = str(form_data.get("groups_id_validator")).strip()
        id_lideres_config = str(os.getenv("GRUPO_GLPI_LIDERES")).strip()

        if grupo_validador != id_lideres_config:
            print(f"ℹ️ Validação {form_answer_id} ignorada (Grupo {grupo_validador} não é Líderes).")
            return

        # Detalhes do Requerente
        user_id = form_data.get("requester_id")
        user = requests.get(f"{url_glpi}User/{user_id}", headers=headers).json()
        nome_usuario = f"{user.get('firstname', '')} {user.get('realname', '')}"
        
        id_limpo = str(int(form_answer_id))
        dt_utc = datetime.strptime(form_data.get("request_date"), "%Y-%m-%d %H:%M:%S")
        dt_br = pytz.utc.localize(dt_utc).astimezone(pytz.timezone('America/Sao_Paulo'))
        data_fmt = dt_br.strftime("%d/%m/%Y %H:%M")

        mensagem = (f"🚨 *Chamado aguardando validação*\n\n"
                    f"👤 Usuário: *{nome_usuario}*\n"
                    f"🎫 Chamado: *{id_limpo}*\n"
                    f"📝 Título: *{form_data.get('name')}*\n"
                    f"📅 Data: *{data_fmt}*\n\n"
                    f"⚠️ Este chamado requer sua validação.\n\n"
                    f"🔗 Acesse o GLPI para validar.")

        # Envio Evolution API (ID do Grupo @g.us)
        destino_lideres = os.getenv("WHATS_LIDERES")
        evo_url = f"{os.getenv('URL_EVOLUTION')}/message/sendText/{os.getenv('NOME_INSTANCIA')}"
        
        requests.post(evo_url, headers={"apikey": os.getenv("API_KEY_EVO")},
                      json={"number": destino_lideres, "text": mensagem})
        
        print(f"✅ Notificação Validação enviada para o Grupo!")

    except Exception as e:
        print(f"❌ Erro no fluxo Validação: {e}")

# --- ENDPOINTS (WEBHOOKS) ---

@app.post("/webhook")
async def handle_novo_chamado(request: Request, background_tasks: BackgroundTasks):
    body = await request.json()
    id_c = body.get("Chamado")
    if id_c:
        background_tasks.add_task(processar_novo_chamado, id_c)
        return {"status": "ok", "tipo": "novo_chamado"}
    return {"status": "error"}

@app.post("/webhook-validacao")
async def handle_validacao(request: Request, background_tasks: BackgroundTasks):
    body = await request.json()
    id_f = body.get("id") or body.get("items_id")
    if id_f:
        background_tasks.add_task(processar_validacao, id_f)
        return {"status": "ok", "tipo": "validacao"}
    return {"status": "error"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)