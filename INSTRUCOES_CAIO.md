# Painel de Coordenação da Dupla - Projeto Caatinga.AI

Este documento é um guia de sincronização e alinhamento entre João Vítor e Caio Lúcio. Seu objetivo é manter o fluxo de trabalho organizado, garantindo que o histórico de 12 commits no Git permaneça consistente, intercalado e autêntico.

---

## Status Atual do Projeto

- Último commit integrado: Commit 7 (realizado por Caio Lúcio Almeida)
- Mensagem do commit 7: test: executa analise de escalabilidade experimental e limites teoricos
- Artefatos entregues: src/escalabilidade.py
- Próximo passo: Commit 8 (responsabilidade de João Vítor Almeida)
- Módulo a desenvolver: src/contraexemplo_bonus.py (adiciona contraexemplo 8x8 para bonus da Liga de IA onde DFS > 2x otimo)

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
| 8 | João Vítor | feat: adiciona contraexemplo 8x8 para bonus da Liga de IA (DFS > 2x otimo) | src/contraexemplo_bonus.py | Sua vez agora |
| 9 | Caio Lúcio | docs: elabora analise teorica PEAS, dimensoes de ambiente e auditoria AgroVision | RELATORIO.md (Partes 1, 2 e 5) | Aguardando |
| 10 | João Vítor | docs: detalha analise de heuristicas, quebra da base especialista e metricas bayesianas | RELATORIO.md (Partes 3, 4 e Bônus) | Aguardando |
| 11 | Caio Lúcio | docs: elabora ANEXO_IA.md com registro obrigatorio, prompts, erro documentado e reflexao | ANEXO_IA.md | Aguardando |
| 12 | João Vítor | docs: finaliza README.md completo com instrucoes, tabela-resumo e mapa do repositorio | README.md | Aguardando |

---

## Instruções Detalhadas para o Caio (Commit 7)

Agora é a sua vez de desenvolver e enviar o Commit 7. Siga o roteiro abaixo:

1. Atualize seu repositório local:
   ```bash
   git pull origin main
   ```

2. Certifique-se de que a identificação de autoria está correta no seu Git:
   ```bash
   git config user.name "Caio Lúcio Almeida"
   git config user.email "kaiolucioalmeida@gmail.com"
   ```

3. Desenvolva o script `src/escalabilidade.py` cobrindo o item 2.4 do enunciado:
   - Aumente a dimensão do pomar $n$ progressivamente:
     Exemplo: $n = 12, 20, 40, 60, 80, 100, 120, 150 \dots$ até que uma das estratégias de busca (BFS, DFS ou UCS) falhe por estouro de memória, estouro de profundidade/recursão ou timeout (> 60 segundos).
   - Use o gerador oficial `gerar_pomar(matricula, n=n)` para a semente oficial `24114066`.
   - Registre e imprima em formato de tabela comparativa:
     - Valor de $n$
     - Tempo gasto por cada algoritmo (BFS, DFS, UCS, A*)
     - Memória máxima ou nós na fronteira máxima
     - Registro explícito de qual estratégia falhou primeiro, em qual $n$ falhou, e a identificação do limite teórico atingido (relacionando com a fórmula da Aula 03: complexidade espacial $O(b^d)$ vs $O(b \cdot m)$).

4. Realize o commit e envie para o GitHub com a mensagem combinada exata:
   ```bash
   git add src/escalabilidade.py INSTRUCOES_CAIO.md
   git commit -m "test: executa analise de escalabilidade experimental e limites teoricos"
   git push origin main
   ```

5. Após o envio, avise João Vítor para que ele assuma o Commit 8 (módulo do contraexemplo bônus da Liga de IA em `src/contraexemplo_bonus.py`).
