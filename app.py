import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import yfinance as yf

# Configuração da página
st.set_page_config(page_title="Meu Plano Financeiro", layout="wide")

st.title("📊 Terminal de Investimentos")

# 1. Criar a conexão com o Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # 2. Ler os dados (ttl=0 força a ler a planilha na hora)
    df_db = conn.read(ttl=0)
    
    # Limpeza básica: remove linhas vazias e espaços nos nomes das colunas
    df_db = df_db.dropna(subset=[df_db.columns[0]])
    df_db.columns = [c.strip() for c in df_db.columns]

    # Padronizar nomes das colunas para o código não quebrar
    # Se a planilha tiver 'ticker', 'Qtd', 'pm' -> vira 'Ticker', 'Qtd', 'PM'
    df_db.columns = ['Ticker', 'Qtd', 'PM'] + list(df_db.columns[3:])

    if not df_db.empty:
        st.success("Dados carregados com sucesso!")
        
        # Exibir a tabela para conferência
        with st.expander("Ver dados da planilha"):
            st.dataframe(df_db)

        # 3. Buscar preços atuais no Yahoo Finance
        tickers = df_db['Ticker'].tolist()
        precos = []
        
        for t in tickers:
            try:
                # Se for ação brasileira e faltar o .SA, o código tenta corrigir
                symbol = t if "." in t or t.endswith("^") else f"{t}"
                data = yf.Ticker(symbol).fast_info['last_price']
                precos.append(data)
            except:
                precos.append(0)

        df_db['Preço Atual'] = precos
        df_db['Total'] = df_db['Qtd'].astype(float) * df_db['Preço Atual']

        # 4. Criar os Gráficos
        st.subheader("Alocação por Ativo")
        st.bar_chart(df_db.set_index('Ticker')['Total'])
        
        if 'Setor' in df_db.columns:
            st.subheader("Alocação por Setor")
            setores = df_db.groupby('Setor')['Total'].sum()
            st.write(setores)
    else:
        st.warning("A planilha parece estar vazia.")

except Exception as e:
    st.error(f"Erro ao processar dados: {e}")
    st.info("Dica: Verifique se os títulos da planilha são: Ticker, Qtd, PM, Setor")
    

 

