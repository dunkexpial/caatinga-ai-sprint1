# Relatório Técnico - Projeto Caatinga.AI (Sprint 1)

**Instituição:** Centro Universitário do Rio São Francisco (UniRios)  
**Curso:** Bacharelado em Sistemas de Informação  
**Disciplina:** Inteligência Artificial (2026.2)  
**Docente:** Prof. Ronierison Maciel  
**Equipe de Desenvolvimento:**  
- **João Vítor Almeida dos Santos** (Matrícula: `24114066`)  
- **Caio Lúcio dos Santos Almeida** (Matrícula: `24114068`)  
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
  - Carreadores firmes (`.`): **80 talhões** ($55,56\%$)
  - Solo encharcado (`~`): **36 talhões** ($25,00\%$)
  - Bloqueios intransitáveis (`#`): **28 talhões** ($19,44\%$)
  - **Espaço de Estados Alcançáveis (Transitáveis):** $80 + 36 = 116$ estados livres.

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

A partir dos testes automatizados desenvolvidos no módulo [`src/escalabilidade.py`](file:///c:/Projetos%20Faculdade/caatinga-ai-sprint1/src/escalabilidade.py), variando $n$ desde 12 até 1000 com monitoramento de memória de pico via `tracemalloc`, consolidamos as seguintes constatações experimentais:

```text
n     | Células    | BFS (ms)  Pico MB  | DFS (ms)  Pico MB  | UCS (ms)  Pico MB  | A* (ms)   Pico MB
------------------------------------------------------------------------------------------------------
12    | 144        |     0.2      0.02  |     0.0      0.01  |     0.3      0.02  |     0.3      0.02
40    | 1,600      |     2.1      0.14  |     0.5      0.02  |     3.4      0.14  |     4.7      0.15
160   | 25,600     |    36.7      2.20  |     0.9      0.09  |    64.7      2.50  |    61.5      2.40
600   | 360,000    |   565.9     48.10  |     4.4      0.40  |  1069.2     53.77  |  1285.2     51.20
1000  | 1,000,000  |  1780.1    172.50  |     7.9      1.20  |  3461.6    188.45  |  4860.9    182.10
```

### 🔬 Análise dos Limites Teóricos (Aula 03):

1. **Complexidade Espacial do BFS e UCS: $O(b^d)$ (em árvore) / $O(n^2)$ (em grafo):**
   - O consumo de memória de pico do UCS escalou de $0,02\text{ MB}$ ($n=12$) para quase **$190\text{ MB}$** ($n=1000$).
   - O crescimento é estritamente quadrático com o número total de vértices transitáveis da grade ($O(|V|) = O(n^2)$), pois todas as células alcançadas precisam permanecer armazenadas nos dicionários `parent` e `cost_so_far`.
   - **Gargalo Crítico:** Em dimensões $n \ge 1800$, a manutenção da fila de prioridade `heapq` contendo centenas de milhares de estados sob isocusto leva a busca a ultrapassar o limite de tempo estipulado (> 60 segundos), tornando o UCS o **primeiro algoritmo a falhar por Timeout**.

2. **Complexidade Espacial do DFS: $O(b \cdot m)$:**
   - O DFS iterativo com pilha explícita demandou meros **$1,20\text{ MB}$** em $n=1000$, confirmando a vantagem teórica de armazenar apenas o caminho corrente e os irmãos não expandidos.
   - **Estouro da Pilha de Chamadas:** Quando o DFS é implementado em sua forma canônica recursiva pura, qualquer rota cuja profundidade ultrapasse $m > 1000$ colapsa imediatamente com `RecursionError` pelo estouro da pilha de execução do interpretador, revelando a fragilidade da recursão sem salvaguarda de profundidade.

3. **O Paradoxo Estrutural do DFS:**
   - No gerador sintético oficial, o caminho garantido é construído passo a passo por sorteios entre Sul $(+1, 0)$ e Leste $(0, +1)$. Como a ordem fixa de expansão da dupla prioriza exatamente Sul e Leste, o DFS encontra o galpão de coleta quase em linha reta em tempo linear $O(n)$ (apenas 7.9 ms para 1 milhão de células), porém pagando o preço de entregar soluções com custo subótimo.

---

# Parte 5 - Auditoria do Laudo Técnico da AgroVision

A cooperativa de fruticultores do Vale do São Francisco recebeu uma proposta técnico-comercial da empresa **AgroVision** contendo cinco afirmações enfáticas. Abaixo realizamos a auditoria analítica e matemática de cada declaração, contrastando as alegações com a teoria de IA (Aulas 01 a 05) e com os dados medidos pela equipe técnica da Caatinga.AI.

---

### 1ª Afirmação da AgroVision:
> *"Nosso algoritmo de busca em largura (BFS) garante encontrar a rota ótima com o menor tempo de processamento, pois alcança o galpão de coleta no menor número possível de passos."*

- **Classificação:** ❌ **INCORRETA**
- **Fundamentação Teórica e Empírica:**  
  A afirmação confunde propositalmente **otimalidade de passos** com **otimalidade de custo financeiro/energético**. Como demonstrado na Aula 03 e comprovado empiricamente na Tabela da Seção 2.2:
  - O BFS encontrou uma rota de 22 passos com custo total **43**.
  - O UCS encontrou uma rota também de 22 passos com custo total **37**.  
  Como o custo dos talhões é heterogêneo (carreador = 1 vs. solo encharcado = 4), a rota do BFS resultou em um custo **$16,2\%$ superior ao ótimo**. O trator da AgroVision gastará mais óleo diesel e correrá risco severo de atolamento para entregar o mesmo número de passos.

---

### 2ª Afirmação da AgroVision:
> *"Multiplicar a distância de Manhattan por 4 na heurística do A\* ($h_3 = 4 \times h_2$) é uma inovação exclusiva da AgroVision que preserva a garantia de rota de menor custo e acelera a convergência."*

- **Classificação:** ❌ **INCORRETA**
- **Fundamentação Teórica e Empírica:**  
  A garantia matemática de que o A* devolve uma rota de custo ótimo repousa no teorema da **admissibilidade** (Aula 03): $h(n) \le h^*(n)$ para todo nó $n$.  
  - No pomar, o menor custo possível por passo em carreador firme é $c = 1$. Portanto, a distância de Manhattan padrão $h_2(n)$ já é o limitante inferior exato no grafo relaxado (admissível).
  - Ao inflacionar a heurística por 4 ($h_3(n) = 4 \cdot h_2(n)$), ela passa a superestimar grosseiramente o custo restante para qualquer caminho que transite por carreadores firmes.  
  **Dado Empírico:** Em nossos testes no pomar oficial (`resultados.csv`), o A* com $h_3$ devolveu uma rota com custo **40**, violando o custo ótimo descoberto pelo UCS e pelo A* com Manhattan admissível ($h_2$), cujo custo foi **37**. A AgroVision sacrificou a rota ótima por ganância desmedida na função de avaliação.

---

### 3ª Afirmação da AgroVision:
> *"Nosso sistema de navegação baseado em Busca de Custo Uniforme (UCS) é plenamente escalável para grandes fazendas de milhares de hectares sem demandar infraestrutura computacional pesada."*

- **Classificação:** ⚠️ **PARCIALMENTE CORRETA (com viés comercial enganoso)**
- **Fundamentação Teórica e Empírica:**  
  Embora o UCS garanta a rota ótima, sua complexidade de espaço em memória cresce exponencialmente em formulação de árvore e quadraticamente $O(n^2)$ em grafos de grade com busca completa.  
  **Dado Empírico:** Nossos testes em [`src/escalabilidade.py`](file:///c:/Projetos%20Faculdade/caatinga-ai-sprint1/src/escalabilidade.py) comprovam que para uma fazenda de porte moderado ($n = 1000$, grade de $1.000 \times 1.000 = 1.000.000$ de células), o UCS consumiu **$188,45\text{ MB}$ de memória RAM** e levou mais de **3,4 segundos** apenas para processar uma rota. Para fazendas com dezenas de milhares de talhões ($n \ge 3000$), a fila de prioridade do UCS extrapola os limites de memória embarcada de controladores industriais e excede timeouts de 60 segundos. A solução exigiria podas heurísticas dirigidas (como A* com heurística consistente), refutando a alegação de leveza computacional.

---

### 4ª Afirmação da AgroVision:
> *"Nosso sensor óptico possui 95% de sensibilidade comprovada em laboratório; portanto, quando o alerta dispara em um talhão, a cooperativa pode ter 95% de certeza de que há infestação de pragas, justificando a imediata mobilização de fiscais."*

- **Classificação:** ❌ **INCORRETA (Falácia da Taxa Base / Base Rate Fallacy)**
- **Fundamentação Teórica e Empírica:**  
  A AgroVision comete o erro estatístico mais clássico em diagnósticos de Inteligência Artificial: **confundir Sensibilidade $P(S^+ \mid I)$ com Valor Preditivo Positivo (VPP) $P(I \mid S^+)$**.  
  Utilizando os parâmetros certificados pelo gerador para a semente `24114066` no módulo [`src/bayes.py`](file:///c:/Projetos%20Faculdade/caatinga-ai-sprint1/src/bayes.py):
  - Prevalência real da praga: $P(I) = 4,7\%$ (talhões sadios: $P(I^c) = 95,3\%$).
  - Sensibilidade: $P(S^+ \mid I) = 95,0\%$.
  - Falso Positivo: $P(S^+ \mid I^c) = 3,0\%$.  
  Pelo **Teorema de Bayes**:
  $$P(I \mid S^+) = \frac{0,95 \times 0,047}{(0,95 \times 0,047) + (0,03 \times 0,953)} = \frac{0,04465}{0,07324} = \mathbf{60,96\%}$$
  - **Taxa Real de Alarmes Falsos (FDR):** $1 - 0,6096 = \mathbf{39,04\%}$.  
  A cada 100 alertas gerados pelo sensor da AgroVision, **cerca de 39 alertas são completamente falsos**. Para uma cooperativa inspecionando 800 talhões por semana, isso representa **22,87 alarmes falsos semanais** e um desperdício direto de **4,57 horas semanais de agrônomos** correndo atrás de pragas inexistentes.

---

### 5ª Afirmação da AgroVision:
> *"Caso a cooperativa deseje reduzir os alertas falsos residuais, basta contratar nosso módulo premium que eleva a sensibilidade do sensor para 99,9% via inteligência artificial."*

- **Classificação:** ❌ **INCORRETA**
- **Fundamentação Teórica e Empírica:**  
  Trata-se de uma tentativa comercial de venda casada inócua. O cálculo probabilístico executado em `src/bayes.py` demonstra:
  - Elevando a sensibilidade para $99,9\%$ enquanto a taxa de falsos positivos permanece em $3\%$, o novo VPP sobe de $60,96\%$ para **$62,15\%$** (um ganho marginal irrisório de apenas **$+1,19\text{ pontos percentuais}$**).
  - O volume de alarmes falsos em talhões sadios continua rigorosamente o mesmo: **$22,87\text{ alertas falsos/semana}$**, e as mesmas **$4,57\text{ horas/semana}$** de agrônomos continuam sendo jogadas no lixo.  
  **Razão Técnica:** A causa raiz dos alarmes falsos não é a falta de sensibilidade, mas sim a incidência da taxa de falso positivo ($3\%$) sobre a gigantesca massa de talhões saudáveis ($95,3\%$). O investimento técnico correto deve ser a **redução da taxa de falso positivo** (aumento da especificidade).

---

## 🏛️ Parecer Final da Equipe Técnica à Diretoria da Cooperativa

> **PARECER TÉCNICO: RECOMENDAÇÃO DE RECUSA DA PROPOSTA ATUAL DA AGROVISION**  
> Recomendamos à Diretoria da Cooperativa a **RECUSA** da proposta comercial da AgroVision no formato submetido, com opção de **CONTRATAÇÃO COM RESSALVAS ESTRITAS** apenas se houver readequação técnica formal. A auditoria comprovou que a empresa utiliza marketing pseudocientífico: o BFS proposto entrega rotas subótimas $16,2\%$ mais caras, o A* anunciado utiliza heurística inflacionada não-admissível que perde o caminho de menor custo, e o sensor óptico gera **$39\%$ de alarmes falsos**, desperdiçando mais de 18 horas de agrônomos por mês sob a Falácia da Taxa Base. Como **condição técnica indispensável** para eventual homologação, a contratada deve: (1) substituir o algoritmo de navegação por A* com heurística de Manhattan admissível ($h_2$); (2) assumir contratualmente a redução da taxa de falsos positivos do sensor para $FPR \le 0,8\%$ (garantindo $VPP \ge 85\%$); e (3) integrar regras determinísticas de bloqueio fitossanitário no sistema especialista, sob pena de glosa contratual pelos prejuízos causados.

---

*(As Partes 3, 4 e Bônus serão incorporadas pelo integrante João Vítor no Commit 10).*
