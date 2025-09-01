import numpy as np
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils import *

st.set_page_config(layout='wide')
st.title('Atividade de Indução Eletromagnética via análise de harmônicos')

tab1, tab2, tab3 = st.tabs(['Dado via Arduíno','Dado tabelado','Apêndice'])

with tab1:

    uploaded = st.file_uploader(
        "Upload data", accept_multiple_files=False, type="txt")


    if uploaded:
        dado = pd.read_csv(uploaded,header=None,names=['measures'])
        dado = dado['measures'].to_list()

        makePlot(dado)
        

with tab2:
    label = st.selectbox('Selecione o dado que deseja utilizar',['Tomada desconectada','Carregador de celular','Ventilador','Onda quadrada'],index=None,placeholder='    ')
    if label:
        if label == 'Tomada desconectada':

            dado = pd.read_csv('./pre_made/dado_nada.txt',header=None,names=['measures'])
            dado = dado['measures'].to_list()
            makePlot(dado)
        
        if label == 'Carregador de celular':

            dado = pd.read_csv('./pre_made/dado_carregador.txt',header=None,names=['measures'])
            dado = dado['measures'].to_list()
            makePlot(dado)

        if label == 'Ventilador':

            dado = pd.read_csv('./pre_made/dado_ventilador.txt',header=None,names=['measures'])
            dado = dado['measures'].to_list()
            makePlot(dado)
            
        if label == 'Onda quadrada':

            dado = pd.read_csv('./pre_made/dado_quadrado.txt',header=None,names=['measures'])
            dado = dado['measures'].to_list()
            makePlot(dado)

with tab3:
    st.markdown('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum')
