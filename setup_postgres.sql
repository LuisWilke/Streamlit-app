-- Script de configuração inicial para PostgreSQL
-- Execute este script para preparar o banco de dados para o sistema de autenticação

-- 1. Criar banco de dados (execute como superusuário)
-- CREATE DATABASE dashboard_vendas;

-- 2. Criar usuário específico para a aplicação (opcional, mas recomendado)
-- CREATE USER dashboard_user WITH PASSWORD 'sua_senha_aqui';

-- 3. Conceder permissões ao usuário
-- GRANT ALL PRIVILEGES ON DATABASE dashboard_vendas TO dashboard_user;

-- 4. Conectar ao banco dashboard_vendas e executar os comandos abaixo:

-- Criar tabela de usuários
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

-- Criar índice para melhor performance nas consultas de login
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);

-- Inserir usuário administrador padrão (opcional)
-- Senha: admin123 (hash SHA-256)
INSERT INTO users (username, password) 
VALUES ('admin', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9')
ON CONFLICT (username) DO NOTHING;

-- Verificar se a tabela foi criada corretamente
SELECT 
    table_name, 
    column_name, 
    data_type, 
    is_nullable
FROM information_schema.columns 
WHERE table_name = 'users'
ORDER BY ordinal_position;

-- Verificar usuários existentes
SELECT id, username, created_at FROM users;

