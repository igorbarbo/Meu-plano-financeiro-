import streamlit as st
import pandas as pd

# Configuração Básica
st.set_page_config(page_title="Quantum Wealth Terminal", layout="wide")

st.sidebar.header("📊 Painel de Controle")
aporte = st.sidebar.number_input("Aporte Mensal (R$)", value=3000.0)
dividendos = st.sidebar.number_input("Dividendos Recebidos (R$)", value=0.0)
total = aporte + dividendos

# Carteira Híbrida
ativos = [
    {"Ativo": "KNCR11", "Peso": 0.25, "Teto": 103.50},
        {"Ativo": "XPML11", "Peso": 0.25, "Teto": 119.00},
            {"Ativo": "BTLG11", "Peso": 0.20, "Teto": 105.00},
                {"Ativo": "BBAS3F", "Peso": 0.10, "Teto": 28.50},
                    {"Ativo": "TAEE11F", "Peso": 0.10, "Teto": 36.00},
                        {"Ativo": "BBSE3F", "Peso": 0.10, "Teto": 34.50}
                        ]

                        st.title("🚀 Terminal Quantum Wealth")
                        st.metric("Poder de Compra", f"R$ {total:,.2f}")

                        st.subheader("🛒 Compras Recomendadas")
                        for a in ativos:
                            valor = total * a['Peso']
                                st.success(f"**{a['Ativo']}**: R$ {valor:,.2f} (Até R$ {a['Teto']})")

                                st.write("---")
                                meses = st.slider("Meses de Investimento", 1, 96, 12)
                                patrimonio = (total * ((1.011**meses) - 1) / 0.011)
                                st.info(f"Patrimônio Estimado: R$ {patrimonio:,.2f}")

                                