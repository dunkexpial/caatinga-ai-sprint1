# Painel de Coordenação da Dupla - Projeto Caatinga.AI

Este documento é um guia de sincronização e alinhamento entre João Vítor e Caio Lúcio. Seu objetivo é manter o fluxo de trabalho organizado, garantindo que o histórico de 12 commits no Git permaneça consistente, intercalado e autêntico.

---

## Status Atual do Projeto

- Último commit integrado: Commit 9 (realizado por Caio Lúcio Almeida)
- Mensagem do commit 9: docs: elabora analise teorica PEAS, dimensoes de ambiente e auditoria AgroVision
- Artefatos entregues: RELATORIO.md (Partes 1, 2 e 5)
- Próximo passo: Commit 10 (responsabilidade de João Vítor Almeida)
- Módulo a desenvolver: RELATORIO.md (Partes 3, 4 e Bônus da Liga de IA)

---

## Parâmetros e Diretrizes Técnicas Fixadas

- Semente oficial do projeto: 24114066 (matrícula do integrante mais velho, João Vítor)
- Repositório remoto: https://github.com/dunkexpial/caatinga-ai-sprint1
- Branch principal de trabalho: main
- Ordem de expansão de vizinhos: estritamente de Sul a Norte
  1. Sul: (+1, 0)
  2. Leste: (0, +1)
  3. Oeste: (0, -1)
  4. Norte: (-1, 0)
- Integridade do gerador: o arquivo src/gerador_pomar.py não deve sofrer nenhuma alteração, conforme regra estipulada no enunciado.

---

## Cronograma dos 12 Commits Intercalados

| N | Responsável | Mensagem Exata do Commit | Artefato Principal | Situação |
|---|---|---|---|---|
| 1 | João Vítor | feat: estrutura inicial do projeto com gerador_pomar e configuracoes | .gitignore, requirements.txt, src/gerador_pomar.py | Concluído |
| 2 | João Vítor | feat: implementa buscas cegas e informadas (BFS, DFS, UCS, A*) com 4 contadores e reabertura de nos | src/buscas.py | Concluído |
| 3 | Caio Lúcio | feat: implementa busca local com subida de encosta e tempera simulada para k=15 | src/busca_local.py | Concluído |
| 4 | João Vítor | feat: implementa sistema especialista com encadeamento para tras e explicacao | src/especialista.py | Concluído |
| 5 | Caio Lúcio | feat: implementa modulo bayesiano para analise do sensor de pragas | src/bayes.py | Concluído |
| 6 | João Vítor | feat: implementa script principal src/main.py gerando pomar, csv e grafico | src/main.py, pasta resultados/ | Concluído |
| 7 | Caio Lúcio | test: executa analise de escalabilidade experimental e limites teoricos | src/escalabilidade.py | Concluído |
| 8 | João Vítor | feat: adiciona contraexemplo 8x8 para bonus da Liga de IA (DFS > 2x otimo) | src/contraexemplo_bonus.py | Concluído |
| 9 | Caio Lúcio | docs: elabora analise teorica PEAS, dimensoes de ambiente e auditoria AgroVision | RELATORIO.md (Partes 1, 2 e 5) | Concluído |
| 10 | João Vítor | docs: detalha analise de heuristicas, quebra da base especialista e metricas bayesianas | RELATORIO.md (Partes 3, 4 e Bônus) | Sua vez agora |
| 11 | Caio Lúcio | docs: elabora ANEXO_IA.md com registro obrigatorio, prompts, erro documentado e reflexao | ANEXO_IA.md | Aguardando |
| 12 | João Vítor | docs: finaliza README.md completo com instrucoes, tabela-resumo e mapa do repositorio | README.md | Aguardando |

---

## Instruções Detalhadas para o Caio (Commit 9)

Agora é a sua vez de desenvolver e enviar o Commit 9. Siga o roteiro abaixo:

1. Atualize seu repositório local:
   ```bash
   git pull origin main
   ```

2. Certifique-se de que a identificação de autoria está correta no seu Git:
   ```bash
   git config user.name "Caio Lúcio Almeida"
   git config user.email "kaiolucioalmeida@gmail.com"
   ```

3. Crie o arquivo `RELATORIO.md` estruturando as **Partes 1, 2 e 5** conforme o enunciado da Sprint 1:
   - **Parte 1 - O agente antes do código:**
     - 1.1 Ficha PEAS completa: Desempenho (métrica mensurável com unidade, ex.: custo operacional de deslocamento em litros de diesel ou R$), Ambiente, Atuadores e Sensores.
     - 1.2 Classificação nas 6 dimensões da Aula 02 com frases literais do cenário sustentando cada uma; identificação e justificativa técnica das 2 dimensões discutíveis (observabilidade e dinamismo).
     - 1.3 Tipo de agente escolhido e justificativa fundamentada nos objetivos do pomar.
     - 1.4 Métrica perversa: proposta de métrica aparentemente boa que gera comportamento disfuncional concreto em ponto específico do pomar, e a formulação da métrica corrigida.
   - **Parte 2 - Formulação e busca cega:**
     - 2.1 Cinco componentes do problema (estado inicial, ações, modelo de transição, teste de objetivo, custo do caminho) e contagem formal do espaço de estados (144 estados).
     - 2.2 Tabela preenchida com os resultados da semente oficial `24114066` para BFS, DFS e UCS (custo, passos, expandidos, fronteira máxima, otimalidade).
     - 2.3 Resposta formal sobre a violação de hipótese da Aula 03 (custos de transição heterogêneos onde passo unitário != custo uniforme).
     - 2.4 Síntese da escalabilidade experimental e limites teóricos com base nos dados obtidos em `src/escalabilidade.py` ($O(b^d)$ vs $O(b \cdot m)$ e RecursionError).
   - **Parte 5 - Auditoria do laudo técnico da AgroVision:**
     - Auditoria analítica das 5 afirmações do laudo comercial da concorrente, classificando cada uma em *Correta*, *Parcialmente Correta* ou *Incorreta*, sustentando obrigatoriamente com a teoria das Aulas 01 a 05 e com os **números experimentais medidos pela dupla** nos módulos `buscas.py`, `escalabilidade.py` e `bayes.py`.
     - Parágrafo de parecer final (máx. 8 linhas) com recomendação à diretoria da cooperativa (*contratar com ressalvas* ou *recusar*), especificando a condição técnica indispensável.

4. Realize o commit e envie para o GitHub com a mensagem combinada exata:
   ```bash
   git add RELATORIO.md INSTRUCOES_CAIO.md
   git commit -m "docs: elabora analise teorica PEAS, dimensoes de ambiente e auditoria AgroVision"
   git push origin main
   ```

5. Após o envio, avise João Vítor para que ele realize o fetch e assuma o Commit 10 (complementação do `RELATORIO.md` com as Partes 3, 4 e Bônus da Liga de IA).
