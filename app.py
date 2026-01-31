import streamlit as st
import pandas as pd
import yfinance as yf
import numpy as np
from streamlit_gsheets import GSheetsConnection

# --- 1. CONFIGURAÇÃO E SEGURANÇA ---
st.set_page_config(page_title="Quantum Wealth Engine", layout="wide", page_icon="🏛️")

def autenticar():
    if "auth" not in st.session_state: st.session_state.auth = False
    if not st.session_state.auth:
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.title("🔐 Acesso Restrito")
            with st.form("login"):
                senha = st.text_input("Chave Institucional", type="password")
                if st.form_submit_button("Desbloquear Terminal"):
                    if senha == "SENHA123": # <--- Altere sua senha aqui
                        st.session_state.auth = True
                        st.rerun()
                    else: st.error("Chave Inválida")
        return False
    return True

# --- 2. MOTOR DE DADOS RESILIENTE ---
@st.cache_data(ttl=3600)
def fetch_global_market(tickers):
    results = {}
    for t in tickers:
        try:
            stock = yf.Ticker(t)
            hist = stock.history(period="1d")
            if not hist.empty:
                results[t] = {
                    "preco": float(hist['Close'].iloc[-1]),
                    "dps": float(stock.dividends.tail(12).sum()) if not stock.dividends.empty else 0.0
                }
            else:
                results[t] = {"preco": 0.0, "dps": 0.0}
        except:
            results[t] = {"preco": 0.0, "dps": 0.0}
    
    try:
        usd_brl = yf.Ticker("USDBRL=X").history(period="1d")['Close'].iloc[-1]
    except:
        usd_brl = 5.0 # Fallback caso a API de câmbio falhe
    return results, float(usd_brl)

# --- 3. EXECUÇÃO PRINCIPAL ---
if autenticar():
    # Conexão Cloud com Google Sheets
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df_db = conn.read(ttl="1m")
        # Forçar conversão numérica para evitar erros de texto na planilha
        cols_num = ['Qtd', 'PM', 'Peso', 'Teto']
        for col in cols_num:
            df_db[col] = pd.to_numeric(df_db[col], errors='coerce').fillna(0.0)
    except Exception as e:
        st.error(f"Erro de conexão com Google Sheets: {e}")
        st.info("Dica: Verifique se o link da planilha está nos 'Secrets' do Streamlit Cloud.")
        st.stop()

    # Busca de Preços e Câmbio
    market_info, cambio_atual = fetch_global_market(df_db['Ticker'].tolist())
    
    # Processamento de Dados (Vetorizado para Performance)
    df_db['Preco_Orig'] = df_db['Ticker'].map(lambda x: market_info[x]['preco'])
    df_db['DPS_Anual'] = df_db['Ticker'].map(lambda x: market_info[x]['dps'])
    
    # Conversão de Moeda Automática
    df_db['Preco_BRL'] = np.where(df_db['Moeda'] == "USD", df_db['Preco_Orig'] * cambio_atual, df_db['Preco_Orig'])
    df_db['Saldo_BRL'] = df_db['Qtd'] * df_db['Preco_BRL']
    
    # Cálculo de Renda (Yield on Cost) com proteção contra divisão por zero
    df_db['YoC'] = (df_db['DPS_Anual'] / df_db['PM'].replace(0, np.nan)).fillna(0)

    # --- DASHBOARD UI ---
    st.title("🏛️ Quantum Wealth Institutional")
    st.caption(f"Câmbio Atual: 1 USD = R$ {cambio_atual:.2f}")
    
    tab1, tab2, tab3 = st.tabs(["🎯 Rebalanceamento", "🛡️ Análise de Risco", "💸 Simulador Fiscal"])

    with tab1:
        aporte = st.sidebar.number_input("Valor do Aporte (R$)", min_value=0.0, value=1000.0)
        patrimonio_total = df_db['Saldo_BRL'].sum() + aporte
        
        df_db['V_Ideal'] = patrimonio_total * df_db['Peso']
        df_db['Desvio'] = (df_db['V_Ideal'] - df_db['Saldo_BRL']).clip(lower=0)
        
        # Distribuição Proporcional do Aporte
        soma_desvios = df_db['Desvio'].sum()
        df_db['Sugerido_R$'] = (df_db['Desvio'] / soma_desvios * aporte) if soma_desvios > 0 else 0
        df_db['Comprar_Qtd'] = (df_db['Sugerido_R$'] / df_db['Preco_BRL'].replace(0, np.nan)).fillna(0).astype(int)

        st.subheader("🛒 Sugestões de Compra")
        st.dataframe(df_db[['Ativo', 'Preco_Orig', 'Teto', 'Comprar_Qtd']].style.highlight_max(axis=0, subset=['Comprar_Qtd'], color='#2e7d32'))

    with tab2:
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("📊 Yield on Cost por Ativo")
            st.bar_chart(df_db.set_index('Ativo')['YoC'])
        with c2:
            st.subheader("🌍 Alocação por Setor")
            st.pie_chart(df_db.groupby('Setor')['Saldo_BRL'].sum())

    with tab3:
        st.subheader("💸 Planejador de Saída")
        sel_ativo = st.selectbox("Escolha o ativo para simular venda", df_db['Ativo'].unique())
        dados_venda = df_db[df_db['Ativo'] == sel_ativo].iloc[0]
        p_venda = st.number_input("Preço de Venda Simulado", value=dados_venda['Preco_Orig'])
        
        lucro = (p_venda - dados_venda['PM']) * dados_venda['Qtd']
        imposto = max(lucro * 0.15, 0) if lucro > 0 else 0
        st.metric("Imposto Estimado (IR)", f"R$ {imposto:,.2f}", delta=f"Lucro: R$ {lucro:,.2f}")

# --- ARQUITETURA FINAL ---
# 

 

