import numpy as np
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout='wide')
st.title('Atividade de Indução Eletromagnética via análise de harmônicos')

uploaded = st.file_uploader(
    "Upload data", accept_multiple_files=False, type="txt")


if uploaded:
    dado = pd.read_csv(uploaded,header=None,names=['measures'])
    dado = dado['measures'].to_list()


    n_ondas = 2                # número de ondas capturadas
    n = n_ondas * 64           # 64 amostras por onda
    T = n_ondas * 1.0 / 60     # período total
    dt = T / n                 # intervalo entre medidas
    t = dt * np.arange(0, n)   # vetor de tempo

    # ==== Transformada de Fourier ====
    dado = dado - np.mean(dado)
    Fk = np.fft.fft(dado) / n
    nu = np.fft.fftfreq(n, dt)
    delta = np.angle(Fk)

    # ==== Gráficos ====
    # Forma de onda
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=t[:len(dado)],
        y=dado,
        mode="lines",
        line=dict(color="black"),
        name="Sinal"
    ))
    fig1.update_layout(
        title="Sinal no tempo",
        xaxis_title="Tempo (s)",
        yaxis_title="Voltagem induzida (V)",
        xaxis=dict(range=[0.001, T]),
        yaxis=dict(range=[1.05*min(dado), 1.05*max(dado)])
    )

    # === Gráfico do espectro de Fourier ===
    max_freq = 1200
    max_amp = max(abs(Fk))

    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        x=nu,
        y=np.abs(Fk),
        marker_color="blue",
        name="Frequência"
    ))
    fig2.update_layout(
        title="Espectro de Fourier",
        xaxis_title="Freq (Hz)",
        yaxis_title="|A(freq)|",
        xaxis=dict(range=[45, max_freq], tickmode="array", tickvals=np.arange(0, max_freq+1, 60)),
        yaxis=dict(range=[0, max_amp * 1.2])
    )

    # === Exibição lado a lado ===
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        st.plotly_chart(fig2, use_container_width=True)