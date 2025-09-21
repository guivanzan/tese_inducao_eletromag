import numpy as np
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from utils import *
from random import randint,random

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
    #st.markdown('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum')
    import streamlit as st

    st.set_page_config(page_title="Sobre a Transformada de Fourier", layout="centered")

    # Explicação em um único parágrafo (perfil do usuário: português, parágrafo único)
    explicacao = (
    "Joseph Fourier, ao estudar equações de calor no início do século XIX, propôs que funções periódicas "
    "podem ser decompostas em somas de senos e cossenos — a chamada Série de Fourier — estabelecendo a ideia de "
    "representação espectral de sinais; desta concepção natural evoluiu a Transformada de Fourier contínua, que "
    "extende a ideia de soma infinita a uma integral que mapeia uma função do tempo para uma função das frequências, "
    "permitindo caracterizar amplitude e fase de componentes harmônicas em sinais não necessariamente periódicos.")

    st.title("Sobre a Transformada de Fourier")
    st.markdown(f'<div style="text-align: justify;">{explicacao}</div>', unsafe_allow_html=True)
    # st.markdown(explicacao, unsafe_allow_html=True)

    st.latex(r"f(t)=\sum_{n=-\infty}^{\infty} c_n e^{i n \omega_0 t}\quad\text{(Série de Fourier)}")
    st.latex(r"\hat{f}(\omega)=\int_{-\infty}^{\infty} f(t) e^{-i\omega t} \,dt\quad\text{(Transformada Contínua)}")
    st.latex(r"X_k=\sum_{n=0}^{N-1} x_n e^{-2\pi i kn/N}\quad\text{(DFT)}")

    st.header("Demonstrações e plots")
    col1, col2 = st.columns([3,1])
    with col1:
        st.write("Aperte o botão abaixo para gerar um sinal composto (soma de mais de uma senóide) e ver seu espectro usando a FFT.")
    with col2:
        boom = st.button("Criar senóides")

    freqs = []
    amps = []

    if boom:
        for i in range (6):
            newDigit = randint(0,((i+1)*50))
            if len(freqs) > 0:
                for freq in freqs:
                    while newDigit < freq:
                        newDigit = randint(0,((i+1)*50))
            freqs.append(newDigit)
            amps.append(random())
                
        # Parâmetros do sinal
        fs = 1024 # taxa de amostragem
        T = 1.0 # duração em segundos
        N = int(fs * T)
        t = np.linspace(0, T, N, endpoint=False)


        # Sinal: soma de duas senóides + ruído
        
        # freqs = [50, 80, 120, 150, 300, 400]
        # amps = [1, 2, 3, 4, 5, 6]
        for freq, amp in zip(freqs,amps):
            if freq == freqs[0]:
                x = (amp * np.sin(2 * np.pi * freq * t))
            else:
                x = x + (amp * np.sin(2 * np.pi * freq * t))
        x = x + np.mean(amps) * np.random.randn(N)

        # FFT
        X = np.fft.fft(x)
        freqs = np.fft.fftfreq(N, 1 / fs)


        # Apenas parte positiva do espectro
        pos_mask = freqs >= 0
        freqs_pos = freqs[pos_mask]
        X_pos = X[pos_mask]


        # Plot do sinal no tempo com Plotly
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=x[:512], y=t[:512], mode='lines', name='Sinal',marker_color="black"))
        fig1.update_layout(
        title='Sinal no domínio do tempo (trecho)',
        xaxis_title='Amplitude',
        yaxis_title='Tempo (s)',
        yaxis=dict(autorange='reversed'),
        template='plotly_white',
        height=1200
        )
        st.plotly_chart(fig1, use_container_width=True, key=randint(1,1000000))


        # Plot do espectro (magnitude) com Plotly
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=np.abs(X_pos) / N, y=freqs_pos, mode='lines', name='Magnitude',marker_color="black"))
        fig2.update_layout(
        title='Espectro obtido pela FFT (magnitude)',
        xaxis_title='Intensidade',
        yaxis_title='Frequência (Hz)',
        yaxis=dict(autorange='reversed'),
        template='plotly_white',
        height=1200
        )
        st.plotly_chart(fig2, use_container_width=True, key = randint(1,10000000))
