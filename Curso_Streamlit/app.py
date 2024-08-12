import pandas as pd
import yfinance as yf
import streamlit as st
from datetime import date

# carregar  os dados
@st.cache_data
def load_data(empresas):
    atual = date.today().strftime("%Y-%m-%d")
    txt_tikers = " ".join(empresas)
    dados_acoes = yf.Tickers(txt_tikers)
    cotacao_acoes = dados_acoes.history(period= "1d", start = "2010-01-01", end = atual)
    cotacao_acoes =  cotacao_acoes["Close"]
    return cotacao_acoes

@st.cache_data
def load_ticker_acoes():
    base_tikers = pd.read_csv("IBOV.csv",sep=";")
    tikers = list(base_tikers["Codigo"])
    tikers = [str(cod) + ".SA" for cod in tikers] 
    return tikers


#acoes = ["ITUB4.SA","PETR4.SA","VIVA3.SA","VALE3.SA","ABEV3.SA","GGBR4.SA"]

acoes = load_ticker_acoes()

print(acoes)
dados = load_data(acoes)


#barra lateral
st.sidebar.header("Filtros")

#filtros de acoes 
lista_acoes = st.sidebar.multiselect("Ações Options",dados.columns)

if lista_acoes:
    dados = dados[lista_acoes]
    if len(lista_acoes) == 1:
        acao_unica = lista_acoes[0]
        dados = dados.rename(columns = {acao_unica: "Close"})


#filtro de data
data_inicial = dados.index.min().to_pydatetime()
data_final = dados.index.max().to_pydatetime()

intervalo_datas = st.sidebar.slider("Data",
                                    min_value=data_inicial,
                                    max_value=data_final,
                                    value=(data_inicial,data_final))

dados = dados.loc[intervalo_datas[0]:intervalo_datas[1]]


#Visual
st.write(f'''
    # App Preço das Ações
''')


st.line_chart(dados)