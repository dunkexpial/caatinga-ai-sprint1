# Caatinga.AI - Sprint 1: Agente de Inspeção Fitossanitária no Semiárido

## Identificação

| Campo | Informação |
| :--- | :--- |
| **Disciplina** | Inteligência Artificial (2026.2) — UniRios |
| **Docente** | Prof. Ronierison Maciel |
| **Dupla** | João Vítor Almeida dos Santos (Matrícula: `24114066`) e Caio Lúcio dos Santos Almeida (Matrícula: `24114035`) |
| **Semente Oficial (matrícula mais antiga)** | `24114066` |

---

## O que este projeto faz

O **Caatinga.AI** implementa um agente autônomo que navega uma grade 12×12 de talhões de pomar (carreadores `.`, poças `~` e bloqueios `#`), partindo do portão `(0,0)` até o ponto de coleta `(11,11)`. O projeto compara algoritmos de busca cega (BFS, DFS, UCS), busca informada (A* com três heurísticas), busca local (Hill Climbing e Têmpera Simulada) e raciocínio simbólico (sistema especialista + Teorema de Bayes) sobre o pomar gerado deterministicamente a partir da matrícula da dupla.

---

## Como rodar

### Requisitos

- Python 3.10 ou superior
- Biblioteca `matplotlib` (única dependência externa)

```bash
pip install -r requirements.txt
```

### Execução principal (gera os três arquivos de saída)

```bash
python src/main.py 24114066
```

Isso produz automaticamente (ou sobrescreve) em `resultados/`:
- `resultados/pomar.txt` — grade do pomar com matrícula-semente na 1ª linha
- `resultados/resultados.csv` — tabela com 6 estratégias de busca
- `resultados/grafico.png` — gráfico de barras: nós expandidos × estratégia (300 DPI, eixos rotulados)

### Módulos individuais (para exploração/arguição)

```bash
python src/buscas.py 24114066          # BFS, DFS, UCS e A* com tabela no terminal
python src/busca_local.py 24114066     # Hill Climbing e Simulated Annealing (30 rodadas)
python src/especialista.py             # Sistema especialista com encadeamento para trás
python src/bayes.py 24114066           # Análise bayesiana do sensor óptico de pragas
python src/escalabilidade.py           # Teste de escalabilidade n=12..1000
python src/contraexemplo_bonus.py      # Bônus: grade 8x8 onde DFS > 2x ótimo
```

---

## Tabela-Resumo dos Resultados (Semente 24114066)

Gerada por `python src/main.py 24114066` e consolidada em `resultados/resultados.csv`:

| Estratégia | Heurística | Custo | Passos | Nós Expandidos | Fronteira Máx. | Tempo (ms) | Ótima? |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **BFS** | N/A | 43 | 22 | 113 | 11 | 0,106 | Nao (passos min.) |
| **DFS** | N/A | 43 | 22 | 23 | 24 | 0,030 | Nao |
| **UCS** | N/A | **37** | 22 | 115 | 14 | 0,169 | **Sim** |
| **A\*** | h1 (zero) | **37** | 22 | 115 | 14 | 0,179 | **Sim** |
| **A\*** | h2 (Manhattan) | **37** | 22 | **102** | 17 | 0,168 | **Sim** |
| **A\*** | h3 (4×Manhattan) | 40 | 22 | 23 | 24 | 0,047 | Nao (inadmissivel) |

> Custo ótimo global: **37**. A* com h2 expande o menor número de nós (102) mantendo a rota ótima.

---

## Ordem de Expansão dos Vizinhos e Reabertura de Nós

A ordem de expansão dos vizinhos, **idêntica em todos os algoritmos**, é:

1. **Sul** `(+1, 0)`
2. **Leste** `(0, +1)`
3. **Oeste** `(0, -1)`
4. **Norte** `(-1, 0)`

Essa ordem é declarada na lista `DIRECOES` em [`src/buscas.py`](src/buscas.py) e mantida invariante em todos os módulos. Sem essa declaração, os contadores de DFS não são reproduzíveis.

**O A\* reabre nós:** Sim. O parâmetro `reabrir_nos=True` (padrão) é utilizado em `busca_a_estrela`. Isso garante otimalidade mesmo com heurísticas admissíveis mas não consistentes. A versão com `reabrir_nos=False` está disponível para demonstração do efeito de heurísticas inadmissíveis (h3).

---

## Mapa do Repositório

```
caatinga-ai-sprint1/
├── README.md                <- este arquivo: porta de entrada do projeto
├── RELATORIO.md             <- relatório técnico completo (Partes 1 a 5 + Bônus)
├── ANEXO_IA.md              <- Parte 6: registro obrigatório de uso de IA generativa
├── requirements.txt         <- dependência única: matplotlib>=3.5
├── src/
│   ├── gerador_pomar.py     <- gerador determinístico do pomar (NAO ALTERAR)
│   ├── buscas.py            <- BFS, DFS, UCS e A* com 4 contadores instrumentados
│   ├── busca_local.py       <- Hill Climbing e Simulated Annealing (K=15, 30 rodadas)
│   ├── especialista.py      <- sistema especialista com encadeamento para trás + trace
│   ├── bayes.py             <- análise bayesiana do sensor óptico (Teorema de Bayes)
│   ├── main.py              <- pipeline unificado: gera pomar, CSV e gráfico
│   ├── escalabilidade.py    <- teste assintótico n=12..1000 com tracemalloc
│   └── contraexemplo_bonus.py <- grade 8x8 onde DFS entrega custo 53 vs ótimo 14
└── resultados/
    ├── pomar.txt            <- grade 12x12 gerada com semente 24114066 (1ª linha)
    ├── resultados.csv       <- 6 linhas de resultados, header exato do enunciado
    └── grafico.png          <- barras de nós expandidos por estratégia (300 DPI)
```

| Arquivo | O que resolve |
| :--- | :--- |
| `src/gerador_pomar.py` | Contrato com a correção: gera o pomar e os parâmetros do sensor pela semente |
| `src/buscas.py` | Parte 2 e Parte 3 (busca cega e busca informada) |
| `src/busca_local.py` | Parte 3.4 (Hill Climbing e Têmpera Simulada) |
| `src/especialista.py` | Parte 4.1 e 4.2 (base de regras, encadeamento para trás, quebra da base) |
| `src/bayes.py` | Parte 4.3 (VPP, FDR, impacto operacional, análise de sensibilidade) |
| `src/main.py` | Ponto único de entrada — gera os três arquivos obrigatórios do enunciado |
| `src/escalabilidade.py` | Parte 2.4 (análise assintótica e limites de memória) |
| `src/contraexemplo_bonus.py` | Bônus Liga de IA (+0,3): contraexemplo construído à mão |
| `RELATORIO.md` | Relatório completo com todas as tabelas e análises das Partes 1 a 5 |
| `ANEXO_IA.md` | Parte 6: ferramentas usadas, prompts, erro do assistente, reflexão |

---

## Limitações Conhecidas

- **`src/escalabilidade.py` tem timeout em n ≥ 1.800** no UCS/A*, pois a fila de prioridade com centenas de milhares de estados ultrapassa 60 segundos. Esse comportamento é documentado na Seção 2.4 do relatório e constitui evidência da complexidade espacial O(n²).
- **DFS recursivo colapsa com RecursionError para rotas com profundidade > 1.000.** A implementação em produção usa pilha iterativa explícita; a versão recursiva é demonstrada separadamente em `escalabilidade.py` com `sys.setrecursionlimit(1000)` para fins didáticos.
- **A heurística h3 (4×Manhattan) é intencionalmente inadmissível.** Ela é incluída para demonstrar empiricamente a perda de otimalidade do A* com heurísticas inflacionadas (custo 40 vs. ótimo 37), conforme exigido pelo enunciado.
- **`resultados/grafico.png` requer `matplotlib`.** Se a biblioteca não estiver instalada, execute `pip install -r requirements.txt` antes de `python src/main.py 24114066`.
