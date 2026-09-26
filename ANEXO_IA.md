# Anexo Obrigatório: Registro de Uso de Ferramentas de IA Generativa (ANEXO_IA.md)

**Projeto:** Caatinga.AI - Automação Agronômica e Roteamento Inteligente no Semiárido  
**Disciplina:** Inteligência Artificial (2026.2) - UniRios  
**Docente:** Prof. Ronierison Maciel  
**Autores:** Caio Lúcio dos Santos Almeida (`24114035`) & João Vítor Almeida dos Santos (`24114066`)  
**Semente Oficial:** `24114066`  

---

## A.1 Ferramentas de IA Generativa Utilizadas

Durante o desenvolvimento da Sprint 1 do projeto Caatinga.AI, a dupla utilizou de forma consciente, crítica e orientada a engenharia as seguintes ferramentas:

1. **Google Antigravity IDE (com Gemini 3.8 Flash e Gemini 3.8 Pro):**
   - Utilizado como ambiente de assistência ao pareamento de código (pair programming), refatoração modular, instrumentação de testes assintóticos de memória com `tracemalloc` e elaboração da arquitetura limpa em Python.
2. **ChatGPT (OpenAI GPT-4o):**
   - Utilizado em sessões exploratórias conceituais para brainstorming da modelagem PEAS, formatação de tabelas Markdown e checagem cruzada das deduções analíticas do Teorema de Bayes.
3. **GitHub Copilot:**
   - Empregado para autocompletar trechos repetitivos de código (como tipagem de assinaturas `typing.Tuple`, `typing.Dict` e cabeçalhos de funções).

### Distribuição do Apoio por Módulo do Projeto:

| Módulo do Repositório | Papel do Assistente de IA | Papel Crítico e Decisório da Dupla Humana |
| :--- | :--- | :--- |
| **`src/buscas.py`** | Esboço inicial da estrutura de filas com `heapq` e `deque`. | Implementação estrita da ordem de expansão Sul $\rightarrow$ Leste $\rightarrow$ Oeste $\rightarrow$ Norte, contadores exatos e algoritmo de reabertura de nós fechados no A*. |
| **`src/busca_local.py`** | Sugestão do operador 1-opt swap e estrutura da têmpera simulada. | Modelagem matemática da função objetivo combinando severidade agronômica de umidade com dispersão espacial, e pré-computação da matriz de distâncias para ganho de $10\times$ em velocidade. |
| **`src/especialista.py`** | Criação da classe base de representação de regras SE... ENTÃO. | Formulação do caso de estudo agronômico real de quebra da base (carência pré-colheita na manga Tommy Atkins) e salvaguarda determinística R7. |
| **`src/bayes.py`** | Validação da fórmula simbólica de probabilidade condicional. | Parametrização estrita pela semente oficial `24114066`, cálculo do impacto prático em horas semanais e identificação do paradoxo da taxa base. |
| **`src/escalabilidade.py`** | Sugestão do módulo padrão `tracemalloc`. | Detecção de gargalos de memória heap no UCS, prevenção de travamentos por timeout e formulação dos limites assintóticos $O(b^d)$ vs $O(b \cdot m)$. |
| **`RELATORIO.md`** | Auxílio na revisão gramatical e formatação estética em Markdown. | Autoria intelectual de 100% das análises conceituais, auditoria com números empíricos da AgroVision e redação do parecer final. |

---

## A.2 Transcrição Literal de Prompts e Respostas

Abaixo constam dois diálogos reais, transcritos na íntegra, demonstrando a interação técnica da dupla com o assistente:

### 📌 Diálogo 1: Modelagem da Função Objetivo para Busca Local (K=15)

#### Prompt Submetido:
> *"Estamos desenvolvendo o módulo de busca local (Hill Climbing e Simulated Annealing) para selecionar K = 15 talhões de inspeção fitossanitária em um pomar 12x12 gerado proceduralmente no semiárido da Caatinga. O pomar tem carreadores '.', poças alagadas '~' e bloqueios '#'. Queremos uma função objetivo realista que faça sentido agronômico para fruticultura irrigada. Como formular essa função objetivo para maximizar tanto o foco em pragas quanto a cobertura geográfica, sem que o algoritmo coloque todos os 15 fiscais grudados no mesmo lamaçal?"*

#### Resposta Recebida:
> *"Para modelar um problema realista de inspeção em agricultura de precisão, a função objetivo deve equilibrar dois termos conflitantes em uma formulação multiobjetivo escalarizada:*  
> *1. Prioridade Agronômica de Foco (Risco): Em áreas semiáridas irrigadas, poças de solo encharcado ('~') favorecem fungos radiculares como Phytophthora e proliferação de pragas. Assim, atribua uma pontuação base maior para células encharcadas (ex: 10 pontos) e menor para carreadores secos (ex: 2 pontos). Além disso, adicione um termo de vizinhança: células secas próximas a poças recebem um bônus decrescente inversamente proporcional à distância Manhattan até os focos de umidade.*  
> *2. Dispersão Espacial (Anti-Aglomeração): Se você maximizar apenas o risco, os 15 pontos ficarão concentrados no maior bolsão de umidade, deixando o restante da fazenda desguarnecido. Para forçar a dispersão, adicione um termo de diversidade geográfica, como a soma das distâncias mínimas de cada talhão inspecionado até o seu vizinho mais próximo dentro do subconjunto escolhido:*  
> *f(S) = \sum_{p \in S} Risco(p) + \lambda \times \sum_{p \in S} \min_{q \in S, q \ne p} Dist(p, q)*  
> *Onde \lambda pondera a importância relativa da dispersão em relação à severidade do talhão. Essa formulação cria uma paisagem multimodal com múltiplos ótimos locais, perfeita para demonstrar a vantagem do Simulated Annealing sobre a Subida de Encosta gulosa."*

---

### 📌 Diálogo 2: Análise da Falácia da Taxa Base no Sensor Óptico de Pragas

#### Prompt Submetido:
> *"No projeto Caatinga.AI, temos um sensor óptico para monitoramento de pragas em talhões de manga. Os parâmetros da nossa semente oficial (24114066) são: prevalência de praga de 4,7%, sensibilidade de 95% e taxa de falsos positivos de 3%. A fazenda inspeciona 800 talhões por semana. Um relatório comercial da empresa concorrente afirma que 'com 95% de sensibilidade, se o sensor apitou positivo, há 95% de certeza de que o talhão está doente'. Demonstre formalmente pelo Teorema de Bayes se essa afirmação procede, calcule a probabilidade real e determine o impacto operacional semanal."*

#### Resposta Recebida:
> *"A afirmação do relatório concorrente é categoricamente FALSA e incorre no viés cognitivo e estatístico conhecido como Falácia da Taxa Base (Base Rate Fallacy). O relatório comete o erro clássico de confundir a Sensibilidade P(Positivo | Infestado) com o Valor Preditivo Positivo P(Infestado | Positivo).*  
> *Pelo Teorema de Bayes:*  
> *P(I | S+) = [P(S+ | I) * P(I)] / P(S+)*  
> *Onde P(S+) é calculado pela Lei da Probabilidade Total:*  
> *P(S+) = P(S+ | I) * P(I) + P(S+ | Saudavel) * P(Saudavel)*  
> *Substituindo os valores da semente 24114066:*  
> *- P(I) = 0,047 | P(Saudavel) = 0,953*  
> *- P(S+ | I) = 0,95 | P(S+ | Saudavel) = 0,03*  
> *P(S+) = (0,95 * 0,047) + (0,03 * 0,953) = 0,04465 + 0,02859 = 0,07324*  
> *P(I | S+) = 0,04465 / 0,07324 = 0,609639... \approx 60,96%*  
> *A certeza real de infestação é de apenas 60,96%, e NÃO de 95%. Isso significa que a taxa de alarmes falsos é de 1 - 0,6096 = 39,04%. Em outras palavras: a cada 100 alertas emitidos pelo sensor, cerca de 39 são falsos.*  
> *Impacto operacional em 800 talhões semanais:*  
> *- Talhões saudáveis: 800 * 0,953 = 762,4 talhões.*  
> *- Alarmes falsos semanais: 762,4 * 0,03 = 22,87 alarmes falsos.*  
> *- Considerando 12 minutos (0,2 horas) por inspeção presencial de um agrônomo para checar cada alerta, gasta-se: 22,87 * 0,2 = 4,57 horas semanais de mão de obra altamente qualificada correndo atrás de pragas inexistentes."*

---

## A.3 Erro Técnico Comprovado do Assistente com Evidência Experimental

Durante o desenvolvimento do módulo de buscas informadas (`src/buscas.py`), submetemos uma consulta ao assistente sobre o comportamento do algoritmo A* com diferentes heurísticas na grade do pomar.

### ❌ A Afirmação Incorreta do Assistente:
> *"Como no pomar existem poças alagadas com custo 4, multiplicar a distância de Manhattan por 4 na heurística h3(n) = 4 * (|r - r_meta| + |c - c_meta|) não causará nenhum problema de otimalidade. Pelo contrário: ela continuará admissível no pior caso do terreno e fará o algoritmo A* se comportar de forma muito mais agressiva em direção à meta, expandindo menos nós e garantindo a rota de menor custo mais rápido do que a heurística de Manhattan normal."*

### 🔍 Por que a Afirmação Está Errada Teórica e Matematicamente?
Conforme estabelece a teoria fundamental de busca heurística (Russell & Norvig, Cap. 3 / Aula 03):
- Uma heurística $h(n)$ é **admissível** se e somente se ela for um limitante inferior do custo real ótimo até o objetivo para **todos** os nós do espaço de estados:
  $$h(n) \le h^*(n), \quad \forall n$$
- Na grade do pomar da Caatinga.AI, a maior parte do terreno ($55,56\%$ na semente oficial) é composta por carreadores transitáveis (`.`) cujo custo de deslocamento unitário é $c = 1$.
- Se o caminho ótimo até a meta for composto predominantemente por carreadores firmes, o custo real remanescente $h^*(n)$ é próximo da distância de Manhattan simples.
- Ao multiplicar por 4, $h_3(n)$ assume ficticiamente que cada passo futuro custará 4. Logo, para qualquer nó ao longo de um corredor de carreadores, teremos:
  $$h_3(n) = 4 \times Dist(n, meta) \gg h^*(n)$$
- A heurística torna-se **inadmissível**. A perda de admissibilidade quebra o teorema fundamental de otimalidade do A*: o algoritmo passa a agir como uma busca puramente gananciosa (Greedy Best-First), podando precocemente ramos promissores de menor custo acumulado $g(n)$ e comprometendo a garantia de encontrar a rota mais barata.

### 🧪 Evidência Experimental Irrefutável Produzida no Código da Dupla:
Executando o script oficial consolidado em `src/main.py` e inspecionando o arquivo de saída gerado [`resultados/resultados.csv`](file:///c:/Projetos%20Faculdade/caatinga-ai-sprint1/resultados/resultados.csv):

| Algoritmo | Heurística | Custo Obtido | Nós Expandidos | Fronteira Máxima | Rota Ótima Garantida? |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **UCS (Dijkstra)** | N/A | **37** | 115 | 14 | ✅ **Sim (Referência Ótima)** |
| **A\*** | **$h_2$ (Manhattan Padrão)** | **37** | **102** | 17 | ✅ **Sim (Ótimo)** |
| **A\*** | **$h_3$ (4x Manhattan Inflacionada)** | **40** | **23** | 24 | ❌ **NÃO (Subótimo!)** |

#### Conclusão Empírica:
A execução no computador desmascarou categoricamente a resposta da IA. O A* com a heurística inflacionada $h_3$ devolveu uma rota com **custo 40**, que é **$8,1\%$ mais cara** do que a rota ótima de **custo 37** descoberta pelo UCS e pelo A* com Manhattan admissível ($h_2$).  
A IA alucinou que a rota ótima seria preservada, quando na realidade o algoritmo foi enganado pela superestimativa da heurística. A dupla rejeitou a sugestão da IA e documentou a quebra de admissibilidade no relatório técnico.

---

## A.4 Reflexão Final da Dupla

> *"Depois de rodar o código e confrontar os resultados na prática, aprendemos que a retórica confiante e a elegância formal das respostas da IA generativa frequentemente mascaram suposições ingênuas e violações graves de admissibilidade que apenas o rigor matemático das aulas e a evidência empírica dos contadores de execução são capazes de desmascarar."*
