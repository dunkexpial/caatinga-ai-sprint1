# Caatinga.AI — Documentação Completa do Projeto, Conceitos e Código

**Instituição:** Centro Universitário do Rio São Francisco (UniRios)  
**Curso:** Bacharelado em Sistemas de Informação  
**Disciplina:** Inteligência Artificial (2026.2)  
**Docente:** Prof. Ronierison Maciel  
**Autores:**  
- **João Vítor Almeida dos Santos** (Matrícula: `24114066`)  
- **Caio Lúcio dos Santos Almeida** (Matrícula: `24114068`)  
**Semente Oficial Adotada:** `24114066`  

---

## Sumário
1. [Visão Geral e Contexto do Projeto](#1-visão-geral-e-contexto-do-projeto)
2. [Conceitos Teóricos e Fundamentos](#2-conceitos-teóricos-e-fundamentos)
   - [2.1 Ficha PEAS do Agente](#21-ficha-peas-do-agente)
   - [2.2 Classificação nas 6 Dimensões do Ambiente](#22-classificação-nas-6-dimensões-do-ambiente)
   - [2.3 A Armadilha da Métrica Perversa e sua Correção](#23-a-armadilha-da-métrica-perversa-e-sua-correção)
   - [2.4 Formulação no Espaço de Estados](#24-formulação-no-espaço-de-estados)
   - [2.5 Buscas Cegas e o Teorema da Quebra do BFS](#25-buscas-cegas-e-o-teorema-da-quebra-do-bfs)
   - [2.6 Busca Informada A* e Admissibilidade Heurística](#26-busca-informada-a-e-admissibilidade-heurística)
   - [2.7 Otimização por Busca Local (K = 15 Talhões)](#27-otimização-por-busca-local-k--15-talhões)
   - [2.8 Sistema Especialista com Encadeamento para Trás (Backward Chaining)](#28-sistema-especialista-com-encadeamento-para-trás-backward-chaining)
   - [2.9 Incerteza, Sensores e Teorema de Bayes](#29-incerteza-sensores-e-teorema-de-bayes)
   - [2.10 Bônus da Liga de IA: Contraexemplo Formal 8x8 (DFS > 2x Ótimo)](#210-bônus-da-liga-de-ia-contraexemplo-formal-8x8-dfs--2x-ótimo)
   - [2.11 Auditoria Crítica do Laudo Técnico da AgroVision](#211-auditoria-crítica-do-laudo-técnico-da-agrovision)
3. [Explicação Detalhada do Código por Módulo](#3-explicação-detalhada-do-código-por-módulo)
   - [3.1 src/gerador_pomar.py](#31-srcgerador_pomarpy)
   - [3.2 src/buscas.py](#32-srcbuscaspy)
   - [3.3 src/busca_local.py](#33-srcbusca_localpy)
   - [3.4 src/especialista.py](#34-srcespecialistapy)
   - [3.5 src/bayes.py](#35-srcbayespy)
   - [3.6 src/escalabilidade.py](#36-srcescalabilidadepy)
   - [3.7 src/contraexemplo_bonus.py](#37-srccontraexemplo_bonuspy)
   - [3.8 src/main.py](#38-srcmainpy)
4. [Resultados Numéricos Oficiais Consolidados](#4-resultados-numéricos-oficiais-consolidados)
5. [Guia de Execução dos Comandos](#5-guia-de-execução-dos-comandos)

---

# 1. Visão Geral e Contexto do Projeto

O **Caatinga.AI** é uma solução de Inteligência Artificial aplicada ao agronegócio de precisão no semiárido brasileiro (Polo Petrolina-PE / Juazeiro-BA, no Vale do São Francisco). O projeto modela o cérebro autônomo de um veículo agrícola inteligente (trator autônomo ou robô de solo) encarregado da logística interna, transporte de colheita e monitoramento fitossanitário em pomares irrigados de manga e uva.

Em pomares do semiárido, a umidade proveniente de irrigação por gotejamento ou falhas de drenagem cria bolsões de solo encharcado que trazem dois grandes desafios:
1. **Desafio Mecânico/Energético:** Solo saturado de água possui alta resistência ao rolamento, patinagem de pneus e risco severo de atolamento do maquinário, gastando muito mais combustível diesel e danificando a estrutura do solo.
2. **Desafio Fitossanitário:** Áreas encharcadas favorecem a proliferação de fungos radiculares (*Phytophthora*) e pragas (mosca-das-frutas).

O sistema **Caatinga.AI** resolve de ponta a ponta esses desafios através de planejamento de trajetórias, seleção ótima de talhões de inspeção, diagnóstico causal de pulverização e análise probabilística de sensores.

---

# 2. Conceitos Teóricos e Fundamentos

## 2.1 Ficha PEAS do Agente

O projeto formaliza o trator inteligente segundo o paradigma de agentes racionais de Russell & Norvig (*Capítulo 2*):

- **Performance (Desempenho):** Métrica multiobjetivo mensurável:
  - Custo operacional de combustível/energia (ponderado: carreador firme = 1 litro/km; solo encharcado = 4 litros/km);
  - Tempo de ciclo logístico entre o portão de entrada `(0, 0)` e o galpão de coleta `(11, 11)`;
  - Índice de preservação estrutural do solo (penalização de compactação e atolamento);
  - Assertividade fitossanitária (eliminação de pragas sem contaminação química indevida).
- **Environment (Ambiente):** Grade $12 \times 12$ de talhões agrícolas, contendo:
  - Carreadores firmes (`.`): vias compactadas de baixo custo ($c = 1$);
  - Solo encharcado (`~`): áreas lamacentas de alto custo e atrito ($c = 4$);
  - Bloqueios intransitáveis (`#`): cercas, valas e quebra-ventos;
  - Portão de acesso em `(0, 0)` e Ponto de Coleta em `(11, 11)`.
- **Actuators (Atuadores):** Motor de propulsão e transmissão hidrostática (aceleração/frenagem), direção eletro-hidráulica (manobras ortogonais: Sul, Leste, Oeste, Norte), barra de pulverização inteligente (calda química ou biológica) e telemetria de bordo.
- **Sensors (Sensores):** Odometria de rodas/encoders de tração, LiDAR 2D/ultrassom (detecção de obstáculos físicos `#`), penetrômetro óptico/umidade de solo (identificação de áreas `~`) e câmera multiespectral foliar para detecção de pragas.

---

## 2.2 Classificação nas 6 Dimensões do Ambiente

1. **Observabilidade: Parcialmente Observável (Discutível):**
   - *Visão de Busca Pura:* O mapa estático da grade é carregado previamente em memória (Totalmente Observável para o roteador).
   - *Visão Operacional Agronômica:* A condição fitossanitária real e a presença de pragas em cada talhão são latentes e incertas, exigindo inferência bayesiana com base em leituras ruidosas de sensores ópticos.
2. **Determinismo: Determinístico:**
   - A cada comando de movimentação para uma célula adjacente livre, o trator alcança com 100% de certeza a coordenada destino, sem deslizamentos estocásticos modelados na grade base.
3. **Episódico vs. Sequencial: Sequencial:**
   - Cada decisão de rota afeta as opções futuras de manobra, o combustível remanescente $g(n)$ e a proximidade do objetivo.
4. **Dinamismo: Estático (Discutível):**
   - O algoritmo calcula a rota enquanto a grade permanece congelada no tempo; porém, no ciclo agronômico real, chuvas ou vazamentos em pivôs centrais podem transformar carreadores secos em lamaçal durante a operação.
5. **Discreto vs. Contínuo: Discreto:**
   - Estados representados por coordenadas inteiras discretas $(r, c)$ e ações particionadas em passos ortogonais unitários.
6. **Número de Agentes: Individual (Monagente):**
   - O trator opera de forma autônoma e isolada no pomar, tratando os demais elementos como parte do ambiente físico.

---

## 2.3 A Armadilha da Métrica Perversa e sua Correção

- **Métrica Perversa Proposta:** *"Minimizar o tempo de percurso (número de passos) entre o portão de entrada e o galpão de coleta."*
- **Comportamento Disfuncional Gerado:** Ao tratar todo talhão como de custo idêntico, o agente trator escolhe cruzar por dentro de grandes poças de solo encharcado (`~`) para economizar curvas. Com um maquinário pesado de 4 toneladas, o trator sofre atolamento severo, destruição de mudas laterais e compactação irreversível do solo argiloso.
- **Métrica Corrigida:**
  $$\text{Desempenho} = - \left( \sum_{k=1}^{P} \text{Custo}(c_k) + \alpha \cdot \text{Tempo} + \beta \cdot \text{Penalidade\_Atolamento} \cdot \mathbb{I}(c_k \in \text{encharcado}) \right)$$

---

## 2.4 Formulação no Espaço de Estados

Para a semente oficial `24114066`:
- **Espaço Total:** $12 \times 12 = 144$ estados.
- **Talhões Livres (Transitáveis):** **116 talhões** (80 carreadores `.` e 36 encharcados `~`).
- **Bloqueios Intransitáveis:** **28 talhões** (`#`).
- **Estado Inicial:** $s_0 = (0, 0)$.
- **Teste de Objetivo:** $s == (11, 11)$.
- **Ordem Fixa de Expansão (Invariante):** **1º Sul** `(+1, 0)`, **2º Leste** `(0, +1)`, **3º Oeste** `(0, -1)`, **4º Norte** `(-1, 0)`.

---

## 2.5 Buscas Cegas e o Teorema da Quebra do BFS

Conforme o **Capítulo 3 de Russell & Norvig**, a Busca em Largura (BFS) é matematicamente ótima **somente quando o custo de cada transição é constante e idêntico** ($c = \epsilon$).  
No pomar, o carreador custa **1** e a poça custa **4**. Logo, a premissa de custos homogêneos é violada:
- O **BFS** utiliza fila FIFO e teste de objetivo na geração, encontrando o menor número de passos (22 passos), mas com **custo 43** (rota repleta de lama).
- O **UCS (Busca de Custo Uniforme)** utiliza fila de prioridade ordenada por $g(n)$ e teste de objetivo na expansão, encontrando a rota de menor custo financeiro: **custo 37** (mesmos 22 passos, contornando a lama por carreadores firmes).
- O **DFS** é atraído pela ordem Sul/Leste e acha uma rota direta quase sem nós expandidos (apenas 23 nós), mas entrega **custo 43** (subótimo).

---

## 2.6 Busca Informada A* e Admissibilidade Heurística

O algoritmo A* seleciona nós na fronteira minimizando a função $f(n) = g(n) + h(n)$, onde $g(n)$ é o custo real acumulado e $h(n)$ é a estimativa heurística até a meta.

1. **Heurística Nula $h_1(n) = 0$:**
   - Reduz o A* ao UCS. Custo: **37** (ótimo), 115 nós expandidos.
2. **Heurística de Manhattan $h_2(n) = |r - 11| + |c - 11|$ (Admissível):**
   - Como o custo mínimo de qualquer transição no pomar é 1 (no carreador), a distância de Manhattan é uma estimativa relaxada que nunca superestima o custo real ($h_2(n) \le h^*(n)$).
   - Resultado: Custo **37** (ótimo garantido) com apenas **102 nós expandidos** (economia de $11,3\%$ de expansões em relação ao UCS).
3. **Heurística Inflacionada $h_3(n) = 4 \times \text{Manhattan}$ (Inadmissível):**
   - Superestima o custo remanescente quando há carreadores no caminho. Viola a admissibilidade ($h_3(n) > h^*(n)$).
   - Resultado: Custo **40** (perde a rota ótima de custo 37 por ganância excessiva).

---

## 2.7 Otimização por Busca Local ($K = 15$ Talhões)

- **Espaço de Busca:** Escolher um subconjunto de $K = 15$ coordenadas entre as 116 transitáveis:
  $$\binom{116}{15} \approx 2,45 \times 10^{18} \text{ combinações possíveis}$$
- **Operador de Vizinhança (1-opt swap):** Substituir 1 talhão inspecionado por 1 talhão livre não inspecionado ($15 \times 101 = 1.515$ vizinhos imediatos por iteração).
- **Função Objetivo a Maximizar:**
  $$f(S) = \sum_{p \in S} \text{Risco}(p) + 2.0 \times \sum_{p \in S} \min_{q \in S \setminus \{p\}} \text{Dist}(p, q)$$
  Equilibra a prioridade de foco em pragas/umidade com a dispersão espacial pelo pomar.
- **Resultados das 30 Rodadas:**
  - **Hill Climbing:** Média **564,78** | Desvio **1,86** | Melhor **567,90** | Tempo **503,9 ms** (preso em ótimos locais gulosos).
  - **Simulated Annealing:** Média **562,62** | Desvio **1,84** | Melhor **566,39** | Tempo **73,3 ms** (aceita pioras temporárias com probabilidade $e^{\Delta E / T}$ e explora múltiplos quadrantes).

---

## 2.8 Sistema Especialista com Encadeamento para Trás (Backward Chaining)

O módulo [`src/especialista.py`](src/especialista.py) implementa um motor de inferência retroativo baseado em regras `SE <antecedentes> ENTÃO <consequente>`:
- **Motor Retroativo:** Parte da hipótese (meta) e busca recursivamente provar as pré-condições necessárias nos fatos conhecidos ou em regras subordinadas, evitando loops cíclicos.
- **Rastreabilidade Causal ("Por quê?"):** Produz a árvore de explicação estruturada demonstrando os fatos sensoriais e regras disparadas.
- **Quebra da Base e Salvaguarda R7:**
  - Base v1 inicial: Diante de infestação severa de mosca-das-frutas, o sistema disparava `aplicar_quimico`.
  - Caso real de quebra: Talhão com colheita de manga em 3 dias e produto com carência de 14 dias (crime sanitário de resíduo tóxico).
  - Base v2 corrigida: Implementação da salvaguarda **R7**:
    $$\text{SE } (\text{colheita\_proxima} \land \text{carencia\_violada}) \rightarrow \text{aplicar\_controle\_biologico}$$
    Garantindo exportação segura e conformidade legal.

---

## 2.9 Incerteza, Sensores e Teorema de Bayes

Com os parâmetros oficiais extraídos da semente `24114066`:
- Prevalência real da praga: $P(I) = 4,7\%$
- Sensibilidade técnica do sensor: $P(S^+ \mid I) = 95,0\%$
- Taxa de falso positivo: $P(S^+ \mid I^c) = 3,0\%$
- Talhões semanais: $800$

### A Falácia da Taxa Base (Base Rate Fallacy):
$$P(I \mid S^+) = \frac{0,95 \times 0,047}{(0,95 \times 0,047) + (0,03 \times 0,953)} = \frac{0,04465}{0,07324} = \mathbf{60,96\%}$$
- **Taxa de Alertas Falsos (FDR):** $1 - 0,6096 = \mathbf{39,04\%}$.
  > *"A cada 100 alertas do meu sistema, cerca de 39 serão falsos."*
- **Impacto em Campo:** Para 800 talhões/semana, o sensor gera **22,87 alarmes falsos**, desperdiçando **4,57 horas semanais** de agrônomos (considerando 12 minutos por checagem presencial).
- **Aumento de Sensibilidade para 99,9%:** Eleva o VPP para apenas **62,15%** ($+1,19\text{ p.p.}$) e não reduz os falsos alertas. A prioridade tecnológica deve ser **reduzir a taxa de falsos positivos** (aumentar a especificidade).

---

## 2.10 Bônus da Liga de IA: Contraexemplo Formal 8x8 (DFS > 2x Ótimo)

Construído em [`src/contraexemplo_bonus.py`](src/contraexemplo_bonus.py):
- Uma grade $8 \times 8$ artesanal onde a saída está em `(0,0)` e a meta em `(7,7)`.
- O miolo central é preenchido com bloqueios intransitáveis (`#`), criando dois corredores isolados:
  - Corredor Norte/Leste: 14 passos em carreador firme (`.`, custo 1) $\rightarrow$ **Custo Ótimo UCS = 14**.
  - Corredor Sul/Oeste: 13 passos em solo encharcado (`~`, custo 4) e 1 carreador $\rightarrow$ **Custo DFS = 53**.
- Como a convenção estrita de expansão é **Sul $\rightarrow$ Leste $\rightarrow$ Oeste $\rightarrow$ Norte**, o DFS entra deterministicamente no corredor Sul e nunca faz backtracking:
  $$\text{Razão} = \frac{53}{14} \approx \mathbf{3,79\times} > 2\times$$

---

## 2.11 Auditoria Crítica do Laudo Técnico da AgroVision

O laudo comercial da empresa concorrente **AgroVision** foi auditado e refutado em [`RELATORIO.md`](RELATORIO.md):
1. *"BFS acha rota ótima mais rápido":* **INCORRETA.** Entrega custo 43 contra 37 do ótimo no pomar oficial ($16,2\%$ mais caro).
2. *"Manhattan 4x acelera preservando rota ótima":* **INCORRETA.** É inadmissível e entrega custo 40 (subótimo).
3. *"UCS é leve e altamente escalável para milhares de hectares":* **PARCIALMENTE CORRETA / ENGANOSA.** UCS consome quase $190\text{ MB}$ em $n=1000$ e é o primeiro a atingir timeout (> 60s) devido à fila de prioridade com milhões de nós.
4. *"95% de sensibilidade significa 95% de certeza":* **INCORRETA.** Confunde sensibilidade com VPP; pela taxa base, $39\%$ dos alertas são falsos.
5. *"Módulo premium com sensibilidade de 99,9% resolve os alarmes falsos":* **INCORRETA.** O VPP sobe apenas 1,19 ponto percentual e os alarmes falsos continuam inalterados.
- **Parecer Final da Dupla:** Recomendação de **RECUSA** da contratação no formato apresentado, condicionando homologação à adoção de A* admissível ($h_2$), redução contratual da taxa de falsos positivos ($FPR \le 0,8\%$) e salvaguarda determinística pré-colheita.

---

# 3. Explicação Detalhada do Código por Módulo

Abaixo está a análise técnica aprofundada de cada um dos scripts do pacote `src/`.

---

## 3.1 `src/gerador_pomar.py`
**Responsabilidade:** Fornecer deterministicamente a grade e os parâmetros de sensores com base na matrícula do aluno (contrato inalterado).

### Principais Componentes:
- `CUSTO = {".": 1, "~": 4}`: Dicionário global de custos de transição.
- `BLOQUEADO = "#"`: Marcador de obstáculo intransitável.
- `gerar_pomar(matricula: int, n: int = 12)`:
  - Inicializa `random.Random(matricula % 1_000_000)` para garantir reprodutibilidade matemática exata.
  - Preenche a matriz $n \times n$: sorteio com probabilidade $< 0.20$ gera `#`; entre $0.20$ e $0.40$ gera `~`; restante gera `.`.
  - Algoritmo de conectividade garantida: traça um caminho aleatório da entrada $(0,0)$ até $(n-1, n-1)$ convertendo eventuais bloqueios `#` em poças `~`, garantindo que sempre exista ao menos uma rota viável.
- `parametros_sensor(matricula: int)`:
  - Inicializa `random.Random((matricula % 1_000_000) + 777)`.
  - Retorna o dicionário contendo: `prevalencia`, `sensibilidade`, `taxa_falso_positivo` e `talhoes_por_semana`.

---

## 3.2 `src/buscas.py`
**Responsabilidade:** Implementar os algoritmos de busca cega e informada no grafo com instrumentação dos 4 contadores exigidos no enunciado.

### Principais Componentes e Funções:
- `DIRECOES = [(1, 0), (0, 1), (0, -1), (-1, 0)]`: Lista estática e imutável que padroniza a ordem de expansão de vizinhos: **Sul, Leste, Oeste, Norte**.
- `obter_vizinhos(r, c, pomar, n)`: Filtra células ortogonais adjacentes que estejam dentro dos limites da matriz $[0, n-1]$ e que não sejam bloqueadas (`!= '#')`.
- `reconstruir_caminho(parent, goal)`: Percorre o encadeamento de ponteiros do dicionário `parent` a partir da meta até o início, invertendo a lista resultante.
- `calcular_custo_caminho(caminho, pomar)`: Soma o custo do terreno para cada célula da rota a partir do segundo elemento ($caminho[1:]$), pois o ponto de partida já foi alcançado.
- `busca_largura(pomar)`:
  - Estrutura: `deque` (fila FIFO).
  - Regra de parada: Teste de meta na **geração** do nó vizinho (otimização canônica do BFS).
  - Contadores: Rastreia o tamanho máximo da fila com `max(fronteira_max, len(queue))` e nós expandidos a cada `popleft()`.
- `busca_profundidade(pomar)`:
  - Estrutura: Lista Python utilizada como pilha LIFO (`stack.append()` e `stack.pop()`).
  - Regra de inversão na inserção: Para garantir que o nó desempilhado siga rigorosamente a ordem Sul $\rightarrow$ Leste $\rightarrow$ Oeste $\rightarrow$ Norte, os vizinhos válidos são inseridos na ordem invertida: `for viz in reversed(vizinhos)`.
- `busca_custo_uniforme(pomar)`:
  - Estrutura: Fila de prioridade (`heapq`), armazenando tuplas `(custo_acumulado, contador, nó)`. O contador de desempate evita erros de comparação entre nós quando os custos são idênticos.
  - Regra de parada: Teste de objetivo na **expansão** (desempilhamento do nó), essencial para garantir otimalidade.
  - Reabertura/Atualização: Atualiza `cost_so_far[viz]` e insere na fila sempre que um caminho com menor $g(n)$ é descoberto.
- `busca_a_estrela(pomar, heuristica, nome_heuristica, reabrir_nos=True)`:
  - Estrutura: Heap ordenado por $f(n) = g(n) + h(n)$, armazenando tuplas `(f, g, contador, nó)`.
  - Reabertura de nós fechados: O parâmetro `reabrir_nos=True` permite reexpandir nós previamente visitados caso uma rota com menor $g(n)$ seja encontrada por outro ramo, blindando o algoritmo contra heurísticas não consistentes.

---

## 3.3 `src/busca_local.py`
**Responsabilidade:** Seleção ótima de $K = 15$ talhões de inspeção fitossanitária no pomar $12 \times 12$ por meio de Subida de Encosta e Têmpera Simulada.

### Principais Componentes:
- `obter_talhoes_livres(pomar)`: Extrai as coordenadas de todas as 116 células transitáveis (`.` e `~`).
- `calcular_mapa_risco(pomar, livres)`: Pré-calcula a severidade fitossanitária de cada talhão livre: base 10 para poças `~`, base 2 para carreadores `.`, somado à influência decrescente $\frac{3.0}{1.0 + \text{dist}}$ de todas as poças vizinhas.
- `precomputar_estrutura(pomar, livres)`: Constrói a matriz $116 \times 116$ de distâncias de Manhattan indexada por inteiros $[0..115]$. Isso substitui chamadas repetitivas de cálculo de distância por lookups em array $O(1)$, conferindo uma aceleração de mais de $10\times$ no loop de vizinhança.
- `funcao_objetivo(...)`: Soma o risco fitossanitário dos 15 talhões selecionados ao bônus de dispersão espacial ($2.0 \times \sum \min \text{Dist}$).
- `hill_climbing(...)`: Implementa a subida de encosta gananciosa tradicional (*Steepest Ascent*). A cada passo, avalia todos os 1.515 vizinhos 1-opt possíveis; move-se para o melhor vizinho se este for estritamente superior ao atual ($\Delta f > 0$); encerra ao atingir um platô ou máximo local.
- `simulated_annealing(...)`: Implementa a têmpera simulada com resfriamento geométrico $T(t) = T_0 \cdot \alpha^t$ ($T_0=100$, $\alpha=0.995$). Sorteia um vizinho 1-opt aleatório; aceita transições de melhora diretamente e pioras com probabilidade de Metropolis-Hastings $e^{\Delta E / T}$. Rastreia e preserva a melhor solução global encontrada ao longo de toda a trajetória.
- `executar_experimento_busca_local(matricula, k=15, num_execucoes=30)`: Orquestra 30 execuções com sementes pseudoaleatórias controladas, calculando Média, Desvio Padrão e Melhor Valor.

---

## 3.4 `src/especialista.py`
**Responsabilidade:** Implementar o sistema especialista baseado em regras de produção para manejo fitossanitário com encadeamento para trás e rastreamento de explicação causal.

### Principais Componentes:
- `class Regra`: Modela a regra com identificador (ex: `'R1'`), lista de antecedentes (premissas), consequente (fato derivado) e justificativa técnica descritiva.
- `class NoExplicacao`: Modela os nós da árvore explicativa gerada pela inferência. Possui o método recursivo `formatar_cadeia()` para imprimir a árvore identada no formato visual:
  ```text
  Conclusão: 'bloqueio_sanitario'
      Disparou [R7] SE colheita_proxima E carencia_violada ENTÃO ...
      |-- Fato comprovado: 'colheita_proxima'
      |-- Fato comprovado: 'carencia_violada'
  ```
- `class MotorInferenciaRetroativo`: Motor de encadeamento para trás (Backward Chaining). Dado um objetivo de interesse, filtra as regras candidatas que concluem esse objetivo e tenta provar recursivamente cada um dos antecedentes. Possui conjunto `caminho_pilha` que detecta e neutraliza loops cíclicos no grafo de conhecimento.
- `executar_caso_estudo_quebra_base()`: Executa o cenário comparativo da colheita em 3 dias com carência de 14 dias:
  - Na Base v1 (incompleta): Prova `aplicar_quimico`, violando normas sanitárias.
  - Na Base v2 (com salvaguarda R7): O motor prioriza a salvaguarda determinística e conclui `aplicar_controle_biologico`, gerando a árvore completa de justificativa.

---

## 3.5 `src/bayes.py`
**Responsabilidade:** Análise probabilística rigorosa do sensor óptico de pragas via Teorema de Bayes e avaliação do impacto operacional no campo.

### Principais Componentes:
- `calcular_probabilidade_posterior(prevalencia, sensibilidade, taxa_falso_positivo)`:
  - Calcula a probabilidade marginal de teste positivo pela Lei da Probabilidade Total:
    $$P(S^+) = P(S^+ \mid I) \cdot P(I) + P(S^+ \mid I^c) \cdot P(I^c)$$
  - Determina o Valor Preditivo Positivo (VPP):
    $$VPP = P(I \mid S^+) = \frac{P(S^+ \mid I) \cdot P(I)}{P(S^+)}$$
  - Determina a Taxa de Alertas Falsos (False Discovery Rate - FDR):
    $$FDR = 1 - VPP$$
- `calcular_impacto_campo(prevalencia, sensibilidade, taxa_falso_positivo, talhoes_semana, minutos_por_inspecao=12.0)`:
  - Multiplica os percentuais pelo volume semanal de talhões ($800$).
  - Calcula o total de alertas emitidos, alertas verdadeiros e falsos alarmes ($22,87$).
  - Converte falsos alarmes em tempo humano desperdiçado: $22,87 \times 0,2\text{ h} = 4,57\text{ horas/semana}$.
- `analisar_sensor_bayesiano(matricula)`: Executa as análises dos itens (a), (b), (c) e (d) do enunciado, formatando a frase oficial obrigatória:
  > *"A cada 100 alertas do meu sistema, cerca de 39 serão falsos."*
  E demonstra que a elevação da sensibilidade para $99,9\%$ é inócua frente à taxa base.

---

## 3.6 `src/escalabilidade.py`
**Responsabilidade:** Avaliar empiricamente e teoricamente os limites de tempo, memória de pico e profundidade de pilha quando a dimensão do pomar cresce até ordens assintóticas.

### Principais Componentes:
- `medir_algoritmo(func, pomar, ...)`: Envolve a execução do algoritmo com `tracemalloc.start()` e `time.perf_counter()`, medindo o pico exato de memória em megabytes (MB) e o tempo em milissegundos. Interrompe a execução caso ultrapasse o limite de timeout (60 segundos).
- `testar_dfs_recursivo_limite(matricula)`: Executa a versão recursiva pura com `sys.setrecursionlimit(1000)` para registrar formalmente o momento em que a profundidade do caminho $m$ ultrapassa o limite da pilha do interpretador, gerando `RecursionError`.
- `executar_estudo_escalabilidade(...)`: Conduz os experimentos na faixa $n \in [12, 20, 40, 80, 160, 320, 600, 1000]$, gerando a tabela comparativa e o diagnóstico formal de limites da **Aula 03**:
  - UCS é o primeiro candidato a falha por timeout em $n \ge 1800$;
  - A memória do UCS e BFS escala quadraticamente com $O(n^2)$ atingindo quase $190\text{ MB}$ em $n=1000$;
  - O DFS consome memória ínfima ($< 2\text{ MB}$), mas entrega rotas subótimas.

---

## 3.7 `src/contraexemplo_bonus.py`
**Responsabilidade:** Implementação e validação formal do bônus da Liga de IA (+0,3 ponto).

### Principais Componentes:
- Matriz $8 \times 8$ artesanal montada deterministicamente:
  - Linha 0 e Coluna 7: Carreadores firmes (`.`, custo 1);
  - Coluna 0 e Linha 7: Solo encharcado (`~`, custo 4);
  - Miolo (Linhas 1 a 6, Colunas 1 a 6): Bloqueios (`#`).
- Demonstração comparativa:
  - Rota do UCS: Segue pelo Norte/Leste $\rightarrow$ Custo **14** (14 passos em `.`).
  - Rota do DFS: Segue pelo Sul/Oeste atraído pela regra de prioridade Sul $\rightarrow$ Custo **53** (13 passos em `~` e 1 em `.`).
  - Razão: $\frac{53}{14} \approx 3,79\times > 2\times$. Atende matematicamente ao regulamento.

---

## 3.8 `src/main.py`
**Responsabilidade:** Orquestrador unificado da Sprint 1. Gera todos os artefatos requeridos pelo enunciado a partir de um único comando.

### Principais Componentes:
- `salvar_pomar_txt(pomar, matricula, caminho_txt)`: Gera `resultados/pomar.txt` contendo a matrícula-semente na primeira linha seguida pela representação textual dos talhões separados por espaço.
- `salvar_resultados_csv(resultados, caminho_csv)`: Exporta `resultados/resultados.csv` contendo exatamente as 7 colunas obrigatórias:
  `estrategia,heuristica,custo,passos,nos_expandidos,fronteira_max,tempo_ms`.
- `gerar_grafico_nos_expandidos(resultados, matricula, caminho_png)`: Utiliza o backend headless do Matplotlib (`matplotlib.use('Agg')`) para gerar `resultados/grafico.png` com gráfico de barras comparativo de nós expandidos em alta resolução (300 DPI), com grid, rótulos e anotações numéricas.
- `executar_pipeline_completo(matricula)`: Executa as buscas, salva os 3 artefatos em `resultados/` e exibe o resumo completo no console (buscas, busca local, especialista e bayes).

---

# 4. Resultados Numéricos Oficiais Consolidados

Todos os dados abaixo foram medidos na semente oficial **`24114066`**:

### Tabela Oficial de Buscas (`resultados/resultados.csv`):
| Estratégia | Heurística | Custo | Passos | Nós Expandidos | Fronteira Máx. | Tempo (ms) | Ótima? |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **BFS** | N/A | 43 | 22 | 113 | 11 | 0,106 | ❌ Não (passos mín.) |
| **DFS** | N/A | 43 | 22 | 23 | 24 | 0,030 | ❌ Não (viés do gerador) |
| **UCS** | N/A | **37** | 22 | 115 | 14 | 0,169 | ✅ **Sim (Ótimo)** |
| **A\*** | $h_1$ (zero) | **37** | 22 | 115 | 14 | 0,179 | ✅ **Sim** |
| **A\*** | $h_2$ (Manhattan) | **37** | 22 | **102** | 17 | 0,168 | ✅ **Sim (Menos nós)** |
| **A\*** | $h_3$ (4x Manhattan) | 40 | 22 | 23 | 24 | 0,047 | ❌ Não (Inadmissível) |

### Síntese da Busca Local ($K = 15$ Talhões, 30 Rodadas):
- **Subida de Encosta (Hill Climbing):** Média: **564,78** | Desvio Padrão: **1,86** | Melhor: **567,90** | Tempo Médio: **503,9 ms**
- **Têmpera Simulada (Simulated Annealing):** Média: **562,62** | Desvio Padrão: **1,84** | Melhor: **566,39** | Tempo Médio: **73,3 ms**

### Diagnóstico Probabilístico Bayesiano:
- Valor Preditivo Positivo (VPP): **$60,96\%$**
- Taxa de Alertas Falsos (FDR): **$39,04\%$**
- Volume Semanal de Alarmes Falsos: **$22,87$ talhões**
- Mão de Obra Agronômica Desperdiçada: **$4,57\text{ horas/semana}$** (cerca de 4h 34min)

---

# 5. Guia de Execução dos Comandos

### Instalação de Dependências:
```bash
pip install -r requirements.txt
```

### 1. Execução Principal (Pipeline Completo):
Gera e atualiza os arquivos `resultados/pomar.txt`, `resultados/resultados.csv` e `resultados/grafico.png`:
```bash
python src/main.py 24114066
```

### 2. Execuções Modulares Específicas:
- **Testar buscas clássicas e A\* com tabela no terminal:**
  ```bash
  python src/buscas.py 24114066
  ```
- **Executar as 30 rodadas de Busca Local (Hill Climbing e Simulated Annealing):**
  ```bash
  python src/busca_local.py 24114066
  ```
- **Executar o Sistema Especialista retroativo e caso de quebra da base:**
  ```bash
  python src/especialista.py
  ```
- **Executar a dedução formal do Teorema de Bayes e impacto em campo:**
  ```bash
  python src/bayes.py 24114066
  ```
- **Executar o estudo assintótico de escalabilidade com medição de memória:**
  ```bash
  python src/escalabilidade.py 24114066
  ```
- **Verificar o contraexemplo formal do bônus da Liga de IA (grade 8x8):**
  ```bash
  python src/contraexemplo_bonus.py
  ```

---

*Documento consolidado e verificado para o projeto Caatinga.AI — Sprint 1.*
