# Broca_AI - Sistema de Detecção e Quantificação da Broca

Plataforma em Python via Streamlit para identificação e quantificação da praga da broca em seu estado adulto através de imagens.

## Funcionalidades

- **Detecção de Pragas**: Upload e análise de imagens para identificação da broca em estado adulto
- **Quantificação**: Contagem automática do número de brocas detectadas
- **Gerenciamento de Dados**: Interface para visualização e análise dos registros de detecção
- **Controle de Acesso**: Sistema de login para proteger os dados e separar funções de usuário e administrador

## Instalação

1. Clone este repositório
2. Instale as dependências: `pip install -r requirements.txt`
3. Execute a aplicação: `streamlit run app.py`

## Credenciais Padrão

- **Usuário**: admin
- **Senha**: admin123

## Estrutura do Projeto

- `app.py`: Aplicação principal
- `requirements.txt`: Dependências do projeto
- `uploads/`: Diretório onde as imagens são armazenadas
- `users.pkl`: Banco de dados de usuários
- `records.pkl`: Banco de dados de registros