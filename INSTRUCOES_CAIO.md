# Painel de Coordenação da Dupla - Projeto Caatinga.AI

Este documento é um guia de sincronização e alinhamento entre João Vítor e Caio Lúcio. Seu objetivo é manter o fluxo de trabalho organizado, garantindo que o histórico de 12 commits no Git permaneça consistente, intercalado e autêntico.

---

## Status Atual do Projeto

- Último commit integrado: Commit 10 (realizado por João Vítor Almeida)
- Mensagem do commit 10: docs: detalha analise de heuristicas, quebra da base especialista e metricas bayesianas
- Artefatos entregues: RELATORIO.md (completo com todas as Partes 1 a 5 e Bônus)
- Próximo passo: Commit 11 (responsabilidade de Caio Lúcio Almeida)
- Módulo a desenvolver: ANEXO_IA.md (Parte 6 do enunciado: ferramentas, prompts na íntegra, erro documentado do assistente com evidência experimental e reflexão crítica)

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
| 10 | João Vítor | docs: detalha analise de heuristicas, quebra da base especialista e metricas bayesianas | RELATORIO.md (Partes 3, 4 e Bônus) | Concluído |
| 11 | Caio Lúcio | docs: elabora ANEXO_IA.md com registro obrigatorio, prompts, erro documentado e reflexao | ANEXO_IA.md | Sua vez agora |
| 12 | João Vítor | docs: finaliza README.md completo com instrucoes, tabela-resumo e mapa do repositorio | README.md | Aguardando |

---

## Instruções Detalhadas para o Caio (Commit 11)

Agora é a sua vez de desenvolver e enviar o Commit 11. Siga o roteiro abaixo:

1. Atualize seu repositório local:
   ```bash
   git pull origin main
   ```

2. Certifique-se de que a identificação de autoria está correta no seu Git:
   ```bash
   git config user.name "Caio Lúcio Almeida"
   git config user.email "kaiolucioalmeida@gmail.com"
   ```

3. Crie o arquivo `ANEXO_IA.md` atendendo rigorosamente à **Parte 6** do enunciado (Anexo obrigatório de uso de IA):
   - **A.1 Ferramentas Utilizadas:**
     Quais ferramentas de IA generativa foram empregadas pela dupla (ex.: Gemini 3.8 / ChatGPT / Copilot / DeepSeek) e em quais partes específicas do trabalho (apoio em algoritmos de busca, modelagem da busca local, inferência bayesiana, revisão de texto).
   - **A.2 Dois Prompts na Íntegra com Respostas Recebidas:**
     Transcrever literalmente dois prompts reais submetidos aos assistentes, acompanhados das respostas completas recebidas.
   - **A.3 Pelo Menos um Erro, Imprecisão ou Invenção do Assistente com Evidência Experimental:**
     Documentar um erro técnico real cometido pelo assistente durante a realização deste projeto.
     *Sugestão autêntica com evidência do nosso código:* O assistente inicialmente sugeriu que no A* não seria necessário reabrir nós visitados se a heurística de Manhattan fosse usada, ou afirmou que inflacionar Manhattan por 4 mantinha o caminho ótimo com menos nós. A evidência do experimento oficial (`resultados.csv`) desmentiu categoricamente essa afirmação, provando que o A* com $h_3$ devolveu rota subótima com custo 40 (enquanto o ótimo é 37). Outra opção de erro: o assistente afirmou inicialmente que a probabilidade a posteriori do sensor de pragas seria próxima da sensibilidade (95%), ignorando a Falácia da Taxa Base, o que foi desmentido pelo Teorema de Bayes em `bayes.py` ($VPP = 60,96\%$).
   - **A.4 Reflexão Final em Uma Frase:**
     Uma frase contundente respondendo: *"o que você sabia depois de rodar o código que não sabia lendo a resposta do assistente"*.

4. Realize o commit e envie para o GitHub com a mensagem combinada exata:
   ```bash
   git add ANEXO_IA.md INSTRUCOES_CAIO.md
   git commit -m "docs: elabora ANEXO_IA.md com registro obrigatorio, prompts, erro documentado e reflexao"
   git push origin main
   ```

5. Após o envio, avise João Vítor para que ele assuma o Commit 12 (finalização do `README.md` completo, fechando os 12 commits do repositório).
