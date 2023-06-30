import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import plotly.express as px

import streamlit as st

dados = pd.read_csv("ExpVinho.csv", sep=";", encoding="utf-8", thousands=".")

tab0, tab1, tab2 = st.tabs(["Continente", "Países"])

col_pais = dados[["País"]]

dados_15anos = dados[dados.columns[-30:]]
cols = dados_15anos.columns.str.replace(".", "-Dolar")
cols = cols.str.replace("r1", "r")

dados_15anos.columns = cols

dados_dolar = dados_15anos[dados_15anos.columns[1::2]]
dados_dolar = col_pais.join(dados_dolar)

dados_dolar["Total"] = dados_dolar.iloc[:, 2:].sum(axis=1)

dados_dolar["País"].unique()
dados_dolar.loc[dados_dolar["País"] == "Alemanha, República Democrática", "País"] = "Alemanha"
dados_dolar.loc[dados_dolar["País"] == "Coreia, Republica Sul", "País"] = "Coreia do Sul"
dados_dolar.loc[dados_dolar["País"] == "Eslovaca, Republica", "País"] = "Eslováquia"
dados_dolar.loc[dados_dolar["País"] == "Taiwan (FORMOSA)", "País"] = "Taiwan"
dados_dolar.loc[dados_dolar["País"] == "Tcheca, República", "País"] = "Chéquia"

dados_dolar["País"].unique()

dados_pais_continente = \
pd.read_html("https://pt.wikipedia.org/wiki/Lista_de_pa%C3%ADses_por_PIB_nominal", match="País/Território",
                 flavor="lxml", header=2)[0]

dados_pais_continente = dados_pais_continente[dados_pais_continente.columns[:2]]
dados_pais_continente.columns = ["País", "Continente"]
dados_pais_continente["Continente"] = dados_pais_continente["Continente"].str.replace("Africa", "África")

dados_pais_continente.query("Continente == 'Europa/Ásia'")

dados_dolar_combinado = dados_dolar.merge(dados_pais_continente[["País", "Continente"]], on="País")

vendas_por_continente = dados_dolar_combinado.groupby("Continente").sum()[["Total"]]
vendas_por_continente = vendas_por_continente.sort_values("Total", ascending=False)
vendas_por_continente = (vendas_por_continente / 1e6).round(1)
vendas_por_continente = vendas_por_continente.reset_index()

dados_dolar_anual = dados_dolar_combinado.copy()
cols = dados_dolar_anual.columns.str.replace("-Dolar","")
dados_dolar_anual.columns = cols
dados_dolar_anual = dados_dolar_anual.melt(id_vars = "Continente", value_vars=dados_dolar_anual.columns[1:16], var_name="Ano", value_name="Vendas_Dolar")

# Criando uma tabela cruzada (crosstab) com os valores de venda por ano por continente
vendas_por_ano = pd.crosstab(index = dados_dolar_anual.Ano, columns = dados_dolar_anual.Continente,
                             values = dados_dolar_anual.Vendas_Dolar, aggfunc="sum")

vendas_por_ano = vendas_por_ano / 1e6

with tab0:
    '''
    ## Tab Geral
    '''
    #DataFrame
    fig1 = plt.figure(figsize=(12, 6))
    axis = sns.barplot(data=vendas_por_continente, x="Continente", y="Total")
    axis.yaxis.set_major_formatter(ticker.StrMethodFormatter("U$ {x} mi"))
    #plt.ylim(0,2500000)
    plt.xticks()

    st.pyplot(fig1, use_container_width=True)

    # Gerando um gráfico de linha com o faturamento da loja por trimestre dividido por região
    fig2 = px.line(vendas_por_ano, x=vendas_por_ano.index, y=vendas_por_ano.columns)

    # Ajustando o layout do gráfico
    fig2.update_layout(width=1300, height=600, font_family='DejaVu Sans', font_size=15,
                      font_color="grey", title_font_color="black", title_font_size=24,
                      title_text='Vendas de vinho por continente' +
                                 '<br><sup size=1 style="color:#555655">De 2007 a 2021</sup>',
                      xaxis_title='', yaxis_title='', plot_bgcolor="white")

    # Ajustando os ticks do eixo y para o formato em milhões
    fig2.update_yaxes(tickprefix="U$ ", ticksuffix=" Mi")

    st.pyplot(fig2, use_container_width=True)

with tab1:
    '''
    ## Sub Tab 1
    '''