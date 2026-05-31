import mysql.connector
import hashlib
import getpass

def add_new_admin():
    print("==============================================")
    print("   CADASTRAR NOVO ADMINISTRADOR DO GAIARB")
    print("==============================================")
    
    # Dados de conexao com o banco
    host = input("Host do banco (Aiven): ").strip()
    port = input("Porta do banco (Aiven) [ex: 26073]: ").strip()
    user = input("Usuário (padrão: avnadmin): ").strip() or "avnadmin"
    password = input("Senha do banco (Aiven): ").strip()
    database = input("Nome do banco (padrão: defaultdb): ").strip() or "defaultdb"
    
    # Dados do novo administrador
    new_user = input("\nNome de usuário para login (ex: joao): ").strip()
    new_name = input("Nome completo do novo admin (ex: João Silva): ").strip()
    new_pass = input("Senha do novo administrador: ").strip()
    
    if not new_user or not new_name or not new_pass:
        print("\nErro: Todos os campos do novo administrador são obrigatórios!")
        return
 
    # Calcula o hash SHA256 da senha
    pwd_hash = hashlib.sha256(new_pass.encode('utf-8')).hexdigest()
    
    print("\nConectando ao banco de dados e cadastrando...")
    try:
        conn = mysql.connector.connect(
            host=host,
            port=int(port),
            user=user,
            password=password,
            database=database
        )
        cursor = conn.cursor()
        
        # Insere o novo admin na tabela
        cursor.execute(
            "INSERT INTO admins (username, password_hash, nome) VALUES (%s, %s, %s)",
            (new_user, pwd_hash, new_name)
        )
        conn.commit()
        print(f"\n[SUCESSO] O administrador '{new_name}' (usuário de login: '{new_user}') foi cadastrado com sucesso!")
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"\n[ERRO] Falha ao conectar ou salvar no banco de dados: {e}")

if __name__ == "__main__":
    add_new_admin()
