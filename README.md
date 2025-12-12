# 🍽️ Nexora | Enterprise ERP

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-007BFF?style=for-the-badge)
![SQLAlchemy](https://img.shields.io/badge/ORM-SQLAlchemy-red?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Stable-success?style=for-the-badge)

> Um sistema de gestão corporativa (ERP) para restaurantes, focado em **UI/UX moderna**, alta performance e segurança de dados.

---

## 🖼️ Visão Geral

O **Restaurante Pro** não é apenas um gerenciador de pedidos; é uma solução completa de **Floor Plan & Order Management**. Desenvolvido para substituir planilhas e sistemas legados com uma interface **Dark Mode** imersiva, responsiva e intuitiva.

O projeto utiliza a biblioteca `CustomTkinter` para entregar uma experiência visual comparável a aplicações web modernas (React/Vue), mas com a performance nativa do Desktop.

---

## ✨ Funcionalidades Principais

### 🏢 Dashboard & Navegação
- **Sidebar Dinâmica:** Menu retrátil com indicadores visuais de estado ativo.
- **KPIs em Tempo Real:** Monitoramento instantâneo de mesas ocupadas, livres e total de capacidade.
- **Perfil de Usuário:** Gestão de sessão com avatar gerado dinamicamente e controle de acesso (RBAC simples).

### 🪑 Gestão de Salão (Floor Plan)
- **Visualização Gráfica:** Mesas representadas como objetos visuais, não apenas listas.
- **Status Color-Coded:** Feedback visual imediato (Verde = Livre, Vermelho = Ocupada).
- **CRUD Completo:** Adicione, edite ou remova mesas com modais integrados.

### 🍔 Cardápio Digital
- **Upload de Imagens:** Suporte para adicionar fotos reais aos produtos (armazenamento local).
- **Categorização:** Organização por tags (Bebidas, Lanches, Pratos).
- **Precificação Inteligente:** Formatação automática de moeda e validação de inputs.

### 📝 Controle de Pedidos
- **Fluxo de Venda:** Abertura de mesas, adição de itens e fechamento de conta.
- **Cálculo Automático:** Totais e subtotais calculados em tempo real pelo ORM.

### 🔐 Segurança Enterprise
- **Criptografia:** Senhas salvas com hash `bcrypt`.
- **Proteção de Dados:** Dados sensíveis trafegam criptografados internamente.
- **Login Seguro:** Validação robusta com tratamento de erros e proteção contra SQL Injection via ORM.



## 🛠️ Tech Stack

- **Linguagem:** [Python 3.10+](https://www.python.org/)
- **Interface Gráfica:** [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) (Modern UI)
- **Banco de Dados:** [SQLAlchemy](https://www.sqlalchemy.org/) (ORM) com suporte a **MySQL** e **SQLite**.
- **Segurança:** `bcrypt` (Hashing) e `cryptography` (Fernet).
- **Manipulação de Imagem:** [Pillow (PIL)](https://python-pillow.org/).

---

## 🚀 Instalação e Execução

Siga os passos abaixo para rodar o projeto localmente.

### 1. Clone o repositório
```bash
git clone [https://github.com/MarcusRochaDeveloper/Restaurante.git](https://github.com/MarcusRochaDeveloper/Restaurante.git)
cd Restaurante

# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
