-- ═══════════════════════════════════════════════
-- GAIARB – DATABASE SCHEMA & SEED DATA
-- ═══════════════════════════════════════════════

-- 1. ADMINS TABLE (For managing the dashboard)
CREATE TABLE IF NOT EXISTS admins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    nome VARCHAR(100) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2. VOLUNTARIOS TABLE (For storing volunteer form applications)
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
);

-- 3. DOACOES TABLE (For logging generated donations)
CREATE TABLE IF NOT EXISTS doacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    valor DECIMAL(10,2) NOT NULL,
    data_doacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    tipo VARCHAR(20) DEFAULT 'PIX',
    status VARCHAR(20) DEFAULT 'Pendente'
);

-- 4. EQUIPE TABLE (For storing team members dynamically)
CREATE TABLE IF NOT EXISTS equipe (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero VARCHAR(10),
    nome VARCHAR(100) NOT NULL,
    cargo VARCHAR(100) NOT NULL,
    bio TEXT,
    ordem INTEGER DEFAULT 0
);


-- ═══════════════════════════════════════════════
-- SEED DATA
-- ═══════════════════════════════════════════════

-- Seed Admin User (Username: admin, Password: admin123, Hash: SHA-256)
INSERT OR IGNORE INTO admins (id, username, password_hash, nome) 
VALUES (1, 'admin', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'Administrador GAIARB');

-- Seed Team Members (Without photo field)
INSERT OR IGNORE INTO equipe (id, numero, nome, cargo, bio, ordem) VALUES
(1, '01', 'Ayla de Cássia Franco Bragança', 'Presidente(a)', 'Fundadora do GAIARB, dedicou sua vida ao acolhimento. Lidera o projeto com amor e determinação.', 1),
(2, '02', 'Daniele dos Santos Charré Duarte', 'Vice-Presidente(a)', 'Bio dela', 2),
(3, '03', 'Danielle de Moraes Góis Diniz', 'Tesoureiro(a)', 'Bio dela', 3),
(4, '04', 'Alan Macedo Santos', 'Tesoureiro Adjunto', 'Bio dele', 4),
(5, '05', 'Renata Maçulo Quintanilha Pimentel', 'Secretário(a)', 'Bio dela', 5),
(6, '06', 'Letícia da Silva Moreira Franco', 'Secretário Adjunto(a)', 'Bio dela', 6);
