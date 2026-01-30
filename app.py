import streamlit as st
import pandas as pd

st.set_page_config(page_title="Quantum Wealth Terminal", layout="wide")

st.sidebar.header("📊 Painel de Controle")
aporte = st.sidebar.number_input("Aporte Mensal (R$)", value=3000.0)
dividendos = st.sidebar.number_input("Dividendos (R$)", value=0.0)
total = aporte + dividendos

ativos = [
    {"Ativo": "KNCR11", "Peso": 0.25, "Teto": 103.50},
        {"Ativo": "XPML11", "Peso": 0.25, "Teto": 119.00},
            {"Ativo": "BTLG11", "Peso": 0.20, "Teto": 105.00},
                {"Ativo": "BBAS3", "Peso": 0.10, "Teto": 28.50},
                    {"Ativo": "TAEE11", "Peso": 0.10, "Teto": 36.00},
                        {"Ativo": "BBSE3", "Peso": 0.10, "Teto": 34.50}
                        ]

                        st.title("🚀 Terminal Quantum Wealth")
                        st.metric("Poder de Compra Total", f"R$ {total:,.2f}")

                        st.subheader("🛒 Compras Sugeridas")
                        for a in ativos:
                            valor_alocar = total * a['Peso']
                            st.success(f"**{a['Ativo']}**: Investir R$ {valor_alocar:,.2f} (Preço Teto: R$ {a['Teto']})")
                            