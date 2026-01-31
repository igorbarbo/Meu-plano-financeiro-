# Carregar dados da planilha
df_db = conn.read(ttl=0) # ttl=0 força a atualização imediata

# Garantir que os nomes das colunas fiquem padronizados (remove espaços e ignora maiúsculas)
df_db.columns = [c.strip().capitalize() for c in df_db.columns]

# Se a coluna se chamar 'Qtd', o código abaixo garante que ele a encontre
if 'Qtd' not in df_db.columns:
    st.error("Coluna 'Qtd' não encontrada. Verifique o título na planilha!")
    
    

 

