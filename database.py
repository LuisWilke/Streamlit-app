import psycopg2
from psycopg2 import Error

def create_users_table(conn):
    """Cria a tabela de usuários se ela não existir."""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL
            );
        """)
        conn.commit()
        print("Tabela 'users' verificada/criada com sucesso.")
    except Error as e:
        print(f"Erro ao criar tabela 'users': {e}")

def register_user(conn, username, password):
    """Registra um novo usuário no banco de dados."""
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s) RETURNING id;",
                       (username, password))
        user_id = cursor.fetchone()[0]
        conn.commit()
        print(f"Usuário {username} registrado com sucesso com ID: {user_id}")
        return True
    except Error as e:
        print(f"Erro ao registrar usuário: {e}")
        conn.rollback()
        return False

def verify_user(conn, username, password):
    """Verifica as credenciais do usuário."""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s;",
                       (username, password))
        user = cursor.fetchone()
        if user:
            print(f"Usuário {username} verificado com sucesso.")
            return True
        else:
            print(f"Credenciais inválidas para o usuário {username}.")
            return False
    except Error as e:
        print(f"Erro ao verificar usuário: {e}")
        return False

def get_db_connection(db_name, db_user, db_password, db_host, db_port):
    """Estabelece e retorna uma conexão com o banco de dados PostgreSQL."""
    conn = None
    try:
        conn = psycopg2.connect(database=db_name, user=db_user, password=db_password,
                                host=db_host, port=db_port)
        print("Conexão com o PostgreSQL estabelecida com sucesso.")
        return conn
    except Error as e:
        print(f"Erro ao conectar ao PostgreSQL: {e}")
        return None



