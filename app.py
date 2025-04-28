import streamlit as st
import pandas as pd
import numpy as np
import os
import pickle
import datetime
import hashlib
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import io
import base64
import uuid
import json
import time
import random

# Configuração da página
st.set_page_config(
    page_title="Broca AI - Detecção de Pragas",
    page_icon="🦋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Aplicar CSS personalizado para os botões da sidebar
st.markdown("""
<style>
    /* Cor de fundo principal */
    .stApp {
        background-color: white;
    }
    
    /* Cor de texto principal */
    .stApp, p, div {
        color: #111111;
    }
    
    /* Cor da sidebar - cinza claro */
    [data-testid="stSidebar"] {
        background-color: #f2f2f2 !important;
    }
    
    /* Manter a cor padrão dos botões em toda a aplicação */
    /* Não adicionar nenhuma regra aqui para manter o azul marinho padrão */
    
    /* Botões de navegação da sidebar com estilo verde */
    div[data-testid="stSidebar"] button {
        background-color: #76B82A !important;
        color: white !important;
        border: none !important;
        transition: all 0.3s ease !important;
    }
    
    /* Efeito hover para os botões da sidebar */
    div[data-testid="stSidebar"] button:hover {
        background-color: #f2f2f2 !important;
        color: #76B82A !important;
        border: 2px solid #76B82A !important;
    }
    
    /* Estilos para botões da sidebar */
    .stSidebar .stButton>button {
        margin-bottom: 5px !important; /* Reduzir espaçamento entre botões */
        padding: 0.25rem 1rem !important; /* Reduzir o padding interno dos botões */
    }
    
    /* Estilos para todos os botões na sidebar */
    div[data-testid="stSidebar"] [data-testid="stButton"] button {
        margin-bottom: 5px !important;
        padding: 0.25rem 1rem !important;
        border-radius: 4px !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        transition: all 0.2s ease !important;
    }
    
    /* Botão primary (verde) */
    div[data-testid="stSidebar"] button[kind="primary"] {
        background-color: #76B82A !important;
        color: white !important;
        border: none !important;
        box-shadow: none !important;
    }
    
    /* Botão secondary (cinza com borda verde) */
    div[data-testid="stSidebar"] button[kind="secondary"] {
        background-color: #f2f2f2 !important;
        color: #76B82A !important;
        border: 2px solid #76B82A !important;
        box-shadow: none !important;
    }
    
    /* Garantir que o hover não mude as cores */
    div[data-testid="stSidebar"] button[kind="primary"]:hover {
        background-color: #68a526 !important;
        color: white !important;
        border: none !important;
    }
    
    div[data-testid="stSidebar"] button[kind="secondary"]:hover {
        background-color: #e8e8e8 !important;
        color: #68a526 !important;
        border: 2px solid #68a526 !important;
    }
    
    /* Garantir que todos os botões da sidebar tenham o espaçamento correto */
    .stSidebar [data-testid="stButton"] button {
        margin-bottom: 5px !important;
        padding: 0.25rem 1rem !important;
    }
    
    /* Efeito hover para os botões da sidebar */
    .stSidebar .stButton>button:hover {
        opacity: 0.9 !important;
    }
    
    /* Botão de logout com estilo personalizado */
    div[data-testid="stSidebar"] [data-testid="stButton"][key="logout_btn"] button {
        background-color: white !important;
        color: #d32f2f !important; /* Vermelho */
        border: 2px solid #d32f2f !important;
        transition: all 0.3s ease !important;
        font-size: 13px !important;
        padding: 0.2rem 1rem !important;
        margin-top: 5px !important;
        margin-bottom: 5px !important;
        border-radius: 4px !important;
        font-weight: 500 !important;
        box-shadow: none !important;
        min-width: 80px !important;
    }
    
    /* Efeito hover para o botão de logout */
    div[data-testid="stSidebar"] [data-testid="stButton"][key="logout_btn"] button:hover {
        background-color: #ffebee !important; /* Vermelho muito claro */
        color: #b71c1c !important; /* Vermelho escuro */
        border: 2px solid #b71c1c !important;
    }
    
    /* Centralizar o botão de logout */
    div[data-testid="stSidebar"] [data-testid="stButton"][key="logout_btn"] {
        display: flex !important;
        justify-content: center !important;
        margin: 0 auto !important;
        width: 100% !important;
        text-align: center !important;
    }
    
    /* Garantir que o botão de logout esteja centralizado */
    div[data-testid="stSidebar"] [data-testid="stButton"][key="logout_btn"] button {
        margin-left: auto !important;
        margin-right: auto !important;
    }
    
    /* Garantir que todos os textos sejam pretos */
    .stApp, .stMarkdown, p, h1, h2, h3, h4, h5, h6, li, span, div {
        color: #111111 !important;
    }
    
    /* Exceções para textos que precisam ser brancos (botões, tabs selecionadas) */
    .stButton>button, .stTabs [aria-selected="true"] {
        color: white !important;
    }
    
    /* Garantir que os botões da sidebar tenham prioridade no estilo */
    div[data-testid="stSidebar"] .stButton>button {
        background-color: #f2f2f2 !important;
        color: #76B82A !important;
        border: 2px solid #76B82A !important;
        transition: all 0.3s ease !important;
    }
    
    /* Estilo para os botões selecionados com maior prioridade */
    div[data-testid="stSidebar"] .stButton>button.selected,
    div[data-testid="stSidebar"] [data-testid="stButton"] button.selected {
        background-color: #76B82A !important;
        color: white !important;
        border: none !important;
    }
    
    /* Garantir que o efeito hover tenha prioridade */
    div[data-testid="stSidebar"] .stButton>button:hover {
        opacity: 0.9 !important;
    }
    
    /* Estilo das tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 16px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6; /* Cinza claro */
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-left: 20px;
        padding-right: 20px;
        color: #111111 !important;
        transition: all 0.3s ease;
        font-weight: 500;
        border: 1px solid transparent;
    }
    .stTabs [aria-selected="true"] {
        background-color:rgb(220, 240, 197) !important; /* Verde claro principal */
        color: #2E7D32 !important; /* Verde escuro para melhor contraste */
        border-bottom: 2px solid #76B82A;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Efeito hover para as abas não selecionadas */
    .stTabs [data-baseweb="tab"]:not([aria-selected="true"]):hover {
        background-color: #e8e8e8;
        border-bottom: 1px solid #76B82A;
    }
    
    /* Estilo dos links na sidebar */
    div[data-testid="stSidebarNav"] li div a {
        margin-left: 1rem;
        padding: 1rem;
        width: 300px;
        border-radius: 0.5rem;
        color: #111111 !important;
    }
    div[data-testid="stSidebarNav"] li div::focus-visible {
    }
    
    /* Ajustes de espaçamento */
    .reportview-container .main .block-container {
        padding-top: 2rem;
    }
    .css-1544g2n.e1fqkh3o4 {
        padding-top: 2rem;
    }
    
    /* Garantir que os cards e containers tenham fundo branco e texto preto */
    .stExpander, .stContainer {
        background-color: white;
    }
    
    /* Ajustar cores dos alertas e mensagens */
    .stAlert {
        background-color: #f8f9fa;
        color: #111111 !important;
    }
    .stAlert > div {
        color: #111111 !important;
    }
    
    /* Garantir que os inputs tenham texto visível */
    .stTextInput input, .stTextArea textarea, .stSelectbox select {
        color: #111111 !important;
    }
    
    /* Caixas em cinza muito claro */
    div[style*="background-color: #f0f2f6"], 
    .stExpander, 
    .stContainer,
    div[data-baseweb="tab"],
    div[data-testid="stForm"],
    div[data-baseweb="card"],
    div[class*="stBlock"] {
        background-color: #f9f9f9 !important; /* Cinza muito claro */
    }
    
    /* Garantir que todas as caixas com estilo inline também sejam claras */
    [style*="background-color: #f0f2f6"],
    [style*="background-color: #f5f5f5"] {
        background-color: #f9f9f9 !important;
    }
</style>
""", unsafe_allow_html=True)

# Função para carregar ou criar o banco de dados de usuários
def load_users():
    if os.path.exists("users.pkl"):
        with open("users.pkl", "rb") as f:
            return pickle.load(f)
    else:
        # Criar usuário admin padrão
        default_users = {
            "admin": {
                "password": hashlib.sha256("123".encode()).hexdigest(),
                "role": "admin"
            }
        }
        with open("users.pkl", "wb") as f:
            pickle.dump(default_users, f)
        return default_users

# Função para carregar ou criar o banco de dados de registros
def load_records():
    if os.path.exists("records.pkl"):
        with open("records.pkl", "rb") as f:
            return pickle.load(f)
    else:
        return []

# Função para salvar registros
def save_records(records):
    with open("records.pkl", "wb") as f:
        pickle.dump(records, f)

# Função para salvar usuários
def save_users(users):
    with open("users.pkl", "wb") as f:
        pickle.dump(users, f)

# Função para autenticar usuário
def authenticate(username, password):
    users = load_users()
    if username in users and users[username]["password"] == hashlib.sha256(password.encode()).hexdigest():
        st.session_state.authenticated = True
        st.session_state.username = username
        st.session_state.role = users[username]["role"]
        st.session_state.current_page = "registrar"  # Definir página inicial como "registrar"
        st.session_state.selected_button = "registrar"  # Definir botão selecionado como "registrar"
        return True
    return False

# Função para processar a imagem e detectar a broca
def detect_broca(image):
    """Detecta e quantifica a broca em seu estado adulto na imagem.
    
    Args:
        image: Imagem PIL para processamento
        
    Returns:
        count: Número de brocas detectadas
        result_pil: Imagem processada com as brocas destacadas
        detection_data: Dados detalhados sobre as detecções (posição, tamanho, etc)
    """
    # Em um ambiente de produção, aqui seria implementado um modelo de IA real para detecção
    # Como não temos o OpenCV disponível, vamos simular a detecção
    
    # Criar uma cópia da imagem para processamento
    img_copy = image.copy()
    
    # Converter para escala de cinza
    gray_img = img_copy.convert('L')
    
    # Aplicar filtro para destacar bordas
    edge_img = gray_img.filter(ImageFilter.FIND_EDGES)
    
    # Aumentar o contraste
    enhancer = ImageEnhance.Contrast(edge_img)
    enhanced_img = enhancer.enhance(2.0)
    
    # Criar uma imagem para desenhar os resultados
    result_img = img_copy.copy()
    draw = ImageDraw.Draw(result_img)
    
    # Simular a detecção de brocas (número aleatório entre 1 e 5)
    # Em um caso real, isso seria feito por um modelo de IA treinado
    width, height = img_copy.size
    num_detections = random.randint(1, 5)
    detection_data = []
    
    for i in range(num_detections):
        # Gerar coordenadas aleatórias para simular detecções
        x = random.randint(50, width - 100)
        y = random.randint(50, height - 100)
        w = random.randint(30, 80)
        h = random.randint(30, 80)
        
        # Calcular a confiança (simulada)
        confidence = random.uniform(0.6, 0.95)
        
        # Armazenar dados da detecção
        detection_data.append({
            "id": i + 1,
            "x": x,
            "y": y,
            "width": w,
            "height": h,
            "area": float(w * h),
            "confidence": float(confidence),
            "aspect_ratio": float(w) / h
        })
        
        # Cor baseada na confiança
        if confidence > 0.8:
            color = "green"  # Verde para alta confiança
        elif confidence > 0.6:
            color = "yellow"  # Amarelo para média confiança
        else:
            color = "red"  # Vermelho para baixa confiança
        
        # Desenhar retângulo
        draw.rectangle([x, y, x+w, y+h], outline=color, width=2)
        
        # Adicionar texto com ID e confiança
        draw.text((x, y-15), f"#{i+1}: {confidence:.2f}", fill=color)
    
    return num_detections, result_img, detection_data

# Função para salvar a imagem processada
def save_image(image, filename):
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    image.save(f"uploads/{filename}")
    return f"uploads/{filename}"

# Inicializar estado da sessão
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.username = None
    st.session_state.role = None
    st.session_state.current_page = "login"
    st.session_state.users = load_users()
    st.session_state.records = load_records()
    st.session_state.last_refresh = time.time()
    st.session_state.detection_data = None
    st.session_state.filtered_records = None
    st.session_state.show_details = False
    st.session_state.edit_mode = False
    st.session_state.camera_active = False  # Estado para controlar a ativação da câmera

# Garantir que a variável selected_button esteja sempre inicializada
if 'selected_button' not in st.session_state:
    st.session_state.selected_button = "registrar"  # Botão "Registrar" selecionado por padrão

# Garantir que a página atual seja consistente com o botão selecionado
if 'authenticated' in st.session_state and st.session_state.authenticated:
    if st.session_state.current_page != st.session_state.selected_button:
        st.session_state.current_page = st.session_state.selected_button

# Função para fazer logout
def logout():
    st.session_state.authenticated = False
    st.session_state.username = None
    st.session_state.role = None
    st.session_state.current_page = "login"

# Função para mostrar a sidebar
def show_sidebar():
    with st.sidebar:
        # Adicionar espaço em branco no topo (reduzido)
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        
        # Criar colunas para centralizar a logo com espaçamento lateral
        col1, col2, col3 = st.columns([1, 3, 1])
        
        with col2:
            # Exibir o logo da Cocal em tamanho reduzido, mantendo proporções
            logo_path = os.path.join("imagens", "logo-cocal.png")
            if os.path.exists(logo_path):
                # Carregar a imagem para redimensionar
                img = Image.open(logo_path)
                # Calcular a largura desejada (60% do tamanho original)
                width, height = img.size
                new_width = int(width * 0.6)
                # Calcular a nova altura mantendo a proporção
                new_height = int(height * (new_width / width))
                # Redimensionar a imagem
                img_resized = img.resize((new_width, new_height), Image.LANCZOS)
                # Exibir a imagem redimensionada
                st.image(img_resized, use_container_width=False)
            else:
                st.warning("Logo não encontrada")
        
        # Adicionar espaço em branco após a logo (reduzido)
        st.markdown("<div style='height: 5px;'></div>", unsafe_allow_html=True)
        
        # Título da aplicação
        st.markdown(f"<h3 style='text-align: center; color: #76B82A; margin-bottom: 5px;'>Broca AI</h3>", unsafe_allow_html=True)
        
        if st.session_state.authenticated:
            # Espaço reduzido
            st.markdown("<div style='height: 5px;'></div>", unsafe_allow_html=True)
            # Separador mais fino
            st.markdown("<hr style='margin: 5px 0; border: 0; border-top: 1px solid #e0e0e0;'>", unsafe_allow_html=True)
            
            # Menu de navegação mais compacto
            st.markdown("<p style='margin-bottom: 5px; font-weight: bold; color: #555;'></p>", unsafe_allow_html=True)
            
            menu_options = ["Registrar"]
            if st.session_state.role == "admin":
                menu_options.append("Gerenciamento")
            
            # Garantir que selected_button esteja inicializado
            if 'selected_button' not in st.session_state:
                st.session_state.selected_button = "registrar"
        
            # Menu de navegação com botões
            for option in menu_options:
                # Verificar se o botão está selecionado
                is_selected = st.session_state.selected_button == option.lower()
                
                # Nenhum CSS adicional necessário, usaremos os tipos de botões nativos do Streamlit
                
                # Botão do Streamlit com estilo direto
                if is_selected:
                    # Botão selecionado - verde
                    button = st.sidebar.button(
                        option, 
                        key=f"btn_{option.lower()}", 
                        use_container_width=True,
                        type="primary"  # Usar o tipo primary para o botão selecionado
                    )
                else:
                    # Botão não selecionado - cinza com borda verde
                    button = st.sidebar.button(
                        option, 
                        key=f"btn_{option.lower()}", 
                        use_container_width=True,
                        type="secondary"  # Usar o tipo secondary para o botão não selecionado
                    )
                
                # Processar o clique no botão
                if button:
                    st.session_state.current_page = option.lower()
                    st.session_state.selected_button = option.lower()  # Atualizar o botão selecionado
                    # Limpar dados temporários ao mudar de página
                    if 'current_record' in st.session_state:
                        del st.session_state.current_record
                    st.session_state.show_details = False
                    st.session_state.edit_mode = False
                    st.rerun()
            
            # Separador mais fino
            st.markdown("<hr style='margin: 10px 0; border: 0; border-top: 1px solid #e0e0e0;'>", unsafe_allow_html=True)
            
            # Adicionar espaço antes do botão de logout
            st.markdown("<div style='height: 5px;'></div>", unsafe_allow_html=True)
            
            # # Criar colunas para centralizar o botão
            # col1, col2, col3 = st.columns([1, 1, 1])
            # with col2:
            #     # Botão de logout menor e com borda vermelha
            #     if st.button("Sair", key="logout_btn", use_container_width=False):
            #         logout()
            #         st.rerun()
        # else:
        #     st.info("Faça login para acessar o sistema")

# CSS personalizado para os inputs na tela de login
login_input_style = """
<style>
    /* Estilo para os campos de entrada na tela de login */
    div[data-testid="stTextInput"] input {
        background-color: #f2f2f2 !important;
        color: #333333 !important;
        border-color: #e0e0e0 !important;
    }
    
    /* Remover o fundo cinza dos labels */
    div[data-testid="stTextInput"] label {
        background-color: transparent !important;
    }
    
    /* Centralizar o botão de login */
    div[data-testid="column"] [data-testid="stButton"] {
        display: flex !important;
        justify-content: center !important;
    }
    
    /* Estilo específico para o botão de login */
    /* Usar seletores mais específicos para garantir que o estilo seja aplicado */
    div[data-testid="column"] [data-testid="stButton"] button,
    .main button[kind="primary"],
    .main button[kind="secondary"],
    .main button {
        background-color: #76B82A !important;
        color: white !important;
        border: none !important;
        font-weight: 500 !important;
        box-shadow: none !important;
        transition: all 0.3s ease !important;
    }
    
    /* Efeito hover para o botão de login */
    div[data-testid="column"] [data-testid="stButton"] button:hover,
    .main button:hover {
        background-color: #68a526 !important;
        color: white !important;
    }
    
    /* Remover qualquer estilo do tema que possa interferir */
    .stApp button[data-testid="baseButton-primary"] {
        background-color: #76B82A !important;
        color: white !important;
    }
    
    /* Seletor super específico para o botão de login usando sua chave */
    button[kind="secondary"][data-testid="baseButton-secondary"],
    [data-testid="stButton"][key="login_button"] button,
    button[data-baseweb="button"] {
        background-color: #76B82A !important;
        color: white !important;
        border: none !important;
    }
</style>
"""

# Página de login
if not st.session_state.authenticated:
    # Aplicar estilo personalizado aos inputs
    st.markdown(login_input_style, unsafe_allow_html=True)
    
    # Criar um container principal para centralizar todo o conteúdo
    with st.container():
        # Logo da Cocal centralizada com tamanho fixo
        logo_col1, logo_col2, logo_col3 = st.columns([1, 1, 1])
        with logo_col2:
            logo_path = os.path.join("imagens", "logo-cocal.png")
            if os.path.exists(logo_path):
                # Usar HTML direto para controlar o tamanho da imagem
                img = Image.open(logo_path)
                buffered = io.BytesIO()
                img.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode()
                
                # Definir um tamanho fixo em pixels para a logo
                st.markdown(f"""
                <div style="display: flex; justify-content: center;">
                    <img src="data:image/png;base64,{img_str}" width="180px">
                </div>
                """, unsafe_allow_html=True)
    
    # Container centralizado para o login
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        st.markdown("<h1 style='text-align: center; color: #76B82A;'>Broca AI</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 1.2em;'>Sistema de detecção e quantificação da broca</p>", unsafe_allow_html=True)
        
        # Espaço entre o título e os campos de login (reduzido)
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        
        # Campos de login sem a caixa
        username = st.text_input("Usuário", key="login_username")
        password = st.text_input("Senha", type="password", key="login_password")
        
        # Botão de login centralizado
        login_col1, login_col2, login_col3 = st.columns([1, 1.5, 1])
        
        with login_col2:
            # Usar markdown com HTML para criar um botão personalizado com estilo inline
            login_button_html = '''
            <button type="button" id="custom_login_button" 
                style="
                    background-color: #76B82A; 
                    color: white; 
                    border: none; 
                    border-radius: 4px; 
                    padding: 0.5rem 1rem; 
                    font-size: 1rem; 
                    font-weight: 500; 
                    cursor: pointer; 
                    width: 100%;
                    transition: background-color 0.3s ease;"
                onmouseover="this.style.backgroundColor='#68a526'" 
                onmouseout="this.style.backgroundColor='#76B82A'"
            >
                Login
            </button>
            <script>
                document.getElementById("custom_login_button").addEventListener("click", function() {
                    // Simular clique no botão escondido do Streamlit
                    document.querySelector('button[data-testid="baseButton-secondary"]').click();
                });
            </script>
            '''
            
            # Botão escondido do Streamlit para manter a funcionalidade
            login_clicked = st.button("Login", use_container_width=True, key="login_button", label_visibility="collapsed")
            
            # Exibir o botão personalizado
            st.markdown(login_button_html, unsafe_allow_html=True)
            
            # Verificar se o botão foi clicado
            if login_clicked:
                if not username or not password:
                    st.error("Preencha os campos!")
                else:
                    # A função authenticate configura diretamente as variáveis de sessão
                    auth_success = authenticate(username, password)
                    if auth_success:
                        # A função authenticate já configurou as variáveis de sessão
                        st.rerun()
                    else:
                        st.error("Usuário ou senha incorretos")

# Página de registro de imagens
elif st.session_state.current_page == "registrar":
    # Mostrar a sidebar quando autenticado
    show_sidebar()
    
    st.markdown("<h1 style='color: #76B82A;'>Registro de Detecção da Broca</h1>", unsafe_allow_html=True)
    
    # Tabs para separar o processo de captura e visualização de resultados
    tab1, tab2 = st.tabs(["Nova Análise", "Resultados"])
    
    with tab1:
        # Container para o formulário de captura
        with st.container():
            st.markdown("<h3 style='color: #76B82A;'>Captura de Imagem para Análise</h3>", unsafe_allow_html=True)
            
            # Opções de captura de imagem
            capture_option = st.radio(
                "Escolha como capturar a imagem:", 
                ["Usar Câmera", "Fazer Upload"], 
                horizontal=True,
                key="capture_option"
            )
            
            # Variável para armazenar a imagem capturada
            captured_image = None
            
            if capture_option == "Usar Câmera":
                # Captura de imagem via câmera
                st.markdown("<p style='color: #76B82A; font-weight: bold;'>Tire uma foto da amostra:</p>", unsafe_allow_html=True)
                
                # Inicialmente, mostrar apenas o botão para ativar a câmera
                if 'camera_active' not in st.session_state:
                    st.session_state.camera_active = False
                
                # Botão para ativar a câmera
                if not st.session_state.camera_active:
                    if st.button("Ativar Câmera", key="activate_camera", use_container_width=False):
                        st.session_state.camera_active = True
                        st.rerun()
                
                # Mostrar a câmera apenas se o botão foi clicado
                if st.session_state.camera_active:
                    camera_image = st.camera_input("Capturar imagem da câmera")
                    
                    # Botão para desativar a câmera
                    if st.button("Cancelar", key="deactivate_camera", use_container_width=False):
                        st.session_state.camera_active = False
                        st.rerun()
                    
                    if camera_image is not None:
                        captured_image = camera_image
                        # Exibir a imagem capturada
                        image = Image.open(camera_image)
                        st.image(image, caption="Imagem capturada", use_container_width=True)
                        # Desativar a câmera após capturar a imagem
                        st.session_state.camera_active = False
            else:
                # Upload de imagem existente
                st.markdown("<p style='color: #76B82A; font-weight: bold;'>Selecione uma imagem existente:</p>", unsafe_allow_html=True)
                uploaded_file = st.file_uploader(
                    "Escolha uma imagem", 
                    type=["jpg", "jpeg", "png"],
                    help="Selecione uma imagem contendo a broca em seu estado adulto"
                )
                
                if uploaded_file is not None:
                    captured_image = uploaded_file
                    # Exibir a imagem enviada
                    image = Image.open(uploaded_file)
                    st.image(image, caption="Imagem enviada", use_container_width=True)
            
            # Se tiver uma imagem capturada ou enviada, mostrar campos adicionais
            if captured_image is not None:
                st.markdown("<h4 style='color: #76B82A; margin-top: 20px;'>Informações da Coleta</h4>", unsafe_allow_html=True)
                
                # Campos de informação em duas colunas
                col1, col2 = st.columns(2)
                with col1:
                    location = st.text_input("Local da coleta", placeholder="Ex: Talhão A-15")
                with col2:
                    collection_date = st.date_input("Data da coleta", datetime.datetime.now())
                
                notes = st.text_area("Observações", placeholder="Insira observações adicionais aqui...")
                
                # Botão de processamento
                process_button = st.button("Processar Imagem", type="primary", use_container_width=True)
                
                # Processar a imagem quando o botão for clicado
                if process_button:
                    if not location:
                        st.warning("Por favor, informe o local da coleta.")
                    else:
                        with st.spinner("Processando imagem..."):
                            # Carregar a imagem
                            image = Image.open(captured_image)
                            
                            # Detectar broca na imagem
                            count, result_image, detection_data = detect_broca(image)
                            
                            # Salvar a imagem original e processada
                            image_id = str(uuid.uuid4())
                            original_filename = f"{image_id}_original.jpg"
                            processed_filename = f"{image_id}_processed.jpg"
                            
                            original_path = save_image(image, original_filename)
                            processed_path = save_image(result_image, processed_filename)
                            
                            # Criar registro
                            new_record = {
                                "id": image_id,
                                "date": collection_date.strftime("%Y-%m-%d"),
                                "location": location,
                                "user": st.session_state.username,
                                "num_detections": count,
                                "original_image": original_path,
                                "processed_image": processed_path,
                                "notes": notes,
                                "detection_data": detection_data
                            }
                            
                            # Adicionar ao estado da sessão
                            st.session_state.records.append(new_record)
                            save_records(st.session_state.records)
                            
                            # Armazenar dados para exibição na aba de resultados
                            st.session_state.current_record = new_record
                            st.session_state.result_image = result_image
                            st.session_state.detection_count = count
                            st.session_state.detection_data = detection_data
                            
                            # Mostrar mensagem de sucesso
                            st.success(f"Análise concluída! Foram detectadas {count} brocas.")
                            
                            # Mudar para a aba de resultados
                            st.query_params.set(tab="Resultados")
                            st.rerun()
            
            # Fechar o container
            st.markdown("</div>", unsafe_allow_html=True)
    
    with tab2:
        if 'current_record' in st.session_state:
            record = st.session_state.current_record
            
            # Layout de duas colunas para os resultados
            res_col1, res_col2 = st.columns([1, 1])
            
            with res_col1:
                st.markdown("<h3 style='color: #76B82A;'>Imagem Original</h3>", unsafe_allow_html=True)
                st.image(Image.open(record['original_image']), use_container_width=True)
            
            with res_col2:
                st.markdown("<h3 style='color: #76B82A;'>Detecção de Brocas</h3>", unsafe_allow_html=True)
                st.image(Image.open(record['result_image']), use_container_width=True)
            
            # Informações detalhadas sobre a análise
            st.markdown("<h3 style='color: #76B82A;'>Detalhes da Análise</h3>", unsafe_allow_html=True)
            
            # Exibir informações em cards
            info_cols = st.columns(3)
            
            with info_cols[0]:
                st.markdown(f"""
                <div style="padding: 15px; border-radius: 5px; background-color: #f9f9f9;">
                    <h4 style="color: #76B82A; margin-top: 0;">Brocas Detectadas</h4>
                    <p style="font-size: 24px; font-weight: bold; color: #111111;">{record['broca_count']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with info_cols[1]:
                st.markdown(f"""
                <div style="padding: 15px; border-radius: 5px; background-color: #f9f9f9;">
                    <h4 style="color: #76B82A; margin-top: 0;">Local</h4>
                    <p style="font-size: 18px; color: #111111;">{record['location']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with info_cols[2]:
                # Formatar a data/hora para exibição
                collection_dt = datetime.datetime.fromisoformat(record.get('collection_datetime', record['timestamp']))
                formatted_dt = collection_dt.strftime("%d/%m/%Y %H:%M")
                
                st.markdown(f"""
                <div style="padding: 15px; border-radius: 5px; background-color: #f9f9f9;">
                    <h4 style="color: #76B82A; margin-top: 0;">Data/Hora da Coleta</h4>
                    <p style="font-size: 18px; color: #111111;">{formatted_dt}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Exibir dados detalhados das detecções
            if 'detection_data' in record and record['detection_data']:
                with st.expander("Dados Detalhados das Detecções", expanded=False):
                    # Criar DataFrame com os dados de detecção
                    detection_df = pd.DataFrame(record['detection_data'])
                    st.dataframe(detection_df, use_container_width=True)
            
            # Observações
            if record['notes']:
                st.markdown("<h3 style='color: #76B82A;'>Observações</h3>", unsafe_allow_html=True)
                st.markdown(f"<div style='padding: 15px; border-radius: 5px; background-color: #f9f9f9;'>{record['notes']}</div>", unsafe_allow_html=True)
            
            # Botão para nova análise
            if st.button("Iniciar Nova Análise", use_container_width=True):
                # Limpar dados temporários
                if 'current_record' in st.session_state:
                    del st.session_state.current_record
                if 'current_image' in st.session_state:
                    del st.session_state.current_image
                if 'result_image' in st.session_state:
                    del st.session_state.result_image
                if 'detection_count' in st.session_state:
                    del st.session_state.detection_count
                if 'detection_data' in st.session_state:
                    del st.session_state.detection_data
                
                # Mudar para a aba de nova análise
                st.query_params.set(tab="nova_analise")
                st.rerun()
        else:
            # Mensagem quando não há resultados para exibir
            st.info("Nenhuma análise foi realizada ainda. Vá para a aba 'Nova Análise' para começar.")

# Página de gerenciamento
elif st.session_state.current_page == "gerenciamento" and st.session_state.role == "admin":
    # Mostrar a sidebar quando autenticado
    show_sidebar()
    
    st.markdown("<h1 style='color: #76B82A;'>Gerenciamento do Sistema</h1>", unsafe_allow_html=True)
    
    # Tabs com estilo melhorado
    tab1, tab2 = st.tabs(["Registros de Detecção", "Gerenciamento de Usuários"])
    
    with tab1:
        st.markdown("<h3 style='color: #76B82A;'>Registros de Detecção da Broca</h3>", unsafe_allow_html=True)
        
        # Filtros em um container com estilo
        with st.container():
            st.markdown("<h4 style='color: #76B82A;'>Filtros</h4>", unsafe_allow_html=True)
            filter_cols = st.columns([1, 1, 1, 1])
            
            with filter_cols[0]:
                filter_date_start = st.date_input(
                    "Data inicial",
                    value=None,
                    help="Filtrar registros a partir desta data"
                )
            
            with filter_cols[1]:
                filter_date_end = st.date_input(
                    "Data final",
                    value=None,
                    help="Filtrar registros até esta data"
                )
            
            with filter_cols[2]:
                filter_location = st.text_input(
                    "Local",
                    help="Filtrar por local da coleta"
                )
            
            with filter_cols[3]:
                filter_user = st.text_input(
                    "Usuário",
                    help="Filtrar por usuário que registrou"
                )
            
            # Botão para limpar filtros
            clear_col1, clear_col2, clear_col3 = st.columns([4, 1, 4])
            with clear_col2:
                if st.button("Limpar Filtros", use_container_width=True):
                    st.query_params.clear()
                    st.session_state.filtered_records = None
                    st.rerun()
        
        # Aplicar filtros apenas quando necessário (usando o sistema de sessão)
        if st.session_state.filtered_records is None or time.time() - st.session_state.last_refresh > 60:
            # Atualizar a cada 60 segundos ou quando os filtros mudarem
            filtered_records = st.session_state.records.copy()
            
            if filter_date_start:
                filter_date_start_str = datetime.datetime.combine(filter_date_start, datetime.time.min).isoformat()
                filtered_records = [r for r in filtered_records if r.get("collection_datetime", r["timestamp"]) >= filter_date_start_str]
            
            if filter_date_end:
                filter_date_end_str = datetime.datetime.combine(filter_date_end, datetime.time.max).isoformat()
                filtered_records = [r for r in filtered_records if r.get("collection_datetime", r["timestamp"]) <= filter_date_end_str]
            
            if filter_location:
                filtered_records = [r for r in filtered_records if filter_location.lower() in r["location"].lower()]
                
            if filter_user:
                filtered_records = [r for r in filtered_records if filter_user.lower() in r["user"].lower()]
            
            # Ordenar por data/hora (mais recentes primeiro)
            filtered_records = sorted(filtered_records, key=lambda x: x.get("collection_datetime", x["timestamp"]), reverse=True)
            
            # Armazenar na sessão
            st.session_state.filtered_records = filtered_records
            st.session_state.last_refresh = time.time()
        else:
            # Usar os registros já filtrados da sessão
            filtered_records = st.session_state.filtered_records
        
        # Exibir os registros em uma tabela editável
        if filtered_records:
            # Criar DataFrame para exibição
            df = pd.DataFrame([
                {
                    "ID": r["id"],
                    "Data/Hora": datetime.datetime.fromisoformat(r.get("collection_datetime", r["timestamp"])).strftime("%d/%m/%Y %H:%M"),
                    "Usuário": r["user"],
                    "Local": r["location"],
                    "Brocas": r["broca_count"],
                    "Observações": r["notes"][:50] + "..." if r["notes"] and len(r["notes"]) > 50 else r["notes"] or ""
                } for r in filtered_records
            ])
            
            # Exibir a tabela com opção de seleção e edição direta
            selection = st.data_editor(
                df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "ID": st.column_config.TextColumn("ID", width="small"),
                    "Data/Hora": st.column_config.TextColumn("Data/Hora", width="medium"),
                    "Usuário": st.column_config.TextColumn("Usuário", width="medium"),
                    "Local": st.column_config.TextColumn("Local", width="medium"),
                    "Brocas": st.column_config.NumberColumn("Brocas", width="small", format="%d"),
                    "Observações": st.column_config.TextColumn("Observações", width="large")
                },
                disabled=["ID", "Data/Hora", "Usuário", "Brocas"],
                num_rows="dynamic"
            )
            
            # Verificar se houve alterações na tabela e atualizar os registros
            if not df.equals(selection):
                # Encontrar as linhas alteradas
                for i, row in selection.iterrows():
                    record_id = row["ID"]
                    # Encontrar o registro correspondente
                    for r in st.session_state.records:
                        if r["id"] == record_id:
                            # Atualizar campos editáveis
                            r["location"] = row["Local"]
                            r["notes"] = row["Observações"].replace("...", "") if row["Observações"].endswith("...") else row["Observações"]
                            break
                
                # Salvar as alterações
                save_records(st.session_state.records)
                st.success("Registros atualizados com sucesso!")
                
                # Atualizar os registros filtrados
                st.session_state.filtered_records = None
                st.rerun()
            
            # Opção para visualizar detalhes do registro selecionado
            st.markdown("<h4 style='color: #76B82A;'>Detalhes do Registro</h4>", unsafe_allow_html=True)
            selected_id = st.selectbox(
                "Selecione um registro para visualizar detalhes",
                options=[r["id"] for r in filtered_records],
                format_func=lambda x: f"ID: {x} - {next((r['location'] for r in filtered_records if r['id'] == x), '')}"
            )
            
            if selected_id:
                selected_record = next((r for r in filtered_records if r["id"] == selected_id), None)
                
                if selected_record:
                    # Exibir detalhes em um layout organizado
                    detail_cols = st.columns([1, 1])
                    
                    with detail_cols[0]:
                        st.markdown("<h5 style='color: #76B82A;'>Imagem Original</h5>", unsafe_allow_html=True)
                        st.image(Image.open(selected_record["original_image"]), use_column_width=True)
                    
                    with detail_cols[1]:
                        st.markdown("<h5 style='color: #76B82A;'>Imagem Processada</h5>", unsafe_allow_html=True)
                        st.image(Image.open(selected_record["result_image"]), use_column_width=True)
                    
                    # Exibir informações detalhadas
                    with st.expander("Informações Detalhadas", expanded=True):
                        info_cols = st.columns(3)
                        
                        with info_cols[0]:
                            st.markdown(f"**ID:** {selected_record['id']}")
                            st.markdown(f"**Usuário:** {selected_record['user']}")
                            
                        with info_cols[1]:
                            # Formatar a data/hora para exibição
                            collection_dt = datetime.datetime.fromisoformat(selected_record.get('collection_datetime', selected_record['timestamp']))
                            formatted_dt = collection_dt.strftime("%d/%m/%Y %H:%M")
                            st.markdown(f"**Data/Hora da Coleta:** {formatted_dt}")
                            st.markdown(f"**Local:** {selected_record['location']}")
                            
                        with info_cols[2]:
                            st.markdown(f"**Brocas Detectadas:** {selected_record['broca_count']}")
                            
                            # Botão para excluir o registro
                            if st.button("Excluir Registro", key="delete_record", use_container_width=True):
                                st.session_state.records = [r for r in st.session_state.records if r["id"] != selected_id]
                                save_records(st.session_state.records)
                                st.session_state.filtered_records = None
                                st.success("Registro excluído com sucesso!")
                                st.rerun()
                    
                    # Exibir observações
                    if selected_record['notes']:
                        st.markdown("<h5 style='color: #76B82A;'>Observações</h5>", unsafe_allow_html=True)
                        st.markdown(f"<div style='padding: 15px; border-radius: 5px; background-color: #f9f9f9;'>{selected_record['notes']}</div>", unsafe_allow_html=True)
                    
                    # Exibir dados detalhados das detecções se disponíveis
                    if 'detection_data' in selected_record and selected_record['detection_data']:
                        st.markdown("<h5 style='color: #76B82A;'>Dados Detalhados das Detecções</h5>", unsafe_allow_html=True)
                        detection_df = pd.DataFrame(selected_record['detection_data'])
                        st.dataframe(detection_df, use_container_width=True)
        else:
            st.info("Nenhum registro encontrado com os filtros aplicados.")
    
    with tab2:
        st.markdown("<h3 style='color: #76B82A;'>Gerenciamento de Usuários</h3>", unsafe_allow_html=True)
        
        # Criar dados de usuários para exibição em tabela editável
        user_data = [
            {
                "Usuário": username,
                "Função": data["role"],
                "Último Acesso": "N/A"  # Em uma implementação real, isso seria rastreado
            } for username, data in st.session_state.users.items()
        ]
        
        # Ordenar por nome de usuário
        user_data = sorted(user_data, key=lambda x: x["Usuário"])
        
        # Exibir tabela de usuários com opção de edição direta
        st.markdown("<h4 style='color: #76B82A;'>Usuários Cadastrados</h4>", unsafe_allow_html=True)
        
        user_df = pd.DataFrame(user_data)
        edited_user_df = st.data_editor(
            user_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Usuário": st.column_config.TextColumn("Usuário", width="medium"),
                "Função": st.column_config.SelectboxColumn(
                    "Função", 
                    width="medium",
                    options=["admin", "user"],
                    required=True
                ),
                "Último Acesso": st.column_config.TextColumn("Último Acesso", width="medium")
            },
            disabled=["Último Acesso"],
            num_rows="dynamic"
        )
        
        # Verificar se houve alterações na tabela de usuários
        if not user_df.equals(edited_user_df):
            # Atualizar funções de usuários existentes
            for i, row in edited_user_df.iterrows():
                username = row["Usuário"]
                role = row["Função"]
                
                # Verificar se o usuário existe
                if username in st.session_state.users:
                    # Atualizar a função
                    st.session_state.users[username]["role"] = role
            
            # Salvar as alterações
            save_users(st.session_state.users)
            st.success("Usuários atualizados com sucesso!")
            st.rerun()
        
        # Adicionar novo usuário em um card estilizado
        st.markdown("<h4 style='color: #76B82A;'>Adicionar Novo Usuário</h4>", unsafe_allow_html=True)
        
        with st.container():
            st.markdown("""<div style="padding: 15px; border-radius: 5px; background-color: #f9f9f9;">""", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                new_username = st.text_input(
                    "Nome de usuário",
                    key="new_username",
                    help="Nome de usuário para login"
                )
                new_password = st.text_input(
                    "Senha", 
                    type="password",
                    key="new_password",
                    help="Senha para o novo usuário"
                )
                
            with col2:
                new_role = st.selectbox(
                    "Função", 
                    options=["user", "admin"],
                    key="new_role",
                    help="Função do usuário (admin tem acesso ao gerenciamento)"
                )
                
                # Espaçador para alinhar o botão com os campos
                st.write("")
                st.write("")
                
                if st.button("Adicionar Usuário", use_container_width=True, key="add_user_btn"):
                    if not new_username or not new_password:
                        st.error("Preencha todos os campos!")
                    elif new_username in st.session_state.users:
                        st.error("Usuário já existe!")
                    else:
                        # Adicionar novo usuário
                        st.session_state.users[new_username] = {
                            "password": hashlib.sha256(new_password.encode()).hexdigest(),
                            "role": new_role
                        }
                        save_users(st.session_state.users)
                        st.success("Usuário adicionado com sucesso!")
                        st.rerun()
            
            st.markdown("""</div>""", unsafe_allow_html=True)
        
        # Gerenciamento de usuários existentes
        st.markdown("<h4 style='color: #76B82A;'>Gerenciar Usuários Existentes</h4>", unsafe_allow_html=True)
        
        # Duas colunas: uma para alterar senha e outra para remover usuário
        manage_col1, manage_col2 = st.columns(2)
        
        with manage_col1:
            st.markdown("<h5 style='color: #76B82A;'>Alterar Senha</h5>", unsafe_allow_html=True)
            
            with st.container():
                st.markdown("""<div style="padding: 15px; border-radius: 5px; background-color: #f9f9f9;">""", unsafe_allow_html=True)
                
                user_to_change = st.selectbox(
                    "Selecione um usuário", 
                    options=list(st.session_state.users.keys()),
                    key="user_change_password",
                    help="Selecione o usuário para alterar a senha"
                )
                
                new_password_change = st.text_input(
                    "Nova senha", 
                    type="password",
                    key="new_password_change",
                    help="Digite a nova senha para o usuário selecionado"
                )
                
                if st.button("Alterar Senha", use_container_width=True, key="change_password_btn"):
                    if not new_password_change:
                        st.error("Digite a nova senha!")
                    else:
                        # Atualizar senha
                        st.session_state.users[user_to_change]["password"] = hashlib.sha256(new_password_change.encode()).hexdigest()
                        save_users(st.session_state.users)
                        st.success("Senha alterada com sucesso!")
                
                st.markdown("""</div>""", unsafe_allow_html=True)
        
        with manage_col2:
            st.markdown("<h5 style='color: #76B82A;'>Remover Usuário</h5>", unsafe_allow_html=True)
            
            with st.container():
                st.markdown("""<div style="padding: 15px; border-radius: 5px; background-color: #f9f9f9;">""", unsafe_allow_html=True)
                
                user_to_remove = st.selectbox(
                    "Selecione um usuário para remover", 
                    options=list(st.session_state.users.keys()),
                    key="user_to_remove",
                    help="Selecione o usuário que deseja remover"
                )
                
                # Aviso de confirmação
                st.warning("Esta ação não pode ser desfeita!")
                
                if st.button("Remover Usuário", use_container_width=True, key="remove_user_btn"):
                    # Verificar se é o último administrador
                    admin_count = sum(1 for u, data in st.session_state.users.items() if data["role"] == "admin")
                    
                    if user_to_remove == st.session_state.username:
                        st.error("Você não pode remover seu próprio usuário!")
                    elif st.session_state.users[user_to_remove]["role"] == "admin" and admin_count <= 1:
                        st.error("Não é possível remover o último usuário administrador!")
                    else:
                        # Remover usuário
                        del st.session_state.users[user_to_remove]
                        save_users(st.session_state.users)
                        st.success("Usuário removido com sucesso!")
                        st.rerun()
                
                st.markdown("""</div>""", unsafe_allow_html=True)
