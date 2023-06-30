import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

import streamlit as st

dados = pd.read_csv("ExpVinho.csv", sep=";", encoding="utf-8", thousands=".")

tab0 = st.tabs("Geral")

with tab0:
    '''
    TAB Geral
    '''

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

    plt.figure(figsize=(12, 6))
    axis = sns.barplot(data=vendas_por_continente, x="Continente", y="Total")
    axis.yaxis.set_major_formatter(ticker.StrMethodFormatter("U$ {x} mi"))
    # plt.ylim(0,2500000)
    plt.xticks()
    plt.show()

    df = pd.DataFrame(vendas_por_continente)
    st.dataframe(df, use_container_width=True)
    st.pyplot(sns.pairplot(vendas_por_continente, hue = "classe"))