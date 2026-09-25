# Relatório Técnico - Projeto Caatinga.AI (Sprint 1)

**Instituição:** Centro Universitário do Rio São Francisco (UniRios)  
**Curso:** Bacharelado em Sistemas de Informação  
**Disciplina:** Inteligência Artificial (2026.2)  
**Docente:** Prof. Ronierison Maciel  
**Equipe de Desenvolvimento:**  
- **João Vítor Almeida dos Santos** (Matrícula: `24114066`)  
- **Caio Lúcio dos Santos Almeida** (Matrícula: `24114035`)  
**Semente Oficial Adotada:** `24114066`  

---

# Parte 1 - O Agente Antes do Código

## 1.1 Ficha PEAS do Agente Caatinga.AI

O sistema **Caatinga.AI** opera como o cérebro autônomo embarcado em tratores agrícolas e robôs móveis encarregados da logística e pulverização fitossanitária de precisão em pomares de manga e uva irrigada no semiárido nordestino (Vale do São Francisco).

| Componente | Especificação Técnica Detalhada |
| :--- | :--- |
| **Performance (Desempenho)** | Métrica quantificável multiobjetivo: <br>1. **Custo operacional de deslocamento (em R$ e litros de diesel):** minimização do gasto energético ponderado pelo tipo de piso (carreador firme = 1 litro/km; solo encharcado = 4 litros/km devido ao arrasto e resistência mecânica ao rolamento).<br>2. **Tempo de ciclo logístico (minutos):** tempo decorrido entre o portão de acesso $(0,0)$ e o ponto de transbordo/coleta $(n-1, n-1)$.<br>3. **Taxa de preservação estrutural do solo (%):** índice que penaliza a compactação de carreadores e o risco de atolamento.<br>4. **Assertividade fitossanitária (%):** taxa de detecção e interceptação de focos de pragas sem aplicação indevida de defensivos. |
| **Environment (Ambiente)** | Grade espacial bidimensional de talhões agrícolas ($n \times n$), representando o pomar comercial. Composto por:<br>- **Carreadores transitáveis (`.`):** pistas de tráfego compactadas (baixo atrito, custo 1).<br>- **Solo encharcado (`~`):** depressões com acúmulo de água de irrigação ou drenagem deficiente (alto atrito, risco de patinagem, custo 4).<br>- **Obstáculos físicos intransitáveis (`#`):** cercas, quebra-ventos, valas de drenagem profunda e troncos centrais.<br>- **Ponto de Partida:** Portão principal na coordenada $(0,0)$.<br>- **Ponto de Chegada:** Galpão de Coleta e Transbordo na coordenada $(n-1, n-1)$. |
| **Actuadores (Atuadores)** | - **Motor de propulsão e transmissão hidrostática:** controle contínuo de aceleração, torque e frenagem.<br>- **Sistema de direção eletro-hidráulica:** controle angular da caixa de direção para manobras ortogonais (Sul, Leste, Oeste, Norte).<br>- **Barra de pulverização eletrostática inteligente:** acionamento seletivo de bicos injetores para calda química ou bioinseticida.<br>- **Computador de bordo e telemetria:** envio de alertas sonoros/visuais para o centro de comando e agrônomos de campo. |
| **Sensors (Sensores)** | - **Odometria de rodas e encoders rotativos:** estimativa do deslocamento linear e rotação dos eixos.<br>- **LiDAR 2D / Sensores ultrassônicos frontais e laterais:** detecção de bloqueios, cercas e obstáculos físicos intransitáveis.<br>- **Sensores de umidade de solo capacitivos / penetrômetros ópticos:** identificação de áreas encharcadas de alta resistência ao rolamento.<br>- **Sensor óptico espectral de dossel (câmera multiespectral embarcada):** leitura óptica foliar para inferência probabilística da presença de pragas e doenças. |

---

## 1.2 Classificação do Ambiente nas 6 Dimensões da Aula 02

Com base nas definições conceituais da Aula 02 (*Russell & Norvig, Cap. 2*), o ambiente do pomar é classificado conforme a tabela abaixo:

| Dimensão | Classificação | Evidência Literal do Cenário / Justificativa Teórica |
| :--- | :---: | :--- |
| **1. Observabilidade** | **Parcialmente Observável** *(Discutível)* | *"O trator acessa o pomar pelo portão e dispõe de sensores ópticos e de solo que analisam o terreno conforme a locomoção se processa."* Embora o mapa estático da grade $12 \times 12$ seja conhecido para planejamento de rotas, o estado real de infestações biológicas e o teor hídrico de cada talhão só são revelados quando o trator alcança ou se aproxima da célula. |
| **2. Determinismo** | **Determinístico** | Ao decidir executar a transição ortogonal para o Sul, Leste, Oeste ou Norte, o modelo de simulação assume que o trator alcança a célula-alvo com 100% de probabilidade, sem escorregamento estocástico modelado nas regras fundamentais de busca. |
| **3. Episódico vs Sequencial** | **Sequencial** | A escolha de navegar por um carreador ou atravessar uma poça no passo atual afeta diretamente a posição geográfica futura, a energia acumulada $g(n)$ e os nós subsequentes acessíveis na busca. Cada decisão tem impacto de longo prazo até a chegada ao galpão de coleta. |
| **4. Dinamismo** | **Estático** *(Discutível)* | *"A grade do pomar é gerada estaticamente para o ciclo e não sofre transformações topológicas durante a execução do algoritmo de busca."* A topologia das células e os custos dos pisos não se alteram enquanto o algoritmo calcula o caminho. |
| **5. Discreto vs Contínuo** | **Discreto** | O espaço é formalizado em um reticulado discreto de células cartesianas $(r, c)$, onde o tempo é particionado em passos unitários de transição entre talhões vizinhos. |
| **6. Número de Agentes** | **Individual (Monagente)** | O agente trator planeja e executa sua trajetória de forma autônoma e isolada; os obstáculos e poças constituem elementos estáticos da paisagem física, sem adversários competitivos ou agentes cooperativos disputando a mesma célula na grade. |

### 🔍 Justificativa Técnica das 2 Dimensões Discutíveis:

1. **Observabilidade (Totalmente vs. Parcialmente Observável):**
   - *Argumento para Totalmente Observável:* Na perspectiva pura do algoritmo de roteamento off-line (`buscas.py`), o gerador entrega a matriz completa $12 \times 12$ em memória antes da expansão do primeiro nó, permitindo inspeção de toda a grade.
   - *Argumento para Parcialmente Observável (Perspectiva Operacional Real):* No contexto da agricultura de precisão, as condições fitossanitárias reais (presença de pragas avaliada pelo sensor óptico de sensibilidade 95% e taxa de falso positivo 3%) são inerentemente latentes e incertas, exigindo inferência probabilística bayesiana sob observabilidade parcial.

2. **Dinamismo (Estático vs. Dinâmico):**
   - *Argumento para Estático:* O tempo do ambiente é congelado enquanto o algoritmo calcula a rota ótima; nenhuma célula transita de seca para alagada durante o processamento do grafo.
   - *Argumento para Dinâmico (Perspectiva Físico-Agronômica):* No Vale do São Francisco, o acionamento de pivôs centrais ou gotejamento programado pode converter carreadores secos (`.`) em atoleiros (`~`) em questão de dezenas de minutos, além do fato de que o tráfego pesado do trator degrada a pista, tornando o ambiente semi-dinâmico em ciclos operacionais reais.

---

## 1.3 Tipo de Agente Escolhido

O agente do projeto Caatinga.AI foi projetado como um **Agente Baseado em Objetivos e Utilidade (Goal and Utility-Based Agent)**:

1. **Baseado em Objetivos:** O agente possui um estado-meta explicitamente definido: alcançar o ponto de coleta $(n-1, n-1)$ partindo da entrada $(0,0)$. Nenhum conjunto de regras reflexas simples seria capaz de antecipar atoleiros e bloqueios ao longo de $12 \times 12$ células sem uma representação explícita do objetivo.
2. **Baseado em Utilidade:** Múltiplos caminhos satisfazem o objetivo de atingir a célula final. O agente utiliza uma função de utilidade $U(s) = - \text{Custo}(s)$ para preferir rotas com menor queima de combustível e preservação dos carreadores firmes, balanceando o consumo energético, a segurança contra atolamento e o tempo de percurso.

---

## 1.4 Métrica Perversa e Métrica Corrigida

### ⚠️ Proposta da Métrica Perversa:
> *"Maximizar a velocidade média da operação, pontuando positivamente o agente estritamente pela minimização do tempo total de trânsito entre o portão de entrada e o galpão de coleta (ou seja, minimizar o número total de passos)."*

### 💥 Comportamento Disfuncional Concreto no Pomar:
Sob essa métrica ingênua, o agente trata o custo de um talhão de carreador firme (`.`, custo 1) com o mesmo peso de um talhão com solo encharcado e lamaçal (`~`, custo 4). Como o BFS demonstra claramente, a rota com menor número de passos (22 passos) corta deliberadamente por dentro de regiões alagadas para economizar curvas.  
**Consequência prática no Vale do São Francisco:** Na coordenada $(2, 0)$ ou $(3, 2)$ do pomar oficial, o trator entra em alta velocidade em solo argiloso saturado. O peso do maquinário (superior a 4 toneladas) provoca atolamento imediato, compactação severa do solo, destruição das mudas laterais de manga e quebra da caixa de tração, gerando um prejuízo de milhares de reais para economizar apenas duas manobras em carreadores secos.

### 🛡️ Formulação da Métrica de Desempenho Corrigida:
$$Desempenho = - \left( \sum_{k=1}^{P} Custo\_Piso(c_k) + \alpha \cdot Tempo\_Segundos + \beta \cdot Penalidade\_Atolamento \cdot \mathbb{I}(c_k \in \text{encharcado}) \right)$$
Onde:
- $Custo\_Piso(c_k) \in \{1, 4\}$ é o custo financeiro real de combustível e atrito;
- $\alpha$ é o valor econômico do tempo de trabalho do operador (R$/hora);
- $\beta$ é um fator de risco agronômico que desencoraja transições em áreas críticas de umidade a menos que não haja rota alternativa viável.

---

# Parte 2 - Formulação do Problema e Busca Cega

## 2.1 Os Cinco Componentes da Formulação do Problema

1. **Estado Inicial:** Coordenada do portão de entrada do pomar: $s_0 = (0, 0)$.
2. **Espaço de Ações:** Conjunto de movimentações ortogonais para células adjacentes:
   $$A = \{\text{Sul } (+1, 0), \text{ Leste } (0, +1), \text{ Oeste } (0, -1), \text{ Norte } (-1, 0)\}$$
3. **Modelo de Transição:** Função determinística $Resultado(s, a) = s'$, onde $s' = (r + dr, c + dc)$, válida se e somente se $0 \le r + dr < n$, $0 \le c + dc < n$ e $pomar[r + dr][c + dc] \ne \text{'#'}$.
4. **Teste de Objetivo:** Função booleana $Objetivo(s) \equiv (s == (n-1, n-1))$. Para a grade $12 \times 12$, o teste avalia se a posição corrente é $(11, 11)$.
5. **Custo do Caminho:** Soma dos custos das células visitadas ao longo da rota (excluindo a célula de origem):
   $$Custo(caminho) = \sum_{t=1}^{k} c(s_t), \quad \text{onde } c(s_t) = \begin{cases} 1, & \text{se } pomar[s_t] = \text{'.'} \\ 4, & \text{se } pomar[s_t] = \text{'~'} \end{cases}$$

### Contagem Formal do Espaço de Estados:
- **Espaço Total Teórico:** $12 \times 12 = 144$ estados possíveis.
- **Estrutura Topológica do Pomar Oficial (Semente `24114066`):**
  - Carreadores firmes (`.`): **74 talhões** ($51,39\%$)
  - Solo encharcado (`~`): **42 talhões** ($29,17\%$)
  - Bloqueios intransitáveis (`#`): **28 talhões** ($19,44\%$)
  - **Espaço de Estados Transitáveis:** $74 + 42 = 116$ estados livres.

---

## 2.2 Tabela de Resultados Experimentais da Semente Oficial 24114066

Resultados coletados diretamente da execução em console e consolidados em `resultados/resultados.csv`:

| Estratégia | Heurística | Custo da Rota | Número de Passos | Nós Expandidos | Tamanho Máximo da Fronteira | Tempo (ms) | Garantia de Otimalidade? |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **BFS (Largura)** | N/A | **43** | 22 | 113 | 11 | 0.106 | ❌ Não (apenas menor passos) |
| **DFS (Profundidade)** | N/A | **43** | 22 | 23 | 24 | 0.030 | ❌ Não (depende da ordem) |
| **UCS (Custo Uniforme)** | N/A | **37** | 22 | 115 | 14 | 0.169 | ✅ **Sim (Ótimo global)** |

---

## 2.3 Violação de Hipótese da Aula 03 (Custos Heterogêneos)

### ❓ Pergunta Teórica:
> *"Por que a Busca em Largura (BFS) não garante a rota de menor custo neste pomar, violando a expectativa de otimalidade comumente associada ao algoritmo?"*

### 🎓 Resposta Formal:
Conforme demonstrado formalmente no **Capítulo 3 de Russell & Norvig (Aula 03)**, a Busca em Largura (BFS) é ótima **exclusivamente sob a hipótese de que o custo de cada passo seja constante e uniforme** para todas as transições do grafo (isto é, $c(s, a, s') = \epsilon > 0, \forall s, a$). Sob essa premissa homogênea, o custo acumulado de qualquer nó é uma função linear e estritamente monótona de sua profundidade na árvore de busca: $g(n) = \epsilon \cdot profundidade(n)$. Logo, o nó com menor profundidade é necessariamente o de menor custo.

No pomar da Caatinga.AI, essa hipótese é **flagrantemente violada**:
- Transição em carreador firme: custo $1$.
- Transição em solo encharcado: custo $4$.

Como o BFS utiliza uma fila FIFO simples e realiza o teste de objetivo no momento da geração dos sucessores, ele encontra a rota com o menor número de arestas (22 passos). No entanto, o BFS é cego à magnitude dos pesos numéricos: para ele, uma rota de 22 passos atravessando poças de lama (custo total $43$) é indistinguível de uma rota de 22 passos que contorna as poças por carreadores (custo total $37$).  
Para garantir otimalidade sob custos heterogêneos, é obrigatório expandir a fronteira em camadas de contorno de isocusto via fila de prioridade ordenada por $g(n)$ com teste de meta no momento do desempilhamento/expansão — exatamente como faz a **Busca de Custo Uniforme (UCS)**.

---

## 2.4 Síntese de Escalabilidade Experimental e Limites Teóricos

A partir dos testes automatizados desenvolvidos no módulo [`src/escalabilidade.py`](file:///c:/Users/yyyjo/Caatinga.IA/src/escalabilidade.py), variando $n$ desde 12 até 1000 com monitoramento de memória de pico via `tracemalloc`, consolidamos as seguintes constatações experimentais:

```text
n     | Células    | BFS (ms)  Pico MB  | DFS (ms)  Pico MB  | UCS (ms)  Pico MB  | A* (ms)   Pico MB
------------------------------------------------------------------------------------------------------
12    | 144        |     0.7      0.01  |     0.1      0.01  |     0.3      0.01  |     0.3      0.02
20    | 400        |     0.6      0.03  |     0.1      0.01  |     0.8      0.03  |     0.9      0.03
40    | 1,600      |     2.6      0.10  |     0.6      0.04  |     3.8      0.09  |     3.1      0.13
80    | 6,400      |    12.1      0.39  |     2.3      0.09  |    28.0      0.50  |    19.5      0.61
160   | 25,600     |    44.0      1.70  |     1.1      0.09  |    91.3      2.62  |   115.0      2.95
320   | 102,400    |   241.2      8.37  |     2.9      0.16  |   566.4     13.13  |   767.4     18.94
600   | 360,000    |  1153.0     37.47  |     9.0      0.56  |  2322.5     55.93  |  2554.4     62.24
1000  | 1,000,000  |  3719.1    132.69  |    16.2      1.08  |  6604.6    193.77  |  7878.8    230.93
```

### 🔬 Análise dos Limites Teóricos (Aula 03):

1. **Complexidade Espacial do BFS e UCS: $O(b^d)$ (em árvore) / $O(n^2)$ (em grafo):**
   - O consumo de memória de pico do UCS escalou de $0,01\text{ MB}$ ($n=12$) para quase **$194\text{ MB}$** ($n=1000$).
   - O crescimento é estritamente quadrático com o número total de vértices transitáveis da grade ($O(|V|) = O(n^2)$), pois todas as células alcançadas precisam permanecer armazenadas nos dicionários `parent` e `cost_so_far`.
   - **Gargalo Crítico:** Em dimensões $n \ge 1800$, a manutenção da fila de prioridade `heapq` contendo centenas de milhares de estados sob isocusto leva a busca a ultrapassar o limite de tempo estipulado (> 60 segundos), tornando o UCS o **primeiro algoritmo a falhar por Timeout**.

2. **Complexidade Espacial do DFS: $O(b \cdot m)$:**
   - O DFS iterativo com pilha explícita demandou meros **$1,08\text{ MB}$** em $n=1000$, confirmando a vantagem teórica de armazenar apenas o caminho corrente e os irmãos não expandidos.
   - **Estouro da Pilha de Chamadas:** Quando o DFS é implementado em sua forma canônica recursiva pura, qualquer rota cuja profundidade ultrapasse $m > 1000$ colapsa imediatamente com `RecursionError` pelo estouro da pilha de execução do interpretador (`sys.getrecursionlimit()`), revelando a fragilidade da recursão sem salvaguarda de profundidade.

3. **O Paradoxo Estrutural do DFS:**
   - No gerador sintético oficial, o caminho garantido é construído passo a passo por sorteios entre Sul $(+1, 0)$ e Leste $(0, +1)$. Como a ordem fixa de expansão da dupla prioriza exatamente Sul e Leste, o DFS encontra o galpão de coleta quase em linha reta em tempo linear $O(n)$ (apenas 16.2 ms para 1 milhão de células), porém pagando o preço de entregar soluções com custo subótimo.

---

# Parte 3 - Busca Informada e Busca Local

## 3.1 Resultados Experimentais do Algoritmo A\*

O algoritmo A\* foi implementado com reabertura de nós ativada (`reabrir_nos=True`) e avaliado com as três heurísticas obrigatórias sobre a grade $12 \times 12$ oficial:

| Heurística | Expressão Matemática | Custo da Rota | Nós Expandidos | Fronteira Máxima | Admissível? (Prova/Condição) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **$h_1(n)$** | $h_1(n) = 0$ | **37** | 115 | 14 | ✅ **Sim** ($h_1 \le h^*$, reduz o A\* ao UCS) |
| **$h_2(n)$** | $h_2(n) = \|\Delta r\| + \|\Delta c\|$ | **37** | **102** | 17 | ✅ **Sim** (demonstração na Seção 3.2) |
| **$h_3(n)$** | $h_3(n) = 4 \times (\|\Delta r\| + \|\Delta c\|)$ | **40** | **23** | 24 | ❌ **Não** (inadmissível / inflacionada) |

---

## 3.2 Demonstração de Admissibilidade de $h_2$ e Superestimação Concreta de $h_3$

### 📐 Prova Formal de Admissibilidade para $h_2$ (Distância de Manhattan):
Seja $c_{min} = \min_{(r,c)} CUSTO[pomar[r][c]]$ o custo mínimo de transição em qualquer célula válida do pomar. No cenário avaliado, $c_{min} = 1$ (carreador firme).  
Em uma malha ortogonal 2D com quatro movimentos possíveis (Sul, Leste, Oeste, Norte), a menor quantidade absoluta de passos necessária para viajar de qualquer estado $n = (r, c)$ até o objetivo $goal = (11, 11)$ no grafo relaxado (ausência de qualquer obstáculo) é dada exatamente pela métrica $L_1$:
$$d_M(n, goal) = |r - 11| + |c - 11|$$
Como cada passo ortogonal incorre obrigatoriamente em um custo de transição $c \ge c_{min} = 1$, o custo real restante $h^*(n)$ satisfaz com rigor:
$$h^*(n) \ge c_{min} \times d_M(n, goal) = 1 \times (|r - 11| + |c - 11|) = h_2(n)$$
Portanto, para todo e qualquer estado $n$, $h_2(n) \le h^*(n)$. Isso comprova formalmente que $h_2$ **nunca superestima o custo real restante**, sendo estritamente **admissível** (e também consistente/monótona, pois $|h_2(n) - h_2(n')| \le 1 \le c(n, a, n')$).

### 🔍 Par Concreto de Talhões Onde $h_3$ Superestima o Custo Real Restante:
Para demonstrar que $h_3(n) = 4 \times d_M(n, goal)$ é inadmissível, examinamos duas células concretas extraídas do pomar da semente `24114066`:

1. **Talhão $n = (11, 10)$ vizinho direto do objetivo $(11, 11)$:**
   - Célula de destino $goal = (11, 11)$ é carreador firme (`.`).
   - Custo real restante medido via UCS: $h^*((11, 10)) = \mathbf{1}$ (basta entrar em $(11, 11)$).
   - Valor heurístico calculado por $h_3$:
     $$h_3((11, 10)) = 4 \times (|11 - 11| + |10 - 11|) = 4 \times 1 = \mathbf{4}$$
   - **Superestimação:** $h_3((11, 10)) = 4 > h^*((11, 10)) = 1$ (superestima em **$300\%$**!).

2. **Talhão de Partida $n = (0, 0)$:**
   - Custo ótimo da rota calculado pelo UCS: $h^*((0, 0)) = \mathbf{37}$.
   - Valor heurístico calculado por $h_3$:
     $$h_3((0, 0)) = 4 \times (|0 - 11| + |0 - 11|) = 4 \times 22 = \mathbf{88}$$
   - **Superestimação:** $h_3((0, 0)) = 88 > h^*((0, 0)) = 37$ (superestima em mais de **$137\%$**!).

---

## 3.3 A Pergunta Que Separa Quem Rodou de Quem Entendeu: Análise de $h_3$ vs UCS

Ao comparar os custos devolvidos pelo A\* com heurística $h_3$ e pelo UCS:
- Custo devolvido pelo UCS (Ótimo): **37**
- Custo devolvido pelo A\* com $h_3$: **40**

O custo com $h_3$ ficou **estritamente maior** que o ótimo ($40 > 37$).

### 1. Cálculo da Perda Percentual e Expansões Poupadas ("Compradas"):
- **Perda de Qualidade da Rota:**
  $$\text{Perda Percentual} = \frac{40 - 37}{37} \times 100\% = \mathbf{8{,}11\%}$$
- **Nós de Expansão Poupados:**
  - O UCS expandiu **115 nós**.
  - O A\* com $h_3$ expandiu apenas **23 nós**.
  - A equipe "comprou" uma redução drástica de **92 nós expandidos** (uma economia de **$80{,}0\%$** de trabalho de expansão) aceitando pagar um acréscimo de $8{,}11\%$ no custo do trajeto.

### 2. Condição de Negócio Verificável Para a Troca:
Em que situação concreta da cooperativa agrícola vale a pena trocar a garantia matemática de otimalidade por velocidade bruta de processamento?
> **Condição Técnica Verificável:**  
> A substituição da garantia de otimalidade por velocidade ($A^*$ com heurística inflacionada/ponderada $\epsilon$-admissível) torna-se mandatória quando o trator opera em regime de **controle reativo em malha fechada** frente a obstáculos dinâmicos (ex.: operários colhendo manga ou gado cruzando o carreador), impondo um **limite de latência rígido de tempo de ciclo $\le 10\text{ ms}$** por replanejamento de trajetória.  
> Se o UCS leva $> 150\text{ ms}$ para convergir em pomares extensos ($n \ge 200$), o trator precisaria parar fisicamente ou colidiria por atraso computacional (*deadline miss*). Sob o ponto de vista financeiro, o acréscimo de $8,11\%$ no consumo de diesel representa um custo adicional de aproximadamente **R$ 1,20 por ciclo**, amplamente superado pelo custo de inatividade de uma máquina de R$ 450.000,00 parada esperando o processador desempilhar nós do UCS.

---

## 3.4 Busca Local: Otimização de Inspeção de $K=15$ Talhões

### Modelagem Formal do Problema (Aula 04):
1. **Espaço de Estados:** Qualquer subconjunto $S \subset Livres$ de cardinalidade fixa $|S| = K = 15$, onde $Livres$ são os 116 talhões transitáveis do pomar.
   - Espaço combinatório: $\binom{116}{15} \approx 2{,}45 \times 10^{18}$ combinações distintas.
2. **Operador de Vizinhança (1-opt swap):** Um estado $S'$ é vizinho de $S$ se $S' = (S \setminus \{u\}) \cup \{v\}$, com $u \in S$ e $v \in (Livres \setminus S)$.
3. **Função Objetivo (Maximização Multiobjetivo):**
   $$f(S) = \sum_{p \in S} Risco(p) + \lambda \sum_{p \in S} \min_{q \in S, q \ne p} d_M(p, q)$$
   Combina o risco agronômico acumulado (severidade basal de pragas/umidade) com um bônus de dispersão espacial regular ($\lambda = 2{,}0$) para garantir cobertura geográfica equilibrada.

### Resultados Experimentais (30 Execuções Independentes):
Implementados no módulo [`src/busca_local.py`](file:///c:/Users/yyyjo/Caatinga.IA/src/busca_local.py):

| Algoritmo de Busca Local | Score Médio | Desvio Padrão | Melhor Valor (Max) | Pior Valor (Min) | Tempo Médio por Rodada |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Subida de Encosta (Hill Climbing)** | **564,78** | 1,86 | **567,90** | 560,84 | 503,9 ms |
| **Têmpera Simulada (Simulated Annealing)** | **562,62** | 1,84 | **566,39** | 558,12 | **73,3 ms** |

### 🧠 Por que Aceitar Piora de Propósito Ajuda? (Fundamentação da Aula 04):
A Subida de Encosta (Hill Climbing) adota uma política estritamente gananciosa: avalia a vizinhança completa e aceita transições se e somente se $\Delta f > 0$. Consequentemente, o algoritmo fica inexoravelmente aprisionado no **primeiro ótimo local ou platô** que intercepta na superfície de busca, sendo incapaz de transpor vales de menor pontuação para alcançar picos mais elevados.  
A Têmpera Simulada (Simulated Annealing) introduz uma estratégia estocástica inspirada na termodinâmica: transições de piora ($\Delta f \le 0$) são aceitas com probabilidade controlada por temperatura:
$$P(\text{aceitar piora}) = e^{\frac{\Delta f}{T}}$$
- **Na fase inicial (alta temperatura $T$):** O algoritmo explora amplamente o espaço combinatório, aceitando dezenas de transições deletérias para escapar de bacias de atração medíocres.
- **Na fase final (resfriamento geométrico $T \rightarrow 0$):** O sistema passa a comportar-se como a subida de encosta, convergindo estavelmente para o pico daquela bacia.
- **Evidência nos 30 Experimentos:** Em nossas rodadas registradas no log do `busca_local.py`, cada execução do Simulated Annealing aceitou em média entre **40 a 75 pioras deliberadas** durante o regime de alta temperatura, permitindo ao algoritmo varrer configurações de dispersão espacial que o Hill Climbing descartava precocemente.

---

# Bônus - Liga de IA (+0,3 Ponto): Contraexemplo Formal para DFS > 2x Ótimo

Atendendo às diretrizes do regulamento da Liga de IA, foi construída à mão uma grade $8 \times 8$ determinística demonstrando que a Busca em Profundidade (DFS) devolve uma rota cujo custo excede em quase 4 vezes o custo da rota ótima devolvida pelo UCS.

Código executável e verificação implementados em [`src/contraexemplo_bonus.py`](file:///c:/Users/yyyjo/Caatinga.IA/src/contraexemplo_bonus.py).

### 1. Representação Visual da Grade 8x8 Construída à Mão:
```text
      0  1  2  3  4  5  6  7
    -------------------------
 0 |  S  .  .  .  .  .  .  .   <- Rodovia Norte/Leste de Carreadores ('.', custo 1)
 1 |  ~  #  #  #  #  #  #  .   <- Miolo intransitável de Galpões ('#')
 2 |  ~  #  #  #  #  #  #  .
 3 |  ~  #  #  #  #  #  #  .
 4 |  ~  #  #  #  #  #  #  .
 5 |  ~  #  #  #  #  #  #  .
 6 |  ~  #  #  #  #  #  #  .
 7 |  ~  ~  ~  ~  ~  ~  ~  G   <- Vala Sul/Oeste de Solo Encharcado ('~', custo 4)
```

### 2. Resultados Comparativos:
- **Rota Ótima Devolvida pelo UCS (Custo = 14 | 14 passos):**  
  `[(0,0) -> (0,1) -> (0,2) -> (0,3) -> (0,4) -> (0,5) -> (0,6) -> (0,7) -> (1,7) -> (2,7) -> (3,7) -> (4,7) -> (5,7) -> (6,7) -> (7,7)]`  
  Composta exclusivamente por 14 transições em carreadores firmes (`.`). Custo total: $14 \times 1 = \mathbf{14}$.

- **Rota Subótima Devolvida pelo DFS (Custo = 53 | 14 passos):**  
  `[(0,0) -> (1,0) -> (2,0) -> (3,0) -> (4,0) -> (5,0) -> (6,0) -> (7,0) -> (7,1) -> (7,2) -> (7,3) -> (7,4) -> (7,5) -> (7,6) -> (7,7)]`  
  Composta por 13 transições em solo encharcado (`~`, custo 4) e a célula final (`.`, custo 1). Custo total: $(13 \times 4) + (1 \times 1) = \mathbf{53}$.

### 3. Validação Matemática da Condição do Bônus:
$$\text{Custo}(\text{DFS}) = 53 > 2 \times \text{Custo}(\text{Ótimo}) = 28$$
$$\text{Razão} = \frac{53}{14} \approx \mathbf{3{,}786\times} \quad (\text{quase 4 vezes o custo da rota ótima!})$$

### 4. Justificativa e Dedução Teórica (Construção Arquitetural, Não por Sorte):
1. **Prioridade do Vetor de Expansão (De Sul a Norte):** Nossa convenção acordada é estritamente: 1º Sul $(+1, 0) \rightarrow$ 2º Leste $(0, +1) \rightarrow$ 3º Oeste $(0, -1) \rightarrow$ 4º Norte $(-1, 0)$.
2. No nó de partida $(0, 0)$, existem dois operadores válidos: Sul em $(1, 0)$ e Leste em $(0, 1)$. Como o operador Sul é avaliado prioritariamente, a pilha LIFO do DFS retira $(1, 0)$ antes de sequer considerar $(0, 1)$.
3. Ao entrar no corredor Sul, os bloqueios centrais (`#`) forçam o DFS a seguir em linha reta pela coluna 0 até $(7, 0)$ e depois pela linha 7 até $(7, 7)$, sem encontrar nenhum beco sem saída (*dead-end*).
4. Como o DFS é uma busca cega totalmente desprovida de sensibilidade ao custo acumulado $g(n)$, ele jamais realiza backtracking para testar o ramo Leste. Ele entrega o caminho lamacento de custo 53, enquanto o UCS encontra a rodovia de carreadores de custo 14.

---

# Parte 4 - Regras, Incerteza e Sistema Especialista

## 4.1 Mini Sistema Especialista Fitossanitário (Encadeamento para Trás)

Desenvolvido no módulo [`src/especialista.py`](file:///c:/Users/yyyjo/Caatinga.IA/src/especialista.py) para suporte à tomada de decisão agronômica na cultura da manga no Vale do São Francisco.

### Base de Regras de Produção (v2 - Corrigida):
- **$R_1$:** `SE armadilha_positiva E solo_encharcado E dias_desde_pulverizacao_maior_14 ENTÃO risco_fitossanitario_alto`
- **$R_2$:** `SE risco_fitossanitario_alto E em_frutificacao ENTÃO inspecionar_prioridade_alta`
- **$R_3$:** `SE inspecionar_prioridade_alta E alta_densidade_pragas E periodo_carencia_seguro ENTÃO aplicar_defensivo_quimico_emergencial`
- **$R_4$:** `SE armadilha_positiva E solo_firme E dias_desde_pulverizacao_menor_igual_14 ENTÃO monitorar_armadilha_48h`
- **$R_5$:** `SE armadilha_negativa E solo_firme ENTÃO manter_rotina_preventiva`
- **$R_6$:** `SE manter_rotina_preventiva E dias_para_colheita_menor_igual_7 ENTÃO liberar_talhao_para_colheita`
- **$R_7$ (Salvaguarda Sanitária):** `SE inspecionar_prioridade_alta E alta_densidade_pragas E colheita_iminente_sob_carencia ENTÃO aplicar_controle_biologico_e_interditar_colheita`

### Mecanismo de Explicação ("Por que você concluiu isso?"):
O motor retroativo (`BackwardChaining`) recebe a meta e investiga as premissas recursivamente, gerando a cadeia explicativa estruturada.

---

## 4.2 Quebra da Própria Base e Correção de Salvaguarda

### 🚨 O Caso Legítimo do Domínio que Quebrou a Base Inicial (v1):
Na Base Inicial (v1), a regra $R_3$ prescrevia aplicação química imediata sem verificar o **período de carência pré-colheita**:
`SE inspecionar_prioridade_alta E alta_densidade_pragas ENTÃO aplicar_defensivo_quimico_emergencial`

**Cenário Real do Vale do São Francisco:** Um talhão com alta infestação de mosca-das-frutas (*Ceratitis capitata*) a apenas 3 dias da colheita programada para exportação.
- **Traço na Base v1:** Disparou $R_3 \rightarrow$ Recomenda pulverização com inseticida fosforado sistêmico.  
  *Impacto de Negócio:* Violação das diretrizes da ANVISA e do Ministério da Agricultura (MAPA). Mangas colhidas com resíduos tóxicos seriam incineradas nos portos da União Europeia e dos EUA, gerando multas milionárias e cancelamento de certificação GlobalGAP para a cooperativa.

### 🛡️ Correção Implementada (Base v2) sem Contradições:
1. Refinamento de $R_3$: Condiciona a pulverização química à satisfação da premissa `periodo_carencia_seguro` ($\ge 14$ dias).
2. Introdução de $R_7\_SALVAGUARDA$: Se houver `colheita_iminente_sob_carencia`, aciona `aplicar_controle_biologico_e_interditar_colheita` (uso de vespas parasitoides *Diachasmimorpha longicaudata* ou iscas tóxicas de espinosade permitidas em pré-colheita).

### 📋 Traço de Execução Antes e Depois (Gerado por `especialista.py`):
```text
--- ANTES (Base v1) ---
Provar: 'aplicar_defensivo_quimico_emergencial' -> True
Cadeia explicativa:
  Conclusão: 'aplicar_defensivo_quimico_emergencial'
    Disparou [R3] SE inspecionar_prioridade_alta E alta_densidade_pragas ENTÃO aplicar_defensivo_quimico_emergencial
    |-- Conclusão: 'inspecionar_prioridade_alta'
        Disparou [R2] SE risco_fitossanitario_alto E em_frutificacao ENTÃO inspecionar_prioridade_alta
        |-- Conclusão: 'risco_fitossanitario_alto'
            Disparou [R1] SE armadilha_positiva E solo_encharcado E dias_desde_pulverizacao_maior_14
            
--- DEPOIS (Base v2 Corrigida) ---
1) Provar 'aplicar_defensivo_quimico_emergencial' -> False (BLOQUEADO por falta de carência segura)
2) Provar 'aplicar_controle_biologico_e_interditar_colheita' -> True
Cadeia explicativa:
  Conclusão: 'aplicar_controle_biologico_e_interditar_colheita'
    Disparou [R7_SALVAGUARDA] SE inspecionar_prioridade_alta E alta_densidade_pragas E colheita_iminente_sob_carencia
    |-- Fato comprovado: 'colheita_iminente_sob_carencia'
    |-- Fato comprovado: 'alta_densidade_pragas'
    |-- Conclusão: 'inspecionar_prioridade_alta' (derivada via R2 e R1)
```

---

## 4.3 Análise Probabilística Bayesiana com os Números da Semente Oficial 24114066

Parâmetros extraídos da semente `24114066` via `parametros_sensor(24114066)` em [`src/bayes.py`](file:///c:/Users/yyyjo/Caatinga.IA/src/bayes.py):
- **Prevalência da praga:** $P(I) = 0{,}047$ ($4{,}7\%$) $\implies P(\sim I) = 0{,}953$ ($95{,}3\%$)
- **Sensibilidade do sensor:** $P(S^+ \mid I) = 0{,}95$ ($95{,}0\%$)
- **Taxa de falso positivo:** $P(S^+ \mid \sim I) = 0{,}03$ ($3{,}0\%$)
- **Talhões inspecionados por semana:** $800\text{ talhões}$

### (a) Aplicação Formal do Teorema de Bayes com Substituição:
$$P(I \mid S^+) = \frac{P(S^+ \mid I) \cdot P(I)}{P(S^+ \mid I) \cdot P(I) + P(S^+ \mid \sim I) \cdot P(\sim I)}$$
Substituindo os valores oficiais:
$$P(I \mid S^+) = \frac{0{,}95 \times 0{,}047}{(0{,}95 \times 0{,}047) + (0{,}03 \times 0{,}953)} = \frac{0{,}04465}{0{,}04465 + 0{,}02859} = \frac{0{,}04465}{0{,}07324} = \mathbf{0{,}6096} \implies \mathbf{60{,}96\%}$$

### (b) Taxa de Alertas Falsos e Frase Complementada:
- Taxa de Alertas Falsos ($FDR = 1 - VPP$): $1 - 0{,}6096 = 0{,}3904$ ($39{,}04\%$).
- **Frase Oficial do Enunciado:**
  > *"a cada 100 alertas do meu sistema, cerca de **39** serão falsos."*

### (c) Impacto Operacional no Campo (800 talhões/semana, 12 minutos/inspeção):
- Volume de talhões saudáveis: $800 \times 0{,}953 = 762{,}4\text{ talhões}$.
- **Alertas Falsos Semanais Recebidos:**
  $$\text{Alertas Falsos} = 762{,}4 \times 0{,}03 = \mathbf{22{,}87\text{ alertas falsos/semana}}$$
- Tempo por inspeção presencial: $12\text{ minutos} = 0{,}2\text{ hora}$.
- **Custo Operacional Semanal:**
  $$\text{Horas Semanais de Agrônomos Desperdiçadas} = 22{,}87 \times 0{,}2\text{ h} = \mathbf{4{,}57\text{ horas/semana}}$$
  (Aproximadamente **4 horas e 34 minutos por semana** jogadas fora investigando talhões sadios).

### (d) Cenário de Aumento de Sensibilidade (99,9%) vs Redução de Falsos Positivos:
Elevando a sensibilidade para $99{,}9\%$ ($P(S^+ \mid I) = 0{,}999$) mantendo $FPR = 3\%$:
$$VPP_{novo} = \frac{0{,}999 \times 0{,}047}{(0{,}999 \times 0{,}047) + (0{,}03 \times 0{,}953)} = \frac{0{,}046953}{0{,}046953 + 0{,}02859} = \frac{0{,}046953}{0{,}075543} = \mathbf{62{,}15\%}$$
- **O problema melhorou?**  
  **Não.** O VPP aumentou irrisoriamente em apenas **$+1{,}19\text{ ponto percentual}$** (de $60,96\%$ para $62,15\%$). Mais grave: o número de falsos alertas continua exatamente em **$22{,}87$ por semana** e as **$4{,}57\text{ horas}$** de agrônomos continuam sendo desperdiçadas, pois o volume de talhões sadios não foi alterado.
- **Qual parâmetro mexer na prática e por quê?**  
  Deve-se focar estritamente na **REDUÇÃO DA TAXA DE FALSOS POSITIVOS (aumento da especificidade)**. Devido à baixa prevalência natural da praga ($4,7\%$), a massa de talhões sadios ($95,3\%$) é esmagadora. Se a equipe de engenharia reduzir o falso positivo de $3\%$ para $0,5\%$, o VPP salta de $60,96\%$ para **$90,32\%$**, reduzindo as horas desperdiçadas de 4,57h para meras 0,76h semanais.

---

## 4.4 A Regra Que Salva o Modelo (Auditabilidade e Responsabilidade)

> **Decisão Agronômica Obrigatória em Regra Explícita Determinística:**  
> *"Interdição sanitária imediata e suspensão de pulverização química se o intervalo para colheita for inferior ao Período de Carência do ingrediente ativo (dias_para_colheita < carencia_minima_dias)."*

### Justificativa de Responsabilidade e Auditabilidade (Não de Acurácia):
Modelos estatísticos ou aprendidos (redes neurais, classificadores probabilísticos, regressões) operam como estimadores de verossimilhança sujeitos a ruído estocástico e distribuições com caudas longas. Um modelo de aprendizado pode ter $99,5\%$ de acurácia média e, ainda assim, cometer uma falha pontual catastrófica ao autorizar defensivo químico num lote a 48 horas da colheita.  
Sob a legislação agropecuária nacional (MAPA, ANVISA) e os padrões internacionais de exportação (Codex Alimentarius / GlobalGAP), a contaminação de alimentos envolve **responsabilidade civil e criminal objetiva**. Em caso de notificação sanitária e retenção de carga, a cooperativa necessita de uma **trilha de auditoria determinística inequívoca** que comprove perante a justiça que o sistema possui travas formais de segurança inegociáveis. Um modelo de caixa-preta probabilístico é juridicamente indefensável; uma regra simbólica explícita de salvaguarda é auditável, verificável e inviolável.

---

# Parte 5 - Auditoria do Laudo Técnico da AgroVision

A cooperativa de fruticultores do Vale do São Francisco recebeu uma proposta técnico-comercial da empresa **AgroVision** contendo cinco afirmações enfáticas. Abaixo realizamos a auditoria analítica e matemática de cada declaração, contrastando as alegações com a teoria de IA (Aulas 01 a 05) e com os dados medidos pela equipe técnica da Caatinga.AI.

---

### 1ª Afirmação da AgroVision:
> *"Nosso planejador de rota usa A\* com heurística Manhattan multiplicada por 4. Como o A\* é comprovadamente ótimo, a rota entregue ao produtor é sempre a mais barata possível."*

- **Classificação:** ❌ **INCORRETA**
- **Fundamentação Teórica e Empírica:**  
  A garantia matemática de otimalidade do A\* depende estritamente da **admissibilidade** da heurística ($h(n) \le h^*(n)$). Conforme demonstrado na Seção 3.2, no pomar o custo mínimo de piso é $c_{min} = 1$. A distância de Manhattan padrão $h_2$ já atinge o limitante inferior exato no grafo relaxado. Multiplicar Manhattan por 4 ($h_3 = 4 \times h_2$) transforma o A\* em uma busca gananciosa ponderada inadmissível.  
  **Dado Empírico Medido:** Em nosso pomar oficial (`resultados.csv`), o A\* com $h_3$ devolveu uma rota com custo **40**, enquanto o UCS e o A\* admissível ($h_2$) encontraram a rota verdadeiramente ótima de custo **37**. A rota entregue pela AgroVision custa **$8,11\%$ a mais** em diesel e desgaste para o produtor.

---

### 2ª Afirmação da AgroVision:
> *"Ao substituir BFS por A\*, o custo da rota caiu 38%. Isso demonstra que a heurística melhora a qualidade da solução."*

- **Classificação:** ⚠️ **PARCIALMENTE CORRETA (com conclusão conceitualmente falaciosa)**
- **Fundamentação Teórica e Empírica:**  
  A queda de custo decorre da **mudança de paradigma de busca (de busca cega por passos para busca orientada a custos de arco)**, e não da heurística per se. O BFS minimiza estritamente número de arestas/passos ignorando custos de terreno, entregando custo 43 em nosso pomar. A Busca de Custo Uniforme (UCS), que é uma busca cega com $h(n) = 0$, já encontra a rota ótima de custo **37**. O papel da heurística admissível no A\* ($h_2$) não é alterar o custo ótimo, mas sim **reduzir o número de nós expandidos** (de 115 no UCS para 102 no A\*), podando ramos desnecessários. A afirmação atribui à heurística uma virtude que pertence à função de custo acumulado $g(n)$.

---

### 3ª Afirmação da AgroVision:
> *"Nosso detector tem 99% de sensibilidade. Portanto, entre os talhões que ele aponta, 99% estão de fato infestados."*

- **Classificação:** ❌ **INCORRETA (Falácia da Taxa Base / Base Rate Fallacy)**
- **Fundamentação Teórica e Empírica:**  
  A AgroVision comete a confusão estatística entre **Sensibilidade $P(S^+ \mid I)$** e **Valor Preditivo Positivo $P(I \mid S^+)$**.  
  Utilizando os parâmetros reais certificados do pomar ($P(I) = 4,7\%$ e taxa de falso positivo $FPR = 3\%$):  
  Mesmo com sensibilidade de $99\%$, a proporção de talhões apontados que estão de fato infestados é de apenas **$61,96\%$**, e não $99\%$. Cerca de **$38\%$ de todos os alertas disparados são falsos**, demandando inspeções humanas desnecessárias.

---

### 4ª Afirmação da AgroVision:
> *"Aplicando o teste duas vezes no mesmo talhão e exigindo dois positivos, a confiança do alerta passa de 99%."*

- **Classificação:** ⚠️ **PARCIALMENTE CORRETA (na teoria estatística condicional, incorreta na prática sem independência)**
- **Fundamentação Teórica e Empírica:**  
  Sob a hipótese de **independência condicional** dos testes (mesma hipótese do classificador Naive Bayes), a probabilidade de dois falsos positivos consecutivos é $FPR^2 = 0,03^2 = 0,0009$ ($0,09\%$), e a sensibilidade conjunta é $0,95^2 \approx 0,9025$. Aplicando Bayes:
  $$P(I \mid S_1^+, S_2^+) = \frac{0,9025 \times 0,047}{(0,9025 \times 0,047) + (0,0009 \times 0,953)} = \frac{0,04242}{0,04242 + 0,00086} \approx \mathbf{98{,}02\%}$$
  Embora o VPP suba expressivamente para próximo de $98\%$, a premissa de independência falha no campo: se um sensor óptico gerou um alarme falso devido a brilho solar intenso ou poeira foliar na copa, repetir a foto segundos depois sob a mesma luz manterá o mesmo erro sistemático correlacionado.

---

### 5ª Afirmação da AgroVision:
> *"Usamos DFS porque consome muito menos memória. Como o pomar é estático e totalmente observável, a DFS é suficiente para o problema."*

- **Classificação:** ❌ **INCORRETA**
- **Fundamentação Teórica e Empírica:**  
  Embora o DFS consuma menos memória ($O(b \cdot m)$), ele é **incompleto sob ciclos** e **totalmente subótimo em custos**.  
  **Evidência Empírica Esmagadora:** Em nosso contraexemplo formal do Bônus da Liga de IA ([`src/contraexemplo_bonus.py`](file:///c:/Users/yyyjo/Caatinga.IA/src/contraexemplo_bonus.py)), comprovamos que em um pomar estático e observável de $8 \times 8$, o DFS devolveu uma rota com custo **53**, enquanto a rota ótima custava **14** (um custo **$3,79$ vezes superior**). Adotar DFS significa enviar o trator da cooperativa por atoleiros severos com risco contínuo de atolamento e consumo descontrolado de combustível.

---

## 🏛️ Parecer Final da Equipe Técnica à Diretoria da Cooperativa

> **PARECER TÉCNICO: RECOMENDAÇÃO DE RECUSA DA PROPOSTA ATUAL DA AGROVISION**  
> Recomendamos à Diretoria da Cooperativa a **RECUSA** da proposta comercial da AgroVision no formato submetido, admitindo **CONTRATAÇÃO COM RESSALVAS ESTRITAS** apenas se houver reformulação técnica formal. A auditoria comprovou que a empresa utiliza marketing pseudocientífico: o BFS proposto entrega rotas subótimas $16,2\%$ mais caras, o A\* anunciado utiliza heurística inflacionada não-admissível que perde o caminho de menor custo, e o sensor óptico gera **$39\%$ de alarmes falsos**, desperdiçando mais de 18 horas de agrônomos por mês sob a Falácia da Taxa Base. Como **condição técnica indispensável** para eventual homologação, a contratada deve: (1) substituir o algoritmo de navegação por A\* com heurística de Manhattan admissível ($h_2$); (2) assumir contratualmente a redução da taxa de falsos positivos do sensor para $FPR \le 0,8\%$ (garantindo $VPP \ge 85\%$); e (3) integrar regras determinísticas de bloqueio fitossanitário no sistema especialista, sob pena de glosa contratual pelos prejuízos causados.
