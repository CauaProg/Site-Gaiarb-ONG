# Servidor Backend do GAIARB

import os
import json
import sqlite3
import hashlib
import decimal
import datetime
import smtplib
import threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify, send_from_directory
try:
    from flask_cors import CORS
    has_cors = True
except ImportError:
    has_cors = False
import mysql.connector

app = Flask(__name__, static_folder='.', static_url_path='')
if has_cors:
    CORS(app)

MYSQL_ACTIVE = False
DB_FILE = 'gaiarb.db'

def calculate_crc16(data: str) -> str:
    crc = 0xFFFF
    for char in data:
        crc ^= ord(char) << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = ((crc << 1) ^ 0x1021) & 0xFFFF
            else:
                crc = (crc << 1) & 0xFFFF
    return f"{crc:04X}"

def get_connection():
    if MYSQL_ACTIVE:
        return mysql.connector.connect(
            host=os.environ.get("DB_HOST", "localhost"),
            port=int(os.environ.get("DB_PORT", 3306)),
            user=os.environ.get("DB_USER", "root"),
            password=os.environ.get("DB_PASSWORD", "[CONFIDENCIAL]"),
            database=os.environ.get("DB_NAME", "bd_teste_01")
        )
    else:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        return conn

def run_db_query(query, params=None):
    if params is None:
        params = ()
    
    if MYSQL_ACTIVE:
        query = query.replace('?', '%s')
        
    conn = get_connection()
    try:
        if MYSQL_ACTIVE:
            cursor = conn.cursor(dictionary=True)
        else:
            cursor = conn.cursor()
            
        cursor.execute(query, params)
        if query.strip().upper().startswith('SELECT'):
            rows = cursor.fetchall()
            if not MYSQL_ACTIVE:
                return [dict(row) for row in rows]
            return rows
        else:
            conn.commit()
            return cursor.lastrowid
    finally:
        conn.close()

def init_db():
    global MYSQL_ACTIVE
    # 1. Tenta conexao com o MySQL
    try:
        db_name = os.environ.get("DB_NAME", "bd_teste_01")
        print(f"Attempting to connect to MySQL database '{db_name}'...")
        
        if os.environ.get("DB_NAME"):
            # Banco na nuvem: conecta diretamente
            conn = mysql.connector.connect(
                host=os.environ.get("DB_HOST"),
                port=int(os.environ.get("DB_PORT", 3306)),
                user=os.environ.get("DB_USER"),
                password=os.environ.get("DB_PASSWORD"),
                database=db_name
            )
        else:
            # Setup local: tenta criar o banco se nao existir
            conn = mysql.connector.connect(
                host=os.environ.get("DB_HOST", "localhost"),
                port=int(os.environ.get("DB_PORT", 3306)),
                user=os.environ.get("DB_USER", "root"),
                password=os.environ.get("DB_PASSWORD", "[CONFIDENCIAL]")
            )
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
            conn.commit()
            conn.close()
            
            # Conecta ao banco de dados
            conn = mysql.connector.connect(
                host=os.environ.get("DB_HOST", "localhost"),
                port=int(os.environ.get("DB_PORT", 3306)),
                user=os.environ.get("DB_USER", "root"),
                password=os.environ.get("DB_PASSWORD", "[CONFIDENCIAL]"),
                database=db_name
            )
        cursor = conn.cursor()
        
        # Cria tabela de administradores
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admins (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                nome VARCHAR(100) NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Cria tabela de voluntarios
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS voluntarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL,
                whatsapp VARCHAR(30) NOT NULL,
                area VARCHAR(100) NOT NULL,
                disponibilidade VARCHAR(100) NOT NULL,
                mensagem TEXT,
                status VARCHAR(20) DEFAULT 'Pendente',
                data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # Garante que a coluna status existe no MySQL
        try:
            cursor.execute("ALTER TABLE voluntarios ADD COLUMN status VARCHAR(20) DEFAULT 'Pendente'")
        except Exception:
            pass
        
        # Cria tabela de doacoes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS doacoes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                valor DECIMAL(10,2) NOT NULL,
                data_doacao DATETIME DEFAULT CURRENT_TIMESTAMP,
                tipo VARCHAR(20) DEFAULT 'PIX',
                status VARCHAR(20) DEFAULT 'Pendente'
            )
        """)
        
        # Cria tabela da equipe
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS equipe (
                id INT AUTO_INCREMENT PRIMARY KEY,
                numero VARCHAR(10),
                nome VARCHAR(100) NOT NULL,
                cargo VARCHAR(100) NOT NULL,
                bio TEXT,
                ordem INTEGER DEFAULT 0
            )
        """)
        
        # Cria o admin padrao se a tabela estiver vazia
        cursor.execute("SELECT COUNT(*) FROM admins")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO admins (username, password_hash, nome) 
                VALUES ('admin', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'Administrador GAIARB')
            """)
            
        # Cria o admin de teste se nao existir
        cursor.execute("SELECT COUNT(*) FROM admins WHERE username = 'teste1'")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO admins (username, password_hash, nome) 
                VALUES ('teste1', '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4', 'Administrador Teste')
            """)
            
        # Preenche a equipe se estiver vazia
        cursor.execute("SELECT COUNT(*) FROM equipe")
        if cursor.fetchone()[0] == 0:
            members = [
                ('01', 'Ayla de Cássia Franco Bragança', 'Presidente(a)', 'Fundadora do GAIARB, dedicou sua vida ao acolhimento. Lidera o projeto com amor e determinação.', 1),
                ('02', 'Daniele dos Santos Charré Duarte', 'Vice-Presidente(a)', 'Bio dela', 2),
                ('03', 'Danielle de Moraes Góis Diniz', 'Tesoureiro(a)', 'Bio dela', 3),
                ('04', 'Alan Macedo Santos', 'Tesoureiro Adjunto', 'Bio dele', 4),
                ('05', 'Renata Maçulo Quintanilha Pimentel', 'Secretário(a)', 'Bio dela', 5),
                ('06', 'Letícia da Silva Moreira Franco', 'Secretário Adjunto(a)', 'Bio dela', 6)
            ]
            for m in members:
                cursor.execute("""
                    INSERT INTO equipe (numero, nome, cargo, bio, ordem) 
                    VALUES (%s, %s, %s, %s, %s)
                """, m)
        
        conn.commit()
        conn.close()
        MYSQL_ACTIVE = True
        print("Successfully initialized and configured MySQL via mysql.connector!")
        return
    except Exception as e:
        print(f"MySQL initialization failed: {e}. Falling back to SQLite.")
        MYSQL_ACTIVE = False
        
    # 2. Fallback para SQLite local
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(50) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            nome VARCHAR(100) NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS voluntarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            whatsapp VARCHAR(30) NOT NULL,
            area VARCHAR(100) NOT NULL,
            disponibilidade VARCHAR(100) NOT NULL,
            mensagem TEXT,
            status VARCHAR(20) DEFAULT 'Pendente',
            data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    try:
        cursor.execute("ALTER TABLE voluntarios ADD COLUMN status VARCHAR(20) DEFAULT 'Pendente'")
    except sqlite3.OperationalError:
        pass
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS doacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            valor DECIMAL(10,2) NOT NULL,
            data_doacao DATETIME DEFAULT CURRENT_TIMESTAMP,
            tipo VARCHAR(20) DEFAULT 'PIX',
            status VARCHAR(20) DEFAULT 'Pendente'
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS equipe (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero VARCHAR(10),
            nome VARCHAR(100) NOT NULL,
            cargo VARCHAR(100) NOT NULL,
            bio TEXT,
            ordem INTEGER DEFAULT 0
        )
    """)
    
    # Cria o admin padrao se a tabela estiver vazia
    cursor.execute("SELECT COUNT(*) FROM admins")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO admins (username, password_hash, nome) 
            VALUES ('admin', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'Administrador GAIARB')
        """)
        
    # Cria o admin de teste se nao existir
    cursor.execute("SELECT COUNT(*) FROM admins WHERE username = 'teste1'")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO admins (username, password_hash, nome) 
            VALUES ('teste1', '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4', 'Administrador Teste')
        """)
        
    # Preenche a equipe se estiver vazia
    cursor.execute("SELECT COUNT(*) FROM equipe")
    if cursor.fetchone()[0] == 0:
        members = [
            ('01', 'Ayla de Cássia Franco Bragança', 'Presidente(a)', 'Fundadora do GAIARB, dedicou sua vida ao acolhimento. Lidera o projeto com amor e determinação.', 1),
            ('02', 'Daniele dos Santos Charré Duarte', 'Vice-Presidente(a)', 'Bio dela', 2),
            ('03', 'Danielle de Moraes Góis Diniz', 'Tesoureiro(a)', 'Bio dela', 3),
            ('04', 'Alan Macedo Santos', 'Tesoureiro Adjunto', 'Bio dele', 4),
            ('05', 'Renata Maçulo Quintanilha Pimentel', 'Secretário(a)', 'Bio dela', 5),
            ('06', 'Letícia da Silva Moreira Franco', 'Secretário Adjunto(a)', 'Bio dela', 6)
        ]
        for m in members:
            cursor.execute("""
                INSERT INTO equipe (numero, nome, cargo, bio, ordem) 
                VALUES (?, ?, ?, ?, ?)
            """, m)
            
    conn.commit()
    conn.close()
    MYSQL_ACTIVE = False
    print("Successfully initialized and configured local SQLite fallback!")

# (Servico de arquivos estaticos movido para o final)

# Funcao de envio de email de boas-vindas
def send_welcome_email_async(to_email, volunteer_name):
    from email.utils import make_msgid, formatdate
    SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))
    SMTP_USER = os.environ.get("SMTP_USER", "equipegaiarb@gmail.com")
    SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "[CONFIDENCIAL]")
    
    def send_email():
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = "Bem-vindo(a) à equipe de voluntários do GAIARB! 🌻"
            msg['From'] = f"GAIARB <{SMTP_USER}>"
            msg['To'] = to_email
            msg['Message-ID'] = make_msgid(domain='gmail.com')
            msg['Date'] = formatdate(localtime=True)

            text_content = f"""
Olá, {volunteer_name}!

Temos a enorme alegria de informar que o seu cadastro como voluntário(a) no GAIARB foi aprovado por nossa equipe de administração!

A partir de agora, você já pode acessar o nosso Portal do Voluntário para acompanhar nossas atividades e gerenciar suas preferências.

Como acessar o portal:
Acesse a página de login e entre usando as credenciais do seu cadastro:
- E-mail: {to_email}
- WhatsApp: (o número utilizado no seu cadastro)

Agradecemos imensamente pelo seu desejo de fazer a diferença conosco através da arte e do acolhimento. Seja muito bem-vindo(a) à nossa equipe!

Este é um e-mail automático enviado pelo sistema de voluntários do GAIARB.
© 2026 GAIARB. Todos os direitos reservados.
"""

            html_content = f"""
            <html>
            <body style="font-family: 'Inter', sans-serif; background-color: #faf8f4; color: #19201c; padding: 20px;">
                <div style="max-width: 600px; margin: 0 auto; background: white; border: 1px solid #e0ddd5; padding: 30px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
                    <div style="text-align: center; margin-bottom: 20px;">
                        <span style="font-size: 40px;">🌻</span>
                        <h2 style="font-family: 'Lora', serif; color: #1d3d31; margin-top: 10px; margin-bottom: 5px;">Cadastro Aprovado!</h2>
                        <p style="color: #56615b; font-size: 14px; margin: 0;">Você agora faz parte do GAIARB</p>
                    </div>
                    <p>Olá, <strong>{volunteer_name}</strong>,</p>
                    <p>Temos a enorme alegria de informar que o seu cadastro como voluntário(a) no <strong>GAIARB</strong> foi aprovado por nossa equipe de administração!</p>
                    <p>A partir de agora, você já pode acessar o nosso <strong>Portal do Voluntário</strong> para acompanhar nossas atividades e gerenciar suas preferências.</p>
                    
                    <div style="background-color: #f1f5f3; padding: 15px; margin: 20px 0; border-left: 4px solid #1d3d31;">
                        <h4 style="margin: 0 0 10px 0; color: #1d3d31;">Como acessar o portal:</h4>
                        <p style="margin: 0; font-size: 14px; line-height: 1.5;">
                            Acesse a página de login e entre usando as credenciais do seu cadastro:<br>
                            <strong>E-mail:</strong> {to_email}<br>
                            <strong>WhatsApp:</strong> (o número utilizado no seu cadastro)
                        </p>
                    </div>
                    
                    <p>Agradecemos imensamente pelo seu desejo de fazer a diferença conosco através da arte e do acolhimento. Seja muito bem-vindo(a) à nossa equipe!</p>
                    
                    <hr style="border: 0; border-top: 1px solid #e0ddd5; margin: 30px 0;">
                    <div style="text-align: center; font-size: 11px; color: #76817b; line-height: 1.4;">
                        <p>Este é um e-mail automático enviado pelo sistema de voluntários do GAIARB.</p>
                        <p>&copy; 2026 GAIARB. Todos os direitos reservados.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            part_text = MIMEText(text_content, 'plain', 'utf-8')
            msg.attach(part_text)
            
            part_html = MIMEText(html_content, 'html', 'utf-8')
            msg.attach(part_html)

            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, to_email, msg.as_string())
            server.quit()
            print(f"Welcome email successfully sent to {volunteer_name} ({to_email}).")
        except Exception as e:
            print(f"Failed to send welcome email to {to_email}: {e}")

    thread = threading.Thread(target=send_email)
    thread.start()

# Rotas da API

@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    data = request.json or {}
    username = data.get('username')
    password = data.get('password') or data.get('senha')
    
    if not username or not password:
        return jsonify({"success": False, "error": "Usuário e senha são obrigatórios"}), 400
        
    pwd_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    users = run_db_query("SELECT id, username, nome FROM admins WHERE username = ? AND password_hash = ?", (username, pwd_hash))
    if users:
        return jsonify({
            "success": True,
            "token": "gaiarb-admin-simulated-token",
            "admin": {
                "nome": users[0]['nome'],
                "username": users[0]['username']
            }
        })
    return jsonify({"success": False, "error": "Credenciais inválidas"}), 401

@app.route('/api/voluntario/login', methods=['POST'])
def voluntario_login():
    data = request.json or {}
    email = data.get('email')
    whatsapp = data.get('whatsapp')
    
    if not email or not whatsapp:
        return jsonify({"success": False, "error": "E-mail e WhatsApp são obrigatórios"}), 400
        
    vols = run_db_query("SELECT * FROM voluntarios WHERE email = ? AND whatsapp = ?", (email, whatsapp))
    if vols:
        vol = vols[0]
        if (vol.get('status') or 'Pendente') != 'Aprovado':
            return jsonify({"success": False, "error": "Acesso pendente de aprovação pelo administrador."}), 403
        # Formata a data para JSON
        if 'data_cadastro' in vol and isinstance(vol['data_cadastro'], datetime.datetime):
            vol['data_cadastro'] = vol['data_cadastro'].isoformat()
        return jsonify({
            "success": True,
            "token": "gaiarb-vol-simulated-token",
            "voluntario": vol
        })
    return jsonify({"success": False, "error": "Voluntário não encontrado."}), 404

@app.route('/api/voluntario/update', methods=['POST'])
def voluntario_update():
    data = request.json or {}
    vid = data.get('id')
    nome = data.get('nome')
    email = data.get('email')
    whatsapp = data.get('whatsapp')
    area = data.get('area')
    disp = data.get('disponibilidade')
    msg = data.get('mensagem')
    
    if not vid or not nome or not email or not whatsapp:
        return jsonify({"success": False, "error": "Campos obrigatórios ausentes"}), 400
        
    run_db_query(
        "UPDATE voluntarios SET nome=?, email=?, whatsapp=?, area=?, disponibilidade=?, mensagem=? WHERE id=?",
        (nome, email, whatsapp, area, disp, msg, vid)
    )
    return jsonify({"success": True})

@app.route('/api/admin/stats', methods=['GET'])
def admin_stats():
    try:
        vols_count = run_db_query("SELECT COUNT(*) as count FROM voluntarios")[0]['count']
        doacoes_stats = run_db_query("SELECT COUNT(*) as count, SUM(valor) as total FROM doacoes WHERE status = 'Confirmado'")[0]
        d_qty = doacoes_stats['count']
        d_val = doacoes_stats['total'] if doacoes_stats['total'] is not None else 0.0
        
        areas_dist = run_db_query("SELECT area, COUNT(*) as quantidade FROM voluntarios GROUP BY area ORDER BY quantidade DESC")
        
        return jsonify({
            "voluntarios_qtd": vols_count,
            "doacoes_qtd": d_qty,
            "doacoes_valor": float(d_val),
            "areas_dist": areas_dist
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/admin/voluntarios', methods=['GET'])
def get_voluntarios_admin():
    try:
        vols = run_db_query("SELECT * FROM voluntarios ORDER BY data_cadastro DESC")
        for v in vols:
            if 'data_cadastro' in v and isinstance(v['data_cadastro'], datetime.datetime):
                v['data_cadastro'] = v['data_cadastro'].isoformat()
        return jsonify(vols)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/admin/voluntarios/aprovar', methods=['POST'])
def admin_aprovar_voluntario():
    data = request.json or {}
    vid = data.get('id')
    if not vid:
        return jsonify({"success": False, "error": "ID do voluntário é obrigatório"}), 400
    try:
        # Busca o nome e email do candidato
        vols = run_db_query("SELECT nome, email FROM voluntarios WHERE id = ?", (vid,))
        if vols:
            vol = vols[0]
            send_welcome_email_async(vol['email'], vol['nome'])
            
        run_db_query("UPDATE voluntarios SET status = 'Aprovado' WHERE id = ?", (vid,))
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/admin/voluntarios/recusar', methods=['POST'])
def admin_recusar_voluntario():
    data = request.json or {}
    vid = data.get('id')
    if not vid:
        return jsonify({"success": False, "error": "ID do voluntário é obrigatório"}), 400
    try:
        run_db_query("DELETE FROM voluntarios WHERE id = ?", (vid,))
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/admin/doacoes/status', methods=['POST'])
def admin_update_doacao_status():
    data = request.json or {}
    did = data.get('id')
    status = data.get('status')
    if not did or not status:
        return jsonify({"success": False, "error": "ID da doação e status são obrigatórios"}), 400
    try:
        run_db_query("UPDATE doacoes SET status = ? WHERE id = ?", (status, did))
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/admin/doacoes', methods=['GET'])
def get_doacoes_admin():
    try:
        doacoes = run_db_query("SELECT * FROM doacoes ORDER BY data_doacao DESC")
        for d in doacoes:
            if 'valor' in d and d['valor'] is not None:
                d['valor'] = float(d['valor'])
            if 'data_doacao' in d and isinstance(d['data_doacao'], datetime.datetime):
                d['data_doacao'] = d['data_doacao'].isoformat()
        return jsonify(doacoes)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/equipe', methods=['GET'])
def get_equipe():
    try:
        members = run_db_query("SELECT * FROM equipe ORDER BY ordem ASC")
        return jsonify(members)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rotas publicas

@app.route('/api/voluntarios', methods=['POST'])
def register_voluntario():
    data = request.json or {}
    nome = data.get('nome')
    email = data.get('email')
    whatsapp = data.get('whatsapp')
    area = data.get('area')
    disp = data.get('disponibilidade')
    msg = data.get('mensagem')
    
    if not nome or not email or not whatsapp:
        return jsonify({"error": "Nome, e-mail e WhatsApp são obrigatórios"}), 400
        
    last_id = run_db_query(
        "INSERT INTO voluntarios (nome, email, whatsapp, area, disponibilidade, mensagem, status) VALUES (?, ?, ?, ?, ?, ?, 'Pendente')",
        (nome, email, whatsapp, area, disp, msg)
    )
    return jsonify({"success": True, "id": last_id})

@app.route('/api/doacoes/mercadopago', methods=['POST'])
def register_doacao_mercadopago():
    data = request.json or {}
    valor = data.get('valor')
    
    if valor is None or float(valor) <= 0:
        return jsonify({"error": "Valor inválido"}), 400
        
    valor = float(valor)
    access_token = os.environ.get("MERCADOPAGO_ACCESS_TOKEN", "[CONFIDENCIAL]")
    
    # 1. Tenta usar a API oficial do Mercado Pago
    try:
        import uuid
        import mercadopago
        
        sdk = mercadopago.SDK(access_token)
        
        payment_data = {
            "transaction_amount": valor,
            "description": "Doacao GAIARB",
            "payment_method_id": "pix",
            "payer": {
                "email": "contato@gaiarb.org",
                "first_name": "Doador",
                "last_name": "GAIARB"
            }
        }
        
        request_options = mercadopago.config.RequestOptions()
        request_options.custom_headers = {
            "X-Idempotency-Key": str(uuid.uuid4())
        }
        
        payment_response = sdk.payment().create(payment_data, request_options)
        
        if payment_response.get("status") in [200, 201]:
            res_json = payment_response.get("response", {})
            poi = res_json.get("point_of_interaction", {})
            tx_data = poi.get("transaction_data", {})
            qr_code = tx_data.get("qr_code")
            qr_code_base64 = tx_data.get("qr_code_base64")
            payment_id = res_json.get("id")
            
            if qr_code:
                # Registra a doacao como pendente no banco
                last_id = run_db_query(
                    "INSERT INTO doacoes (valor, tipo, status) VALUES (?, ?, ?)",
                    (valor, 'PIX', 'Pendente')
                )
                return jsonify({
                    "success": True,
                    "provider": "mercadopago",
                    "payment_id": payment_id,
                    "qr_code": qr_code,
                    "qr_code_base64": qr_code_base64,
                    "db_id": last_id
                })
        else:
            print("Mercado Pago SDK returned status error:", payment_response.get("status"), payment_response.get("response"))
    except Exception as e:
        print("Mercado Pago SDK failed, falling back to local simulation:", e)
                
    # 2. Simulacao local caso a API falhe
    import uuid
    last_id = run_db_query(
        "INSERT INTO doacoes (valor, tipo, status) VALUES (?, ?, ?)",
        (valor, 'PIX', 'Pendente')
    )
    
    unique_tx = str(uuid.uuid4())[:8].upper()
    tag62 = f"62120508{unique_tx}"
    
    amt_str = f"{valor:.2f}"
    amt_len = len(amt_str)
    amt_len_str = f"{amt_len:02d}"
    tag54 = f"54{amt_len_str}{amt_str}"
    
    merchant_info = "0014br.gov.bcb.pix013667c3117b-28f1-4ac2-94a6-c4bc3121807f"
    payload_base = (
        "000201"
        f"26{len(merchant_info):02d}{merchant_info}"
        "52040000"
        "5303986"
        f"{tag54}"
        "5802BR"
        "5906GAIARB"
        "6014RIO DE JANEIRO"
        f"{tag62}"
        "6304"
    )
    
    crc = calculate_crc16(payload_base)
    qr_code = payload_base + crc
    
    return jsonify({
        "success": True,
        "provider": "simulation",
        "message": "Mercado Pago (Homologação Pendente)",
        "qr_code": qr_code,
        "db_id": last_id
    })

@app.route('/api/webhook', methods=['POST'])
@app.route('/webhook', methods=['POST'])
def mercadopago_webhook():
    data = request.json or {}
    topic = data.get('type') or request.args.get('topic')
    payment_id = None
    
    if topic == 'payment':
        payment_id = data.get('data', {}).get('id') or request.args.get('id')
    
    if not payment_id:
        payment_id = data.get('id') or data.get('payment_id') or request.args.get('data.id')
        
    if not payment_id:
        print("Webhook received but no payment_id found in payload:", data, request.args)
        return jsonify({"success": False, "message": "ID do pagamento nao encontrado"}), 400
        
    print(f"Webhook received for payment_id: {payment_id}")
    
    # 1. Suporte a webhook simulado localmente
    if str(payment_id).startswith("simulado-"):
        parts = str(payment_id).split('-')
        if len(parts) >= 3:
            sim_status = parts[1]  # aprovado ou recusado
            sim_amount = float(parts[2])
            db_status = 'Confirmado' if sim_status == 'approved' else 'Cancelado'
            
            rows = run_db_query(
                "SELECT id FROM doacoes WHERE valor = ? AND status = 'Pendente' AND tipo = 'PIX' ORDER BY id DESC LIMIT 1",
                (sim_amount,)
            )
            if rows:
                db_id = rows[0]['id']
                run_db_query("UPDATE doacoes SET status = ? WHERE id = ?", (db_status, db_id))
                return jsonify({"success": True, "message": "[Simulado] Status atualizado", "db_id": db_id, "status": db_status})
            return jsonify({"success": False, "message": "Nenhuma doacao pendente encontrada no valor informado"}), 404
            
    # 2. Consulta o status na API oficial do Mercado Pago
    access_token = os.environ.get("MERCADOPAGO_ACCESS_TOKEN", "[CONFIDENCIAL]")
    try:
        import mercadopago
        sdk = mercadopago.SDK(access_token)
        payment_info_response = sdk.payment().get(int(payment_id))
        
        if payment_info_response.get("status") in [200, 201]:
            payment_info = payment_info_response.get("response", {})
            status = payment_info.get("status")
            amount = payment_info.get("transaction_amount")
            
            db_status = 'Pendente'
            if status == 'approved':
                db_status = 'Confirmado'
            elif status in ['cancelled', 'rejected', 'refunded', 'charged_back']:
                db_status = 'Cancelado'
                
            print(f"Mercado Pago payment status for {payment_id} is: {status} ({db_status}), value: {amount}")
            
            rows = run_db_query(
                "SELECT id FROM doacoes WHERE valor = ? AND status = 'Pendente' AND tipo = 'PIX' ORDER BY id DESC LIMIT 1",
                (amount,)
            )
            if rows:
                db_id = rows[0]['id']
                run_db_query("UPDATE doacoes SET status = ? WHERE id = ?", (db_status, db_id))
                print(f"Database record updated. Donation ID #{db_id} status set to: {db_status}")
                return jsonify({"success": True, "message": "Status atualizado", "db_id": db_id, "status": db_status})
            else:
                print(f"No pending donation with value R$ {amount} found to update.")
                return jsonify({"success": True, "message": "Nenhuma doacao pendente correspondente encontrada"})
        else:
            print("Webhook query to Mercado Pago failed, status code:", payment_info_response.get("status"))
    except Exception as e:
        print("Webhook handling exception:", e)
        
    return jsonify({"success": False, "message": "Erro ao processar notificacao"}), 500

@app.route('/api/doacoes', methods=['POST'])
def register_doacao():
    data = request.json or {}
    valor = data.get('valor')
    tipo = data.get('tipo', 'PIX')
    status = data.get('status', 'Pendente')
    
    if valor is None:
        return jsonify({"error": "Valor é obrigatório"}), 400
        
    last_id = run_db_query(
        "INSERT INTO doacoes (valor, tipo, status) VALUES (?, ?, ?)",
        (valor, tipo, status)
    )
    return jsonify({"success": True, "id": last_id})

# Rotas de administracao

@app.route('/api/voluntarios/<int:vid>', methods=['DELETE'])
def delete_voluntario(vid):
    run_db_query("DELETE FROM voluntarios WHERE id = ?", (vid,))
    return jsonify({"success": True, "message": "Voluntário deletado."})

@app.route('/api/doacoes/<int:did>', methods=['DELETE'])
def delete_doacao(did):
    run_db_query("DELETE FROM doacoes WHERE id = ?", (did,))
    return jsonify({"success": True, "message": "Doação deletada."})

@app.route('/api/equipe', methods=['POST'])
def add_equipe():
    data = request.json or {}
    numero = data.get('numero')
    nome = data.get('nome')
    cargo = data.get('cargo')
    bio = data.get('bio', '')
    ordem = data.get('ordem', 0)
    
    if not nome or not cargo:
        return jsonify({"error": "Nome e cargo são obrigatórios"}), 400
        
    last_id = run_db_query(
        "INSERT INTO equipe (numero, nome, cargo, bio, ordem) VALUES (?, ?, ?, ?, ?)",
        (numero, nome, cargo, bio, ordem)
    )
    return jsonify({"success": True, "id": last_id})

@app.route('/api/equipe/<int:eid>', methods=['DELETE'])
def delete_equipe(eid):
    run_db_query("DELETE FROM equipe WHERE id = ?", (eid,))
    return jsonify({"success": True, "message": "Membro da equipe deletado."})

# Servico de arquivos estaticos
@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory('.', path)

init_db()

if __name__ == '__main__':
    # Executa o servidor na porta 8000
    app.run(host='0.0.0.0', port=8000, debug=True)
