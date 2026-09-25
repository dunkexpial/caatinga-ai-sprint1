# 📋 Painel de Coordenação da Dupla (Caatinga.AI)

> **Aviso:** Este arquivo é um guia temporário de sincronização entre **João Vítor** e **Caio Lúcio**. Ele orienta os passos exatos de cada integrante para manter o histórico de 12 commits perfeitamente intercalado e autêntico no GitHub.

---

## 📌 Status Atual do Projeto
- **Último Commit Realizado:** `Commit 1` (por João Vítor Almeida)
- **Mensagem:** `feat: estrutura inicial do projeto com gerador_pomar e configuracoes`
- **Próximo Commit:** `Commit 2` (por João Vítor Almeida)
- **Quando Caio assume:** No **`Commit 3`** (implementação de `src/busca_local.py`).

---

## 🎯 Dados Oficiais do Projeto e Regras Técnicas
- **Semente Oficial:** `24114066` (Matrícula do integrante mais velho: João Vítor)
- **Repositório Remoto:** `https://github.com/dunkexpial/caatinga-ai-sprint1`
- **Branch Principal:** `main`
- **Ordem Fixa de Expansão dos Vizinhos (De Sul a Norte):**
  1. **Sul:** `(+1, 0)` — Linha abaixo
  2. **Leste:** `(0, +1)` — Coluna à direita
  3. **Oeste:** `(0, -1)` — Coluna à esquerda
  4. **Norte:** `(-1, 0)` — Linha acima
- **Regra de Ouro:** Não alterar `src/gerador_pomar.py` sob nenhuma hipótese.

---

## 🗺️ Tabela Geral dos 12 Commits Intercalados

| # | Responsável | Mensagem Exata do Commit | Arquivos / Conteúdo | Status |
|:---:|:---:|:---|:---|:---:|
| **1** | **João Vítor** | `feat: estrutura inicial do projeto com gerador_pomar e configuracoes` | `.gitignore`, `requirements.txt`, `src/gerador_pomar.py` | ✅ Concluído |
| **2** | **João Vítor** | `feat: implementa buscas cegas e informadas (BFS, DFS, UCS, A*) com 4 contadores e reabertura de nos` | `src/buscas.py` | ⏳ Em andamento |
| **3** | **Caio Lúcio** | `feat: implementa busca local com subida de encosta e tempera simulada para k=15` | `src/busca_local.py` | ⏸️ Aguardando vez |
| **4** | **João Vítor** | `feat: implementa sistema especialista com encadeamento para tras e explicacao` | `src/especialista.py` | ⏸️ Aguardando |
| **5** | **Caio Lúcio** | `feat: implementa modulo bayesiano para analise do sensor de pragas` | `src/bayes.py` | ⏸️ Aguardando |
| **6** | **João Vítor** | `feat: implementa script principal src/main.py gerando pomar, csv e grafico` | `src/main.py`, `resultados/` | ⏸️ Aguardando |
| **7** | **Caio Lúcio** | `test: executa analise de escalabilidade experimental e limites teoricos` | `src/escalabilidade.py` | ⏸️ Aguardando |
| **8** | **João Vítor** | `feat: adiciona contraexemplo 8x8 para bonus da Liga de IA (DFS > 2x otimo)` | `src/contraexemplo_bonus.py` | ⏸️ Aguardando |
| **9** | **Caio Lúcio** | `docs: elabora analise teorica PEAS, dimensoes de ambiente e auditoria AgroVision` | `RELATORIO.md` (Partes 1, 2 e 5) | ⏸️ Aguardando |
| **10** | **João Vítor** | `docs: detalha analise de heuristicas, quebra da base especialista e metricas bayesianas` | `RELATORIO.md` (Partes 3, 4 e Bônus) | ⏸️ Aguardando |
| **11** | **Caio Lúcio** | `docs: elabora ANEXO_IA.md com registro obrigatorio, prompts, erro documentado e reflexao` | `ANEXO_IA.md` | ⏸️ Aguardando |
| **12** | **João Vítor** | `docs: finaliza README.md completo com instrucoes, tabela-resumo e mapa do repositorio` | `README.md` | ⏸️ Aguardando |

---

## 👨‍💻 Instruções para Caio quando chegar sua vez (a partir do Commit 3)

1. **Atualize seu repositório local:**
   ```bash
   git pull origin main
   ```
2. **Confirme sua autoria no Git:**
   Certifique-se de que no seu Git local esteja configurado:
   ```bash
   git config user.name "Caio Lúcio Almeida"
   git config user.email "kaiolucioalmeida@gmail.com"
   ```
3. **Desenvolva/adicione o artefato referente ao seu commit.**
4. **Faça o commit com a mensagem combinada exata.**
5. **Envie para o GitHub:**
   ```bash
   git push origin main
   ```
6. **Alerte João Vítor** para que ele dê fetch/pull e dê continuidade ao próximo commit.
