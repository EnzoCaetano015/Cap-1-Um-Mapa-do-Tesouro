🌱 FarmTech Solutions – Sistema de Irrigação Inteligente (Fase 2)
📌 Descrição do Projeto
Este projeto implementa um sistema de irrigação automatizado utilizando ESP32 no Wokwi, com base em variáveis agrícolas simuladas.
O objetivo é tomar decisões inteligentes de irrigação considerando:
Umidade do solo (simulada via DHT22)
Níveis de nutrientes N, P e K (simulados via switches)
pH do solo (simulado via LDR)
Previsão de chuva (integrada via Python + API pública)
A proposta simula um cenário real de agricultura de precisão, onde múltiplos fatores influenciam a decisão de irrigar ou não.
---
🧠 Lógica do Sistema
A bomba de irrigação (relé) é acionada com base na seguinte regra:
SE:
Umidade está baixa
E
Solo está saudável (pH dentro da faixa + NPK presente)
E
Não há previsão de chuva forte
ENTÃO:
→ Liga a bomba de irrigação
---
⚙️ Componentes Utilizados
Componente	Função
ESP32	Controlador principal
DHT22	Simula umidade do solo e temperatura
LDR	Simula o pH do solo
3x Slide Switch	Simulam N, P e K
Relé	Simula a bomba de irrigação
Python + API	Previsão de chuva
---
🌡️ Sensor de Umidade (DHT22)
Representa a umidade do solo
Controla diretamente a necessidade de irrigação
Regra:
Umidade < 40% → solo seco → possível irrigação
---
🧪 Sensor de pH (LDR)
O LDR foi utilizado para simular o pH do solo.
Conversão:
pH = função calibrada baseada no valor analógico (0–4095)
Faixa ideal (tomate):
5.5 ≤ pH ≤ 7.5 → OK
Valores fora dessa faixa geram alerta e impedem irrigação.
---
🌿 Nutrientes NPK (Slide Switch)
Cada switch representa um nutriente:
N → Nitrogênio
P → Fósforo
K → Potássio
Estados:
ON → nutriente presente
OFF → nutriente ausente
Regra:
Todos ON → solo OK  
Qualquer OFF → solo com deficiência
---
☁️ Integração com API de Clima (Python)
Foi utilizada a API Open-Meteo para prever chuva.
Classificação:
Valor	Situação
0	Sem chuva
1	Chuva fraca
2	Chuva forte
Integração:
O valor retornado pelo Python é inserido manualmente no Serial Monitor do ESP32.
---
🔌 Comunicação via Serial
O ESP32 recebe o nível de chuva via teclado:
0 → sem chuva  
1 → chuva moderada  
2 → chuva forte
---
🚰 Lógica Final da Irrigação
Se chuva forte:
NÃO irriga
Se chuva moderada:
irriga apenas se umidade < 30% e solo OK
Se sem chuva:
irriga se umidade < 40% e solo OK
---
🧪 Testes Realizados
Cenário 1 – Ideal
Umidade: baixa
pH: OK
NPK: OK
Chuva: 0  
→ ✅ Bomba LIGADA
---
Cenário 2 – Chuva forte
Umidade: baixa
Solo: OK
Chuva: 2  
→ ❌ Bomba DESLIGADA
---
Cenário 3 – Solo ruim
Umidade: baixa
pH: fora da faixa  
→ ❌ Bomba DESLIGADA + alerta
---
Cenário 4 – Nutrientes faltando
NPK incompleto  
→ ❌ Bomba DESLIGADA
---
🎯 Diferencial do Projeto
Integração com API externa (clima)
Simulação de sensores agrícolas reais
Sistema baseado em múltiplas variáveis
Decisão automatizada inteligente
Uso de comunicação serial para entrada dinâmica
---
🧾 Estrutura do Projeto
sketch.ino → lógica do ESP32
diagram.json → circuito no Wokwi
clima.py → consulta API de previsão do tempo
libraries.txt → dependências
---
🚀 Como Executar
ESP32 (Wokwi)
Abrir o projeto no Wokwi
Rodar a simulação
Ajustar:
Umidade (DHT22)
LUX (LDR)
Switches NPK
Digitar no Serial:
0, 1 ou 2
---
Python
pip install requests
python clima.py
---
🧠 Conclusão
O sistema desenvolvido demonstra um modelo simplificado, porém funcional, de irrigação inteligente.
Ele integra:
sensores simulados
dados externos (clima)
regras de negócio
resultando em uma tomada de decisão automatizada mais eficiente e sustentável.
---
📌 Observações
O DHT22 simula umidade do ar, mas foi adaptado para solo
O LDR não mede pH real, sendo apenas uma aproximação didática
A integração com a API foi feita de forma semi-manual via Serial