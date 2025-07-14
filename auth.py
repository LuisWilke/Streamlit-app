import streamlit as st
import hashlib
from database import get_db_connection, create_users_table, register_user, verify_user

def hash_password(password):
    """Cria um hash da senha usando SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def show_login_page():
    """Exibe a página de login."""
    st.markdown('<h1 class="main-header">🔐 Login</h1>', unsafe_allow_html=True)
    
    with st.form("login_form"):
        st.subheader("Entre com suas credenciais")
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        
        col1, col2 = st.columns(2)
        with col1:
            login_button = st.form_submit_button("🚀 Entrar", type="primary")
        with col2:
            register_button = st.form_submit_button("📝 Registrar-se")
        
        if login_button:
            if username and password:
                # Conectar ao banco de dados
                conn = get_db_connection(
                    st.session_state.get('db_name', 'postgres'),
                    st.session_state.get('db_user', 'postgres'),
                    st.session_state.get('db_password', ''),
                    st.session_state.get('db_host', 'localhost'),
                    st.session_state.get('db_port', '5432')
                )
                
                if conn:
                    hashed_password = hash_password(password)
                    if verify_user(conn, username, hashed_password):
                        st.session_state.authenticated = True
                        st.session_state.username = username
                        st.success("Login realizado com sucesso!")
                        st.rerun()
                    else:
                        st.error("Usuário ou senha incorretos!")
                    conn.close()
                else:
                    st.error("Erro ao conectar com o banco de dados!")
            else:
                st.error("Por favor, preencha todos os campos!")
        
        if register_button:
            st.session_state.show_register = True
            st.rerun()

def show_register_page():
    """Exibe a página de registro."""
    st.markdown('<h1 class="main-header">📝 Registro</h1>', unsafe_allow_html=True)
    
    with st.form("register_form"):
        st.subheader("Crie sua conta")
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        confirm_password = st.text_input("Confirmar Senha", type="password")
        
        col1, col2 = st.columns(2)
        with col1:
            register_button = st.form_submit_button("✅ Registrar", type="primary")
        with col2:
            back_button = st.form_submit_button("⬅️ Voltar ao Login")
        
        if register_button:
            if username and password and confirm_password:
                if password == confirm_password:
                    # Conectar ao banco de dados
                    conn = get_db_connection(
                        st.session_state.get('db_name', 'postgres'),
                        st.session_state.get('db_user', 'postgres'),
                        st.session_state.get('db_password', ''),
                        st.session_state.get('db_host', 'localhost'),
                        st.session_state.get('db_port', '5432')
                    )
                    
                    if conn:
                        create_users_table(conn)
                        hashed_password = hash_password(password)
                        if register_user(conn, username, hashed_password):
                            st.success("Usuário registrado com sucesso! Faça login agora.")
                            st.session_state.show_register = False
                            st.rerun()
                        else:
                            st.error("Erro ao registrar usuário. Usuário pode já existir.")
                        conn.close()
                    else:
                        st.error("Erro ao conectar com o banco de dados!")
                else:
                    st.error("As senhas não coincidem!")
            else:
                st.error("Por favor, preencha todos os campos!")
        
        if back_button:
            st.session_state.show_register = False
            st.rerun()

def show_database_config():
    """Exibe a configuração do banco de dados."""
    st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.sidebar.header("🗄️ Configuração PostgreSQL")
    
    st.session_state.db_host = st.sidebar.text_input("Host", value=st.session_state.get('db_host', 'localhost'))
    st.session_state.db_port = st.sidebar.text_input("Porta", value=st.session_state.get('db_port', '5432'))
    st.session_state.db_name = st.sidebar.text_input("Nome do Banco", value=st.session_state.get('db_name', 'postgres'))
    st.session_state.db_user = st.sidebar.text_input("Usuário", value=st.session_state.get('db_user', 'postgres'))
    st.session_state.db_password = st.sidebar.text_input("Senha", type="password", value=st.session_state.get('db_password', ''))
    
    if st.sidebar.button("🔧 Testar Conexão"):
        conn = get_db_connection(
            st.session_state.db_name,
            st.session_state.db_user,
            st.session_state.db_password,
            st.session_state.db_host,
            st.session_state.db_port
        )
        if conn:
            st.sidebar.success("✅ Conexão bem-sucedida!")
            conn.close()
        else:
            st.sidebar.error("❌ Falha na conexão!")
    
    st.sidebar.markdown('</div>', unsafe_allow_html=True)

def logout():
    """Realiza o logout do usuário."""
    st.session_state.authenticated = False
    st.session_state.username = None
    st.rerun()

def check_authentication():
    """Verifica se o usuário está autenticado."""
    return st.session_state.get('authenticated', False)

def get_current_user():
    """Retorna o usuário atual."""
    return st.session_state.get('username', None)

