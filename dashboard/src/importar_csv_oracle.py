import os
import sys
from pathlib import Path

import oracledb
import pandas as pd
from dotenv import load_dotenv


def carregar_env() -> dict:
    load_dotenv()
    usuario = os.getenv("ORACLE_USER")
    senha = os.getenv("ORACLE_PASSWORD")
    dsn = os.getenv("ORACLE_DSN")

    if not usuario or not senha or not dsn:
        print("Erro: configure ORACLE_USER, ORACLE_PASSWORD e ORACLE_DSN no .env.")
        sys.exit(1)

    return {"usuario": usuario, "senha": senha, "dsn": dsn}


def carregar_csv(caminho_csv: Path) -> pd.DataFrame:
    if not caminho_csv.exists():
        raise FileNotFoundError(f"CSV nao encontrado: {caminho_csv}")

    df = pd.read_csv(caminho_csv)
    df["data_hora"] = pd.to_datetime(df["data_hora"])
    return df


def importar_dados(df: pd.DataFrame, credenciais: dict) -> int:
    conexao = oracledb.connect(
        user=credenciais["usuario"],
        password=credenciais["senha"],
        dsn=credenciais["dsn"],
    )
    cursor = conexao.cursor()

    cursor.execute("DELETE FROM FARMTECH_SENSOR_LEITURA")

    registros = []
    for indice, linha in df.iterrows():
        registros.append(
            (
                int(indice) + 1,
                linha["data_hora"].to_pydatetime(),
                float(linha["umidade"]),
                float(linha["temperatura"]),
                float(linha["ph"]),
                int(linha["n"]),
                int(linha["p"]),
                int(linha["k"]),
                int(linha["nivel_chuva"]),
                str(linha["status_irrigacao"]),
                str(linha["sugestao"]),
            )
        )

    cursor.executemany(
        """
        INSERT INTO FARMTECH_SENSOR_LEITURA
            (ID_LEITURA, DATA_HORA, UMIDADE, TEMPERATURA, PH, N, P, K, NIVEL_CHUVA, STATUS_IRRIGACAO, SUGESTAO)
        VALUES
            (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11)
        """,
        registros,
    )

    conexao.commit()
    cursor.close()
    conexao.close()
    return len(registros)


def main() -> None:
    base_dir = Path(__file__).resolve().parents[2]
    caminho_csv = base_dir / "data" / "sensores_fase2.csv"

    try:
        credenciais = carregar_env()
        df = carregar_csv(caminho_csv)
        total = importar_dados(df, credenciais)
        print(f"Importacao concluida. Total de registros: {total}")
    except FileNotFoundError as exc:
        print(f"Erro: {exc}")
    except oracledb.Error as exc:
        print(f"Erro de Oracle: {exc}")
    except Exception as exc:
        print(f"Erro inesperado: {exc}")


if __name__ == "__main__":
    main()
