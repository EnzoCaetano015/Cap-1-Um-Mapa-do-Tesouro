from __future__ import annotations

import sqlite3
import time
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
DB_DIR = BASE_DIR / "database"
DB_PATH = DB_DIR / "farmtech_iot.db"


def conectar() -> sqlite3.Connection:
    DB_DIR.mkdir(exist_ok=True)
    return sqlite3.connect(DB_PATH)


def criar_tabela(conexao: sqlite3.Connection) -> None:
    conexao.execute(
        """
        CREATE TABLE IF NOT EXISTS leituras_iot (
            id_leitura INTEGER PRIMARY KEY AUTOINCREMENT,
            data_hora TEXT NOT NULL,
            umidade REAL NOT NULL,
            temperatura REAL NOT NULL,
            ph REAL NOT NULL,
            n INTEGER NOT NULL,
            p INTEGER NOT NULL,
            k INTEGER NOT NULL,
            nivel_chuva INTEGER NOT NULL,
            status_irrigacao TEXT NOT NULL,
            sugestao TEXT
        )
        """
    )
    conexao.commit()


def popular_banco(caminho_csv: Path | None = None, modo_continuo: bool = False) -> None:
    caminho_csv = caminho_csv or DATA_DIR / "sensores_fase2.csv"
    if not caminho_csv.exists():
        raise FileNotFoundError(f"CSV não encontrado: {caminho_csv}")

    df = pd.read_csv(caminho_csv)
    conexao = conectar()
    criar_tabela(conexao)
    conexao.execute("DELETE FROM leituras_iot")
    conexao.commit()

    print("Iniciando ingestão de dados IoT no SQLite...")
    for _, linha in df.iterrows():
        conexao.execute(
            """
            INSERT INTO leituras_iot
                (data_hora, umidade, temperatura, ph, n, p, k, nivel_chuva, status_irrigacao, sugestao)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                str(linha["data_hora"]),
                float(linha["umidade"]),
                float(linha["temperatura"]),
                float(linha["ph"]),
                int(linha["n"]),
                int(linha["p"]),
                int(linha["k"]),
                int(linha["nivel_chuva"]),
                str(linha["status_irrigacao"]),
                str(linha["sugestao"]),
            ),
        )
        conexao.commit()
        print(f"Leitura inserida: {linha['data_hora']} | Umidade={linha['umidade']} | pH={linha['ph']}")
        if modo_continuo:
            time.sleep(1)

    total = conexao.execute("SELECT COUNT(*) FROM leituras_iot").fetchone()[0]
    conexao.close()
    print(f"Ingestão concluída. Total de registros no banco: {total}")
    print(f"Banco gerado em: {DB_PATH}")


if __name__ == "__main__":
    popular_banco(modo_continuo=True)
