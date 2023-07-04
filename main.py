import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import plotly.express as px

import streamlit as st

## Paleta 01 - 5 cores
RED1, GREEN1, GREEN2, YELLOW1, RED2 = "#EE6055", "#60D394", "#AAF683", "#FFD97D", "#FF9B85"
PALETA01 = [RED1, GREEN1, GREEN2, YELLOW1, RED2]

## Paleta 02 - 10 cores
VINHO1, VINHO2, VINHO3, VINHO4, VINHO5 =  "#590D22", "#800F2F", "#A4133C", "#C9184A", "#FF4D6D"
VINHO6, VINHO7, VINHO8, VINHO9, VINHO10 = "#FF758F", "#FF758F", "#FF758F", "#FF758F", "#FF758F"
PALETA02 = [VINHO1, VINHO2, VINHO3, VINHO4, VINHO5, VINHO6, VINHO7, VINHO8, VINHO9, VINHO10]

## Paleta 03 - Títulos
CINZA1, CINZA2, CINZA3, CINZA4, CINZA5 = '#212529', '#495057', '#adb5bd', '#dee2e6', '#f8f9fa'

dados = pd.read_csv("ExpVinho.csv", sep=";", encoding="utf-8", thousands=".")

tab0, tab1, tab2 = st.tabs(["Exportação de vinhos", "Exportação por continente", "Exportação por países"])

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

total_dolar_ano = dados_dolar.drop("Total", axis = 1).set_index("País").T
total_dolar_ano["Total"] = total_dolar_ano.loc[:].sum(axis = 1)

dados_dolar_ordenados = dados_dolar_combinado.sort_values("Total", axis= 0 , ascending= False)

dados_dolar_anual_total = dados_dolar_combinado.copy()
dados_dolar_anual_total.columns = dados_dolar_anual_total.columns.str.replace("-Dolar","")
export_por_ano = dados_dolar_anual_total.iloc[:,1:-2].sum().to_frame().rename(columns={0: "Total"})
export_por_ano["Total"] = (export_por_ano["Total"] / 1e6).round(2)

with tab0:
    '''
    ## Tab Geral
    '''
    fig0 = plt.figure(figsize=(20, 10))
    axis = sns.lineplot(data=total_dolar_ano, x=total_dolar_ano.index, y="Total")
    axis.yaxis.set_major_formatter(ticker.StrMethodFormatter("U$ {x} mi"))
    plt.title("Exportação de vinhos no período de 2007 á 2021")

    st.pyplot(fig0, use_container_width=True)

    # Definindo a área do gráfico e o tema da visualização
    fig, ax = plt.subplots(figsize=(14, 6))

    # Desenhando o gráfico
    ax.plot(export_por_ano.index, export_por_ano["Total"], marker="o")

    # Personalizando o gráfico
    ax.set_title('Exportação de Vinhos em milhões de dolares (U$ mi) (2007 - 2021)',
                 loc='left', fontsize=18, color=CINZA1, pad=40)
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.xaxis.set_tick_params(labelsize=14, labelcolor=CINZA2)
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("U$ {x} mi"))
    ax.grid(axis="y", linestyle="--", lw=1)
    ax.set_ylim(0, 25)
    sns.despine(left=True, bottom=True)

    st.pyplot(fig, use_container_width=True)

with tab1:
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
    fig2.update_layout(width=1000, height=600, font_family='DejaVu Sans', font_size=15,
                      font_color="grey", title_font_color="black", title_font_size=24,
                      title_text='Vendas de vinho por continente' +
                                 '<br><sup size=1 style="color:#555655">De 2007 a 2021</sup>',
                      xaxis_title='', yaxis_title='', plot_bgcolor="#f8f9fa")

    # Ajustando os ticks do eixo y para o formato em milhões
    fig2.update_yaxes(tickprefix="U$ ", ticksuffix=" Mi")

    fig2.update_xaxes(tickmode='array', tickvals=np.arange(2007, 2022, 2))

    st.plotly_chart(fig2, use_container_width=True)


with tab2:
    '''
    ## Sub Tab 1
    '''
    fig0 = plt.figure(figsize=(14, 8))
    ax = sns.barplot(data=dados_dolar_ordenados.head(10), y="País", x="Total")
    plt.title("Top 10 Países que mais importam vinhos do Brasil")
    plt.xlabel("Total em milhões de US$")
    ax.xaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.2f}"))

    st.pyplot(fig0, use_container_width=True)