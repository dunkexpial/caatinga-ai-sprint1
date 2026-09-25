# 📋 Painel de Coordenação da Dupla (Caatinga.AI)

> **Aviso:** Este arquivo é um guia temporário de sincronização entre **João Vítor** e **Caio Lúcio**. Ele orienta os passos exatos de cada integrante para manter o histórico de 12 commits perfeitamente intercalado e autêntico no GitHub.

---

## 📌 Status Atual do Projeto
- **Último Commit Realizado:** `Commit 2` (por João Vítor Almeida)
- **Mensagem:** `feat: implementa buscas cegas e informadas (BFS, DFS, UCS, A*) com 4 contadores e reabertura de nos`
- **Artefato Criado:** `src/buscas.py`
- **👉 Próximo Passo:** **`Commit 3` — AGORA É A VEZ DO CAIO!**

---

## 🎯 Instruções Específicas para o Caio (Commit 3)

### 1. Atualize seu repositório local
No seu terminal/Git Bash na pasta do projeto:
```bash
git pull origin main
```

### 2. Verifique sua autoria do Git
Certifique-se de que seus commits saiam com seus dados oficiais:
```bash
git config user.name "Caio Lúcio Almeida"
git config user.email "kaiolucioalmeida@gmail.com"
```

### 3. O que você deve fazer no Commit 3:
Implementar o arquivo `src/busca_local.py` atendendo à **Seção 5.4 do enunciado**:
- **Problema:** Escolher $K = 15$ talhões livres para inspeção no pomar gerado com a semente `24114066`.
- **Modelagem da Busca Local:**
  - **Estado:** Subconjunto de $K = 15$ coordenadas livres `(r, c)` (ou seja, células diferentes de `#`).
  - **Vizinhança:** Trocar um dos talhões inspecionados por um talhão livre não inspecionado (1-opt swap).
  - **Função Objetivo (a maximizar):** Por exemplo, pontuação de prioridade/cobertura ou severidade de pragas (ex: células com maior proximidade a focos de solo encharcado `~`, ou dispersão uniforme pela grade).
  - **Algoritmos obrigatórios:**
    1. **Subida de Encosta (Hill Climbing)**: ganancioso tradicional.
    2. **Têmpera Simulada (Simulated Annealing)**: com programação de resfriamento (temperatura $T$, probabilidade $e^{\Delta E / T}$ para aceitar piora).
  - **Execução:** Rodar cada um **30 vezes** (conforme Seção 5.4 e item 6 das armadilhas: *"Média de 30 execuções, não uma execução isolada"*).
  - Reportar: Média, Desvio Padrão e Melhor Valor de cada algoritmo.

### 4. Realizar o Commit e Push
Após testar `src/busca_local.py`, faça o commit exatamente com a mensagem combinada:
```bash
git add src/busca_local.py INSTRUCOES_CAIO.md
git commit -m "feat: implementa busca local com subida de encosta e tempera simulada para k=15"
git push origin main
```

### 5. Após o push
Alerte o João Vítor para que ele faça o `git fetch` / `git pull` e dê continuidade ao **Commit 4** (`src/especialista.py`).

---

## 🗺️ Tabela Geral dos 12 Commits Intercalados

| # | Responsável | Mensagem Exata do Commit | Arquivos / Conteúdo | Status |
|:---:|:---:|:---|:---|:---:|
| **1** | **João Vítor** | `feat: estrutura inicial do projeto com gerador_pomar e configuracoes` | `.gitignore`, `requirements.txt`, `src/gerador_pomar.py` | ✅ Concluído |
| **2** | **João Vítor** | `feat: implementa buscas cegas e informadas (BFS, DFS, UCS, A*) com 4 contadores e reabertura de nos` | `src/buscas.py` | ✅ Concluído |
| **3** | **Caio Lúcio** | `feat: implementa busca local com subida de encosta e tempera simulada para k=15` | `src/busca_local.py` | ⏳ **SUA VEZ AGORA** |
| **4** | **João Vítor** | `feat: implementa sistema especialista com encadeamento para tras e explicacao` | `src/especialista.py` | ⏸️ Aguardando Caio |
| **5** | **Caio Lúcio** | `feat: implementa modulo bayesiano para analise do sensor de pragas` | `src/bayes.py` | ⏸️ Aguardando |
| **6** | **João Vítor** | `feat: implementa script principal src/main.py gerando pomar, csv e grafico` | `src/main.py`, `resultados/` | ⏸️ Aguardando |
| **7** | **Caio Lúcio** | `test: executa analise de escalabilidade experimental e limites teoricos` | `src/escalabilidade.py` | ⏸️ Aguardando |
| **8** | **João Vítor** | `feat: adiciona contraexemplo 8x8 para bonus da Liga de IA (DFS > 2x otimo)` | `src/contraexemplo_bonus.py` | ⏸️ Aguardando |
| **9** | **Caio Lúcio** | `docs: elabora analise teorica PEAS, dimensoes de ambiente e auditoria AgroVision` | `RELATORIO.md` (Partes 1, 2 e 5) | ⏸️ Aguardando |
| **10** | **João Vítor** | `docs: detalha analise de heuristicas, quebra da base especialista e metricas bayesianas` | `RELATORIO.md` (Partes 3, 4 e Bônus) | ⏸️ Aguardando |
| **11** | **Caio Lúcio** | `docs: elabora ANEXO_IA.md com registro obrigatorio, prompts, erro documentado e reflexao` | `ANEXO_IA.md` | ⏸️ Aguardando |
| **12** | **João Vítor** | `docs: finaliza README.md completo com instrucoes, tabela-resumo e mapa do repositorio` | `README.md` | ⏸️ Aguardando |
