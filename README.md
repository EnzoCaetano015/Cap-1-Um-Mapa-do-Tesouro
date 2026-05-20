# FarmTech Solutions — Fase 3

![Logo do projeto](img/logo.png)

## Sistema de Irrigação Inteligente com Oracle, Python, Streamlit e ESP32

Este projeto simula uma solução de agricultura de precisão para monitoramento de solo e tomada de decisão sobre irrigação. A proposta evolui a Fase 2, que utilizava sensores simulados no ESP32/Wokwi, para a Fase 3, adicionando persistência em banco de dados relacional Oracle, consultas SQL e uma dashboard em Python.

O sistema trabalha com dados de umidade, temperatura, pH, nutrientes NPK, previsão de chuva e status da irrigação. A partir desses dados, é possível registrar leituras, consultar informações no banco e visualizar indicadores em uma dashboard.

---

## Objetivo da atividade

A atividade tem como objetivo explorar conceitos iniciais de banco de dados, usando os dados coletados/simulados pelos sensores da Fase 2 como base para importação em um banco relacional Oracle.

Além disso, o projeto também apresenta uma dashboard em Python para visualização dos dados agrícolas.

---

## Arquitetura do projeto

```text
.
├── api-clima/
│   └── clima.py
├── dashboard/
│   └── src/
│       ├── dashboard.py
│       └── importar_csv_oracle.py
├── data/
│   └── sensores_fase2.csv
├── img/
│   └── prototipo/
│       ├── image.png
│       └── image2.png
├── prints/
│   ├── print_01_tabela_criada.png
│   ├── print_02_select_todos_registros.png
│   ├── print_03_status_irrigacao.png
│   ├── print_04_medias_sensores.png
│   ├── print_05_leituras_criticas.png
│   ├── print_06_dashboard_geral.png
│   ├── print_07_dashboard_filtro_ligada.png
│   └── print_08_api_clima_terminal.png
├── prototipo-ESP32/
│   ├── src/
│   │   └── sketch.ino
│   ├── diagram.json
│   ├── platformio.ini
│   └── wokwi.toml
├── sql/
│   ├── 01_create_table.sql
│   ├── 02_consultas.sql
│   └── 03_script_completo_oracle.sql
├── .env.example
├── README.md
├── CONSULTAS.md
└── requirements.txt
```

---

## Papel de cada pasta

| Pasta/arquivo | Função |
|---|---|
| `api-clima/clima.py` | Consulta previsão de chuva usando API externa e retorna um nível de chuva para uso no ESP32. |
| `dashboard/src/dashboard.py` | Dashboard em Streamlit para visualizar os dados da Fase 2. |
| `dashboard/src/importar_csv_oracle.py` | Script Python responsável por importar o CSV para o banco Oracle. |
| `data/sensores_fase2.csv` | Base de dados usada na importação para o Oracle e na dashboard. |
| `img/prototipo/` | Imagens do protótipo ESP32/Wokwi. |
| `prints/` | Pasta para salvar os prints das consultas SQL, dashboard e testes. |
| `prototipo-ESP32/` | Código e configuração da simulação do ESP32 no Wokwi/PlatformIO. |
| `sql/` | Scripts SQL para criação da tabela, carga de exemplo e consultas. |
| `.env.example` | Modelo das variáveis de ambiente usadas na conexão Oracle. |
| `requirements.txt` | Dependências Python do projeto. |

---

## Tecnologias utilizadas

- Python
- Pandas
- Streamlit
- Oracle Database
- Oracle SQL Developer
- `oracledb`
- `python-dotenv`
- Requests
- ESP32
- Wokwi/PlatformIO

---

## Base de dados utilizada

O arquivo principal usado como base é:

```text
data/sensores_fase2.csv
```

Ele contém as seguintes colunas:

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

---

## Regras de irrigação usadas no projeto

A decisão de irrigação considera umidade, pH, nutrientes NPK e previsão de chuva.

Regras principais:

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

## Configuração do banco Oracle

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

Substitua os dados pelos acessos fornecidos pela FIAP.

---

## Como criar a tabela no Oracle

Abra o Oracle SQL Developer, conecte no banco e execute:

```text
sql/03_script_completo_oracle.sql
```

Esse script faz:

1. Remove a tabela anterior, caso exista.
2. Cria a tabela `FARMTECH_SENSOR_LEITURA`.
3. Cria constraints de validação.
4. Insere registros de exemplo.
5. Executa `COMMIT`.
6. Executa consultas de validação.

Tabela criada:

```sql
FARMTECH_SENSOR_LEITURA
```

---

## Como importar o CSV para o Oracle

Após criar a tabela, execute:

```bash
python dashboard/src/importar_csv_oracle.py
```

Resultado esperado no terminal:

```text
Importacao concluida. Total de registros: 10
```

Depois, no SQL Developer, valide com:

```sql
SELECT COUNT(*) AS TOTAL_REGISTROS
FROM FARMTECH_SENSOR_LEITURA;
```

---

## Atenção ao caminho do CSV

Como os scripts estão dentro de `dashboard/src/` e o CSV está em `data/`, o caminho correto deve subir duas pastas.

Nos arquivos:

```text
dashboard/src/dashboard.py
dashboard/src/importar_csv_oracle.py
```

Use:

```python
base_dir = Path(__file__).resolve().parents[2]
caminho_csv = base_dir / "data" / "sensores_fase2.csv"
```

Se estiver como `parents[1]`, o Python vai procurar o CSV em `dashboard/data/`, que não existe na arquitetura atual.

---

## Como executar a dashboard

Execute:

```bash
streamlit run dashboard/src/dashboard.py
```

O Streamlit abrirá no navegador, normalmente em:

```text
http://localhost:8501
```

A dashboard apresenta:

- média de umidade;
- média de temperatura;
- média de pH;
- total de leituras;
- quantidade de registros com irrigação ligada;
- gráfico de umidade ao longo do tempo;
- gráfico de pH ao longo do tempo;
- gráfico de presença de P e K;
- gráfico de status da irrigação;
- tabela com sugestões de irrigação.

Também existe um filtro por status:

```text
Todos
LIGADA
DESLIGADA
```

---

## Como testar a API de clima

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

Esse valor pode ser usado no Monitor Serial do ESP32:

| Valor | Significado |
|---|---|
| `0` | Sem chuva |
| `1` | Chuva fraca/moderada |
| `2` | Chuva forte |

---

## Como testar o protótipo ESP32

Abra a pasta:

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

O sistema deve mostrar no serial:

- chuva prevista;
- umidade;
- temperatura;
- pH;
- status de N, P e K;
- situação do solo;
- status da bomba.

---

## Consultas SQL

As consultas principais estão documentadas em:

```text
CONSULTAS.md
```

E o arquivo SQL original está em:

```text
sql/02_consultas.sql
```

Use essas consultas para gerar os prints obrigatórios da atividade.

---

## Prints recomendados

Salve os prints na pasta `prints/` com os seguintes nomes:

```text
print_01_tabela_criada.png
print_02_select_todos_registros.png
print_03_status_irrigacao.png
print_04_medias_sensores.png
print_05_leituras_criticas.png
print_06_dashboard_geral.png
print_07_dashboard_filtro_ligada.png
print_08_api_clima_terminal.png
```

Esses prints devem ser referenciados no `CONSULTAS.md` e podem ser usados no relatório final.

---

## Roteiro sugerido para teste completo

1. Abrir o projeto no VS Code.
2. Criar e ativar o ambiente virtual.
3. Instalar dependências com `pip install -r requirements.txt`.
4. Configurar o `.env` com os dados do Oracle.
5. Rodar `sql/03_script_completo_oracle.sql` no Oracle SQL Developer.
6. Executar `python dashboard/src/importar_csv_oracle.py`.
7. Rodar consultas do arquivo `sql/02_consultas.sql`.
8. Tirar prints das consultas.
9. Executar `streamlit run dashboard/src/dashboard.py`.
10. Tirar prints da dashboard.
11. Executar `python api-clima/clima.py`.
12. Testar o valor retornado no Monitor Serial do ESP32.

---

## Roteiro sugerido para vídeo

Tempo máximo: 5 minutos.

Sugestão de ordem:

1. Apresentar rapidamente o objetivo do projeto.
2. Mostrar a estrutura de pastas no VS Code.
3. Mostrar o arquivo `data/sensores_fase2.csv`.
4. Mostrar o script SQL criando a tabela no Oracle.
5. Rodar uma consulta no SQL Developer.
6. Executar o script de importação Python.
7. Abrir a dashboard Streamlit.
8. Mostrar gráficos e filtro de irrigação.
9. Executar a API de clima.
10. Mostrar rapidamente o protótipo ESP32/Wokwi.

---

## Conclusão

O projeto demonstra uma solução didática de agricultura inteligente integrando sensores simulados, regra de decisão para irrigação, armazenamento relacional em Oracle, scripts Python e visualização em dashboard.

A entrega atende aos pontos principais da atividade: uso de dados da Fase 2, importação para banco Oracle, consultas SQL com prints, códigos Python, documentação em Markdown e demonstração funcional por vídeo.
