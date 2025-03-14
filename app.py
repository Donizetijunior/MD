import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar os dados
df = pd.read_csv("data_lake.csv", sep=",", decimal=".")

# Garantir que a coluna 'Perdas' é numérica (removendo R$ e espaços extras)
df["Perdas"] = df["Perdas"].astype(str).str.replace("R$", "").str.replace(",", "").str.strip()
df["Perdas"] = pd.to_numeric(df["Perdas"], errors="coerce").fillna(0)

# Título da aplicação
st.title("Análise de Dados Sensíveis e Prejuízos")


# Gráfico 1: Dados sensíveis por empresa
st.subheader("Dados Sensiveis Vazados por Empresa")
dados_empresa = df.groupby("Empresa")["Dados"].sum().reset_index()
fig1 = px.bar(dados_empresa, x="Empresa", y="Dados", title="Dados Sensíveis por Empresa")
st.plotly_chart(fig1)

# Gráfico 2: Total de prejuízo por ano por empresa
st.subheader("Total de Prejuízo por Empresa")
prejuizo_ano_empresa = df.groupby("Empresa")["Perdas"].sum().reset_index()
fig2 = px.bar(prejuizo_ano_empresa, x="Empresa", y="Perdas", title="Total de Prejuízo por Empresa", text="Perdas")
fig2.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig2.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
st.plotly_chart(fig2)

# Gráfico 3: Método x Setor
st.subheader("Método de Hack por Setor")
metodo_setor = df.groupby(["Metodo", "Setor"]).size().reset_index(name="contagem")
fig3 = px.bar(metodo_setor, x="Metodo", y="contagem", color="Setor", barmode="group", title="Método x Setor")
st.plotly_chart(fig3)

# Gráfico 4: Total de prejuízo por método
st.subheader("Total Acumulado de Prejuízo por Métodode Hack")
prejuizo_metodo = df.groupby("Metodo")["Perdas"].sum().reset_index()
prejuizo_metodo["Perdas"] = prejuizo_metodo["Perdas"].round(2)  # Arredondar valores para melhor visualização
st.write("Debug: Dados de prejuízo por método", prejuizo_metodo)  # Exibir dados para verificação
if not prejuizo_metodo.empty:
    fig4 = px.pie(prejuizo_metodo, names="Metodo", values="Perdas", title="Distribuição do Prejuízo Total por Método")
    st.plotly_chart(fig4)
else:
    st.warning("Não há dados suficientes para exibir o gráfico de prejuízo por método.")
