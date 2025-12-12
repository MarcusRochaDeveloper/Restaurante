-- 1. Criação do Banco de Dados
CREATE DATABASE IF NOT EXISTS restaurante_db;
USE restaurante_db;

-- 2. Criação das Tabelas

-- Tabela de Usuários
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    senha_hash VARCHAR(255) NOT NULL,
    senha_encriptada VARCHAR(255) NOT NULL,
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Mesas
CREATE TABLE IF NOT EXISTS mesas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero INT NOT NULL UNIQUE,
    capacidade INT DEFAULT 4,
    status ENUM('LIVRE', 'OCUPADA') DEFAULT 'LIVRE'
);

-- Tabela de Cardápio (Com a coluna de imagem)
CREATE TABLE IF NOT EXISTS cardapio (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(255),
    preco FLOAT NOT NULL,
    categoria VARCHAR(50),
    imagem_path VARCHAR(500)
);

-- Tabela de Pedidos
CREATE TABLE IF NOT EXISTS pedidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mesa_id INT,
    usuario_id INT,
    status ENUM('ABERTO', 'FECHADO') DEFAULT 'ABERTO',
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    total FLOAT DEFAULT 0.0,
    FOREIGN KEY (mesa_id) REFERENCES mesas(id) ON DELETE SET NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL
);

-- Tabela de Itens do Pedido
CREATE TABLE IF NOT EXISTS pedido_itens (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pedido_id INT,
    cardapio_id INT,
    quantidade INT NOT NULL,
    preco_unitario FLOAT NOT NULL,
    subtotal FLOAT NOT NULL,
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id) ON DELETE CASCADE,
    FOREIGN KEY (cardapio_id) REFERENCES cardapio(id) ON DELETE CASCADE
);

-- 3. Inserção de Dados Iniciais (Seed)

-- Inserir Usuário Admin (Senha: admin123)
-- OBS: Apenas um modelo separado do banco de dados. 
-- Se não funcionar no seu ambiente, logue com outro ou rode o script python uma vez.
INSERT INTO usuarios (nome, email, senha_hash, senha_encriptada) 
VALUES (
    'Administrador', 
    'admin@restaurante.com', 
    '$2b$12$ExampleHashForAdmin123......................', 
    'gAAAAABExampleEncryptedPassword=='
);

-- Inserir Mesas 
INSERT INTO mesas (numero, capacidade) VALUES 
(1, 4), (2, 6), (3, 4), (4, 6), (5, 4), (6, 6),
(7, 4), (8, 6), (9, 4), (10, 6), (11, 4), (12, 6);

-- Inserir Cardápio
INSERT INTO cardapio (nome, descricao, categoria, preco) VALUES 
('Pizza Margherita', 'Molho de tomate, mussarela e manjericão fresco.', 'Pizza', 45.90),
('Pizza Calabresa', 'Molho especial, mussarela, calabresa e cebola roxa.', 'Pizza', 48.90),
('Hambúrguer Clássico', 'Pão brioche, carne 180g, queijo cheddar e salada.', 'Lanche', 28.90),
('X-Bacon Artesanal', 'Pão australiano, carne, bacon crocante e molho barbecue.', 'Lanche', 32.90),
('Refrigerante Lata', 'Coca-Cola, Guaraná ou Fanta (350ml).', 'Bebida', 6.00),
('Suco Natural', 'Laranja, limão ou maracujá (500ml).', 'Bebida', 8.50),
('Batata Frita Rústica', 'Porção grande com alho e alecrim.', 'Acompanhamento', 18.90),
('Salada Caesar', 'Alface americana, croutons, parmesão e molho caesar.', 'Prato', 22.90),
('Petit Gâteau', 'Bolo de chocolate com sorvete de creme.', 'Sobremesa', 19.90);