# Painel de Coordenação da Dupla - Projeto Caatinga.AI

Este documento é um guia de sincronização e alinhamento entre João Vítor e Caio Lúcio. Seu objetivo é manter o fluxo de trabalho organizado, garantindo que o histórico de 12 commits no Git permaneça consistente, intercalado e autêntico.

---

## Status Atual do Projeto

- Último commit integrado: Commit 5 (realizado por Caio Lúcio Almeida)
- Mensagem do commit 5: feat: implementa modulo bayesiano para analise do sensor de pragas
- Artefatos entregues: src/bayes.py
- Próximo passo: Commit 6 (responsabilidade de João Vítor Almeida)
- Módulo a desenvolver: src/main.py (script principal gerando pomar, csv e grafico na pasta resultados/)

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
| 6 | João Vítor | feat: implementa script principal src/main.py gerando pomar, csv e grafico | src/main.py, pasta resultados/ | Sua vez agora |
| 7 | Caio Lúcio | test: executa analise de escalabilidade experimental e limites teoricos | src/escalabilidade.py | Aguardando |
| 8 | João Vítor | feat: adiciona contraexemplo 8x8 para bonus da Liga de IA (DFS > 2x otimo) | src/contraexemplo_bonus.py | Aguardando |
| 9 | Caio Lúcio | docs: elabora analise teorica PEAS, dimensoes de ambiente e auditoria AgroVision | RELATORIO.md (Partes 1, 2 e 5) | Aguardando |
| 10 | João Vítor | docs: detalha analise de heuristicas, quebra da base especialista e metricas bayesianas | RELATORIO.md (Partes 3, 4 e Bônus) | Aguardando |
| 11 | Caio Lúcio | docs: elabora ANEXO_IA.md com registro obrigatorio, prompts, erro documentado e reflexao | ANEXO_IA.md | Aguardando |
| 12 | João Vítor | docs: finaliza README.md completo com instrucoes, tabela-resumo e mapa do repositorio | README.md | Aguardando |

---

## Instruções Detalhadas para o Caio (Commit 5)

Agora é a sua vez de desenvolver e enviar o Commit 5. Siga o roteiro abaixo:

1. Atualize seu repositório local:
   ```bash
   git pull origin main
   ```

2. Certifique-se de que a identificação de autoria está correta no seu Git:
   ```bash
   git config user.name "Caio Lúcio Almeida"
   git config user.email "kaiolucioalmeida@gmail.com"
   ```

3. Desenvolva o arquivo src/bayes.py cobrindo os itens da Seção 4.3 do enunciado:
   - Obtenha os parâmetros do sensor para a semente oficial 24114066:
     prevalência: 0.047 (4.7%)
     sensibilidade: 0.95 (95.0%)
     taxa de falso positivo: 0.03 (3.0%)
     talhões por semana: 800
   - Implemente as quatro respostas e cálculos:
     (a) Teorema de Bayes para calcular P(infestado | sensor_positivo) mostrando a substituição formal:
         P(infestado | positivo) = [P(positivo | infestado) * P(infestado)] / P(positivo)
     (b) Taxa de alertas falsos: percentual de alertas do sensor que não correspondem a infestações reais (1 - P(infestado | positivo)). Complete a frase requerida: "a cada 100 alertas do meu sistema, cerca de X serão falsos."
     (c) Impacto no campo: com 800 talhões/semana, calcular o número esperado de alertas falsos e o custo em horas semanais de agrônomos (considerando 12 minutos por inspeção).
     (d) Cenário de aumento de sensibilidade para 99.9% mantendo taxa de falso positivo em 3%: calcular o novo valor preditivo positivo, discutir se houve melhora perceptível e justificar qual parâmetro agronômico/tecnológico deve ser atacado na prática (a redução da taxa de falsos positivos).

4. Realize o commit e envie para o GitHub com a mensagem combinada exata:
   ```bash
   git add src/bayes.py INSTRUCOES_CAIO.md
   git commit -m "feat: implementa modulo bayesiano para analise do sensor de pragas"
   git push origin main
   ```

5. Após o envio, avise João Vítor para que ele realize o fetch e assuma o Commit 6 (script principal unificado src/main.py).
