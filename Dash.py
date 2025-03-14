import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Configuração da Página
st.set_page_config(page_title="Cybersecurity Dashboard", layout="wide")

# Título
st.title("🔒 Cybersecurity Dashboard: Leaked Data Overview")

# Carregar os dados
@st.cache_data  # Cache para evitar recarregamento desnecessário
def load_data():
    try:
        data = pd.read_csv("leaked_data.csv")

        # Removendo espaços extras nos nomes das colunas
        data.columns = data.columns.str.strip()

        # Garantindo que a coluna 'YEAR' contenha apenas valores numéricos
        if "YEAR" in data.columns:
            data = data[data["YEAR"].str.isnumeric()]  # Mantém apenas anos numéricos
            data["YEAR"] = data["YEAR"].astype(int)  # Converte para inteiro
            data["date"] = pd.to_datetime(data["YEAR"], format="%Y")  # Converte para data
        else:
            st.warning("A coluna 'YEAR' não foi encontrada no arquivo CSV!")

        return data

    except Exception as e:
        st.error(f"Erro ao carregar os dados: {e}")
        return pd.DataFrame()  # Retorna um DataFrame vazio caso haja erro

# Carregar os dados
data = load_data()

# Verificar se os dados foram carregados corretamente
if data.empty:
    st.error("Os dados não foram carregados corretamente. Verifique o arquivo CSV!")
    st.stop()  # Para a execução do Streamlit

# Mostrar os primeiros registros
st.subheader("📊 Visão Geral dos Dados")
st.dataframe(data.head())

# Gráfico de vazamentos ao longo do tempo
if "date" in data.columns and not data["date"].isna().all():
    st.subheader("📅 Vazamentos ao Longo do Tempo")
    leaks_over_time = data.groupby(data["date"].dt.year).size()
    st.line_chart(leaks_over_time)
else:
    st.warning("Os dados não contêm informações de data válidas para gerar o gráfico de vazamentos.")

# Mensagem final
st.success("✅ Dashboard carregado com sucesso!")
