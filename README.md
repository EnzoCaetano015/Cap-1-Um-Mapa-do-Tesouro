# FarmTech Solutions — Assistente Agrícola Inteligente

![Logo do projeto](img/logo.png)

## Sistema de irrigação inteligente com ESP32, Oracle, Python, Streamlit e Machine Learning

Este projeto simula uma solução de agricultura de precisão para monitoramento de solo, apoio à decisão de irrigação e geração de recomendações agrícolas. A base do sistema vem das leituras simuladas do protótipo ESP32/Wokwi e foi evoluída com persistência em Oracle, consultas SQL, dashboard em Streamlit, ingestão local em SQLite e modelos de Machine Learning.

O sistema trabalha com umidade, temperatura, pH, nutrientes NPK, previsão de chuva, status da irrigação e sugestões de manejo. A partir desses dados, é possível registrar leituras, consultar informações no banco, visualizar indicadores, treinar modelos preditivos e gerar recomendações de irrigação, correção de solo e fertilização.

---

## Objetivo

Construir um protótipo didático de agricultura inteligente que integra:

- sensores simulados no ESP32/Wokwi;
- regra de decisão para irrigação;
- armazenamento e consultas em banco Oracle;
- ingestão simulada de dados IoT em SQLite;
- dashboard em Python com Streamlit;
- modelos de regressão com Scikit-Learn;
- recomendador agrícola baseado nas previsões geradas.

---

## Estrutura atual do projeto

```text
.
├── api-clima/
│   └── clima.py
├── dashboard/
│   └── src/
│       ├── dashboard.py
│       └── importar_csv_oracle.py
├── data/
│   ├── sensores_fase2.csv
│   └── sensores_fase4_ml.csv
├── database/
│   └── ingestao_iot_sqlite.py
├── img/
│   ├── logo.png
│   ├── consultas-sql/
│   │   ├── consulta-1.png
│   │   ├── consulta-2.png
│   │   ├── consulta-3.png
│   │   ├── consulta-4.png
│   │   ├── consulta-5.png
│   │   ├── consulta-6.png
│   │   └── consulta-7.png
│   └── prototipo/
│       ├── image.png
│       └── image2.png
├── ml/
│   ├── recomendador.py
│   └── treinar_modelos.py
├── models/
│   ├── modelo_ph_previsto.joblib
│   ├── modelo_ph_previsto_meta.json
│   ├── modelo_produtividade_estimada.joblib
│   ├── modelo_produtividade_estimada_meta.json
│   ├── modelo_umidade_prevista.joblib
│   └── modelo_umidade_prevista_meta.json
├── prototipo-ESP32/
│   ├── src/
│   │   └── sketch.ino
│   ├── diagram.json
│   ├── platformio.ini
│   ├── PROTOTIPO.md
│   └── wokwi.toml
├── relatorios/
│   └── fase4/
│       └── metricas_modelos.csv
├── sql/
│   ├── 01_create_table.sql
│   ├── 02_consultas.sql
│   ├── 03_script_completo_oracle.sql
│   ├── 04_create_table_fase4_ml.sql
│   └── CONSULTAS_FARMTECH.md
├── .env.example
├── README.md
└── requirements.txt
```

---

## Papel de cada pasta

| Pasta/arquivo | Função |
|---|---|
| `api-clima/clima.py` | Consulta previsão de chuva por latitude e longitude e converte o resultado para o valor usado no ESP32. |
| `dashboard/src/dashboard.py` | Dashboard Streamlit com monitoramento, métricas de ML e previsão interativa. |
| `dashboard/src/importar_csv_oracle.py` | Importa `data/sensores_fase2.csv` para a tabela Oracle `FARMTECH_SENSOR_LEITURA`. |
| `data/sensores_fase2.csv` | Base original de leituras simuladas dos sensores. |
| `data/sensores_fase4_ml.csv` | Dataset gerado para treinamento e análise de Machine Learning. |
| `database/ingestao_iot_sqlite.py` | Simula ingestão de dados IoT em um banco SQLite local. |
| `img/consultas-sql/` | Evidências visuais das consultas SQL. |
| `img/prototipo/` | Imagens do protótipo ESP32/Wokwi. |
| `ml/treinar_modelos.py` | Gera dataset sintético, treina modelos de regressão e salva métricas. |
| `ml/recomendador.py` | Gera recomendações de manejo a partir das previsões dos modelos. |
| `models/` | Modelos `.joblib` treinados e metadados `.json`. |
| `prototipo-ESP32/` | Código, configuração e documentação da simulação ESP32. |
| `relatorios/fase4/metricas_modelos.csv` | Métricas MAE, MSE, RMSE e R² dos modelos treinados. |
| `sql/` | Scripts de criação de tabelas, consultas Oracle e documentação das consultas. |
| `.env.example` | Modelo das variáveis de ambiente para conexão Oracle. |
| `requirements.txt` | Dependências Python do projeto. |

---

## Tecnologias utilizadas

- Python
- Pandas
- NumPy
- Streamlit
- Scikit-Learn
- Joblib
- SQLite
- Oracle Database
- Oracle SQL Developer
- `oracledb`
- `python-dotenv`
- Requests
- ESP32
- Wokwi/PlatformIO

---

## Base de dados

O arquivo principal de entrada é:

```text
data/sensores_fase2.csv
```

Ele contém as leituras simuladas usadas no Oracle, no dashboard e como base para geração do dataset de ML.

| Coluna | Descrição |
|---|---|
| `data_hora` | Data e hora da leitura. |
| `umidade` | Umidade simulada do solo. |
| `temperatura` | Temperatura ambiente simulada. |
| `ph` | pH simulado do solo. |
| `n` | Presença de nitrogênio. `1 = presente`, `0 = ausente`. |
| `p` | Presença de fósforo. `1 = presente`, `0 = ausente`. |
| `k` | Presença de potássio. `1 = presente`, `0 = ausente`. |
| `nivel_chuva` | Nível de chuva previsto. `0 = sem chuva`, `1 = chuva fraca/moderada`, `2 = chuva forte`. |
| `status_irrigacao` | Status da bomba de irrigação: `LIGADA` ou `DESLIGADA`. |
| `sugestao` | Recomendação baseada nas condições simuladas. |

O treinamento de ML também gera:

```text
data/sensores_fase4_ml.csv
```

Esse arquivo adiciona variáveis-alvo como `umidade_prevista`, `ph_previsto` e `produtividade_estimada`.

---

## Regras de irrigação

A decisão de irrigação considera umidade, pH, nutrientes NPK e previsão de chuva.

```text
Chuva forte:
- A irrigação permanece desligada.

Chuva fraca ou moderada:
- Irriga somente se a umidade estiver muito baixa e o solo estiver adequado.

Sem chuva:
- Irriga se a umidade estiver baixa e o solo estiver adequado.

Solo inadequado:
- A irrigação permanece desligada até ajuste de pH ou nutrientes.
```

Na Fase 4, o recomendador também considera previsões de umidade, pH e produtividade para sugerir irrigação, correção de pH, fertilização NPK e nível de risco produtivo.

---

## Configuração do ambiente Python

### 1. Criar ambiente virtual

No Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

No Linux/Mac:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

---

## Configuração do Oracle

Crie um arquivo `.env` na raiz do projeto com base no `.env.example`:

```env
ORACLE_USER=seu_usuario
ORACLE_PASSWORD=sua_senha
ORACLE_DSN=oracle.fiap.com.br:1521/orcl
```

Exemplo usando RM:

```env
ORACLE_USER=RM000000
ORACLE_PASSWORD=sua_senha
ORACLE_DSN=oracle.fiap.com.br:1521/orcl
```

---

## Criar tabela e importar dados no Oracle

No Oracle SQL Developer, execute:

```text
sql/03_script_completo_oracle.sql
```

Esse script cria a tabela principal:

```sql
FARMTECH_SENSOR_LEITURA
```

Depois, para importar o CSV da Fase 2 para o Oracle:

```bash
python dashboard/src/importar_csv_oracle.py
```

Resultado esperado:

```text
Importacao concluida. Total de registros: 10
```

Para a tabela de previsões da Fase 4, use:

```text
sql/04_create_table_fase4_ml.sql
```

Esse script cria:

```sql
FARMTECH_ML_PREVISAO
```

---

## Consultas SQL

As consultas principais estão em:

```text
sql/02_consultas.sql
```

A documentação com explicação e imagens está em:

```text
sql/CONSULTAS_FARMTECH.md
```

As evidências visuais ficam em:

```text
img/consultas-sql/
```

---

## Treinar os modelos de Machine Learning

Execute na raiz do projeto:

```bash
python ml/treinar_modelos.py
```

Esse comando:

1. Lê `data/sensores_fase2.csv`.
2. Gera `data/sensores_fase4_ml.csv`.
3. Treina modelos para prever umidade futura, pH futuro e produtividade estimada.
4. Salva os modelos em `models/`.
5. Salva as métricas em `relatorios/fase4/metricas_modelos.csv`.

Arquivos gerados/atualizados:

```text
data/sensores_fase4_ml.csv
models/modelo_umidade_prevista.joblib
models/modelo_ph_previsto.joblib
models/modelo_produtividade_estimada.joblib
models/*_meta.json
relatorios/fase4/metricas_modelos.csv
```

As métricas avaliadas são:

- MAE;
- MSE;
- RMSE;
- R².

---

## Rodar a dashboard

Execute:

```bash
streamlit run dashboard/src/dashboard.py
```

O Streamlit abrirá no navegador, normalmente em:

```text
http://localhost:8501
```

A dashboard possui três abas:

| Aba | Conteúdo |
|---|---|
| `Monitoramento` | Indicadores da base de sensores, gráficos de umidade, pH, presença de P/K e tabela de sugestões. |
| `ML e métricas` | Métricas dos modelos, correlação entre variáveis e tendência de produtividade. |
| `Previsão interativa` | Formulário com sliders/selects para gerar previsões e recomendações em tempo real. |

Se os modelos ainda não existirem, execute primeiro:

```bash
python ml/treinar_modelos.py
```

---

## Ingestão IoT com SQLite

Para simular ingestão local de leituras IoT em banco SQL:

```bash
python database/ingestao_iot_sqlite.py
```

O script lê:

```text
data/sensores_fase2.csv
```

E cria/popula:

```text
database/farmtech_iot.db
```

A tabela local criada é:

```sql
leituras_iot
```

Durante a execução, cada leitura é inserida e exibida no terminal, simulando uma entrada contínua de dados.

---

## API de clima

Execute:

```bash
python api-clima/clima.py
```

Exemplo de entrada para São Paulo:

```text
Latitude: -23.55
Longitude: -46.63
```

Resultado esperado:

```text
Resultado da previsão: SEM CHUVA / CHUVA FRACA/MODERADA / CHUVA FORTE
VALOR PARA DIGITAR NO SERIAL DO WOKWI: 0, 1 ou 2
```

Valores usados no Monitor Serial do ESP32:

| Valor | Significado |
|---|---|
| `0` | Sem chuva |
| `1` | Chuva fraca/moderada |
| `2` | Chuva forte |

---

## Protótipo ESP32

A pasta do protótipo é:

```text
prototipo-ESP32/
```

O protótipo usa:

- ESP32;
- DHT22 para umidade e temperatura;
- LDR para simular pH;
- switches para N, P e K;
- relé para simular bomba de irrigação;
- entrada serial para nível de chuva.

No Monitor Serial, digite:

```text
0 = sem chuva
1 = chuva fraca/moderada
2 = chuva forte
```

A documentação visual do circuito está em:

```text
prototipo-ESP32/PROTOTIPO.md
```

---

## Fluxo técnico

```text
Sensores simulados no ESP32/Wokwi
        ↓
CSV estruturado em data/sensores_fase2.csv
        ↓
Oracle para persistência e consultas SQL
        ↓
SQLite para simulação de ingestão IoT local
        ↓
Pipeline de Machine Learning com Scikit-Learn
        ↓
Modelos treinados em models/
        ↓
Dashboard Streamlit
        ↓
Previsões e recomendações agrícolas
```

---

## Roteiro sugerido de teste completo

1. Criar e ativar o ambiente virtual.
2. Instalar dependências com `pip install -r requirements.txt`.
3. Configurar o `.env` com os dados do Oracle.
4. Executar `sql/03_script_completo_oracle.sql` no Oracle SQL Developer.
5. Executar `python dashboard/src/importar_csv_oracle.py`.
6. Rodar as consultas de `sql/02_consultas.sql`.
7. Conferir a documentação em `sql/CONSULTAS_FARMTECH.md`.
8. Executar `python ml/treinar_modelos.py`.
9. Executar `python database/ingestao_iot_sqlite.py`.
10. Executar `streamlit run dashboard/src/dashboard.py`.
11. Testar a aba `Previsão interativa`.
12. Executar `python api-clima/clima.py`.
13. Testar o valor retornado no Monitor Serial do ESP32.

---

## Roteiro sugerido para vídeo

Tempo máximo sugerido: 5 minutos.

1. Apresentar o objetivo do projeto.
2. Mostrar a estrutura de pastas atual.
3. Mostrar `data/sensores_fase2.csv` e `data/sensores_fase4_ml.csv`.
4. Mostrar o protótipo ESP32/Wokwi e a lógica de chuva no Serial.
5. Mostrar a criação/importação da tabela Oracle.
6. Mostrar consultas SQL e imagens em `img/consultas-sql/`.
7. Treinar os modelos com `python ml/treinar_modelos.py`.
8. Mostrar as métricas em `relatorios/fase4/metricas_modelos.csv`.
9. Rodar a ingestão SQLite.
10. Abrir a dashboard Streamlit e demonstrar as três abas.

---

## Conclusão

O projeto demonstra uma solução integrada de agricultura inteligente, conectando sensores simulados, regra de decisão de irrigação, armazenamento relacional em Oracle, ingestão SQL local, Machine Learning e visualização em dashboard.

A versão atual vai além do monitoramento básico: ela usa os dados agrícolas para prever condições futuras, estimar produtividade e sugerir ações de manejo, formando um protótipo de assistente agrícola inteligente.
