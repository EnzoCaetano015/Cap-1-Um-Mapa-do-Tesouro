from pathlib import Path

import pandas as pd
import streamlit as st


def carregar_dados() -> pd.DataFrame:
    base_dir = Path(__file__).resolve().parents[2]
    caminho_csv = base_dir / "data" / "sensores_fase2.csv"
    df = pd.read_csv(caminho_csv)
    df["data_hora"] = pd.to_datetime(df["data_hora"])
    return df


def main() -> None:
    st.set_page_config(page_title="FarmTech Solutions - Fase 3", layout="wide")
    st.title("FarmTech Solutions - Fase 3")
    st.write("Dashboard para monitoramento de sensores e irrigação")

    df = carregar_dados()

    opcoes_status = ["Todos", "LIGADA", "DESLIGADA"]
    status_selecionado = st.selectbox("Filtrar por status da irrigacao", opcoes_status)

    if status_selecionado != "Todos":
        df_filtrado = df[df["status_irrigacao"] == status_selecionado]
    else:
        df_filtrado = df

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Media umidade", f"{df_filtrado['umidade'].mean():.2f}")
    col2.metric("Media temperatura", f"{df_filtrado['temperatura'].mean():.2f}")
    col3.metric("Media pH", f"{df_filtrado['ph'].mean():.2f}")
    col4.metric("Total leituras", f"{len(df_filtrado)}")
    col5.metric("Irrigacao ligada", f"{(df_filtrado['status_irrigacao'] == 'LIGADA').sum()}")

    st.subheader("Umidade ao longo do tempo")
    st.line_chart(df_filtrado.set_index("data_hora")["umidade"])

    st.subheader("pH ao longo do tempo")
    st.line_chart(df_filtrado.set_index("data_hora")["ph"])

    st.subheader("Presenca de P e K")
    pk = pd.DataFrame(
        {
            "sensor": ["P", "K"],
            "total": [df_filtrado["p"].sum(), df_filtrado["k"].sum()],
        }
    )
    st.bar_chart(pk.set_index("sensor"))

    st.subheader("Status da irrigacao")
    status_counts = df_filtrado["status_irrigacao"].value_counts().sort_index()
    st.bar_chart(status_counts)

    st.subheader("Sugestoes de irrigacao")
    st.dataframe(df_filtrado[["data_hora", "status_irrigacao", "sugestao"]])


if __name__ == "__main__":
    main()
