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
    dados.head()