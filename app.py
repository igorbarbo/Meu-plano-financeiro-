
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Terminal Rumo ao Milhão", layout="wide")

# --- BARRA LATERAL ---
st.sidebar.header("⚙️ Parâmetros do Projeto")
aporte = st.sidebar.number_input("Aporte Mensal (R$)", value=3000.0)
patrimonio_atual = st.sidebar.number_input("Patrimônio Já Acumulado (R$)", value=0.0)
rentabilidade_anual = st.sidebar.slider("Rentabilidade Esperada (% ao ano)", 5.0, 15.0, 10.0)

total_disponivel = aporte

# --- CÁLCULO DO MILHÃO ---
juros_mensais = (1 + rentabilidade_anual/100)**(1/12) - 1
objetivo = 1000000

# Fórmula de juros compostos para tempo (n)
if patrimonio_atual >= objetivo:
    meses_para_milhao = 0
else:
    # Cálculo simplificado de meses para atingir o objetivo
    meses_para_milhao = np.log((objetivo * juros_mensais + aporte) / (patrimonio_atual * juros_mensais + aporte)) / np.log(1 + juros_mensais)

anos = int(meses_para_milhao // 12)
meses = int(meses_para_milhao % 12)

# --- LAYOUT PRINCIPAL ---
st.title("💰 Terminal Rumo ao Milhão")

col1, col2, col3 = st.columns(3)
col1.metric("Aporte Atual", f"R$ {total_disponivel:,.2f}")
col2.metric("Tempo até o Milhão", f"{anos} anos e {meses} meses")
col3.metric("Meta", "R$ 1.000.000,00")

st.markdown("---")

# --- TABELA DE ATIVOS COM CÁLCULO DE COTAS ---
# Adicionei o 'Preço_Atual' para o sistema saber quantas cotas cabem no seu bolso
ativos = [
    {"Ativo": "KNCR11", "Peso": 0.25, "Preço_Atual": 102.50, "Teto": 103.50},
    {"Ativo": "XPML11", "Peso": 0.25, "Preço_Atual": 115.20, "Teto": 119.00},
    {"Ativo": "BTLG11", "Peso": 0.20, "Preço_Atual": 102.10, "Teto": 105.00},
    {"Ativo": "BBAS3", "Peso": 0.10, "Preço_Atual": 27.10, "Teto": 28.50},
    {"Ativo": "TAEE11", "Peso": 0.10, "Preço_Atual": 34.80, "Teto": 36.00},
    {"Ativo": "BBSE3", "Peso": 0.10, "Preço_Atual": 33.20, "Teto": 34.50}
]

st.subheader("🛒 Ordens de Compra (Investimento Automático)")
df = pd.DataFrame(ativos)

# Cálculos Automáticos
df['Valor_Alocar'] = total_disponivel * df['Peso']
df['Qtd_Cotas'] = (df['Valor_Alocar'] / df['Preço_Atual']).astype(int)
df['Investimento_Real'] = df['Qtd_Cotas'] * df['Preço_Atual']

# Exibição
for _, row in df.iterrows():
    if row['Preço_Atual'] <= row['Teto']:
        st.success(f"✅ **{row['Ativo']}**: Comprar **{row['Qtd_Cotas']}** cotas. (Total: R$ {row['Investimento_Real']:,.2f})")
    else:
        st.warning(f"⚠️ **{row['Ativo']}**: Acima do preço teto. Não comprar agora.")

st.markdown("---")
st.info("ℹ️ O 'Investimento Automático' calcula a quantidade inteira de cotas que o seu aporte permite comprar hoje, respeitando a sua estratégia de pesos.")
