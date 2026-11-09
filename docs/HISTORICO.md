# Histórico do projeto

## 2026-11-01

- Lido o enunciado da competição e registrados requisitos e restrições.
- Criada estrutura para dados compartilhados, quatro modelos, resultados e apresentação.
- Criados modelos de documentação e notebooks iniciais sem execução.
- Nenhum dado foi baixado ou analisado e nenhum experimento foi executado.

## 2026-11-05 — Rede neural

- Criados dois notebooks em `Mod3_RN/`, com sigmoide, erro quadrático e retropropagação implementados com NumPy.
- O notebook 01 registra 584 configurações com atualização em lote. A diferença em relação à atualização após cada exemplo da aula foi explicitada.
- O notebook 02 usa atualização após cada exemplo, conforme a sequência da aula 6. Comparamos 54 configurações e duas extensões de épocas, mantendo a escolha pelo F1 macro nas cinco partes da divisão 42.
- A configuração escolhida do notebook 02 usa pressão sistólica, glicose, hemoglobina e triglicerídeos, 12 neurônios ocultos, taxa 0,1 e 800 épocas. Normalizamos pela média e desvio padrão e preenchemos vazios com a mediana, sempre calculados no treinamento.
- O F1 macro foi 88,70% na escolha e 85,58% nas 104 amostras reservadas. As conferências adicionais ficaram entre 88,20% e 88,67%. Os resultados completos e as limitações estão no notebook e em `Mod3_RN/experimentos/EXP_001.md`.
- Gerados os modelos salvos e os CSVs com 312 previsões. O arquivo da atualização após cada exemplo é `resultados/submissao_rede_neural_exemplos.csv`. Os modelos foram reabertos para conferir as previsões. Nenhum envio ao Kaggle foi feito nesta execução.

## 2026-11-05 — Combinações dos três modelos

- Comparadas 79.326 configurações de médias ponderadas, votação e outras regras, cobrindo os pares e o trio. Os componentes são o KNN K=11 original, a árvore de quatro atributos e a rede neural com atualização após cada exemplo.
- Conferido que os componentes reproduzem os três CSVs individuais e que a mistura original reproduz sua submissão. As matrizes de validação dos componentes também coincidem com os registros anteriores.
- A busca ampla usou as sementes 42, 73 e 101. Uma segunda seleção comparou 40 candidatas também nas sementes 21, 145 e 307. As conferências posteriores usaram as sementes 509 e 911, além das inicializações 19 e 31 da rede na divisão 42.
- A indicação usa 25% KNN, 42,5% árvore e 32,5% rede, com limite 45,5%. Seu F1 macro foi 91,37% na seleção e 88,44% nas 104 amostras reservadas. Acertou 92 amostras, um acerto a mais que a mistura original, sem perder acertos nessa reserva.
- A melhor dupla entre as candidatas da segunda seleção usa KNN e árvore com pesos iguais e limite 45%. Ficou com F1 macro 91,25% na seleção e 84,56% na reserva. O trio foi a indicação fixada pelo critério de seleção.
- Criados `Mod6_KNN_AD_RN/01_Combinacoes.ipynb`, a documentação e os registros completos em `resultados/combinacoes_tres_*`. A indicação principal é `resultados/submissao_combinacao_escolhida.csv`, com 312 previsões. Nenhum envio dessa nova regra ao Kaggle foi feito nesta execução.

## 2026-11-06 — Escala comum e Random Forest

- Adotada a fórmula `(valor − média) / desvio padrão` para os modelos das novas versões, por pedido do aluno. Os parâmetros são ajustados no treinamento de cada parte; o CSV padronizado conserva as unidades da exploração.
- Criado `Mod6_KNN_AD_RN/02_Combinacoes_escala_padrao.ipynb`. A mudança manteve as previsões da árvore e da rede e alterou o KNN. O F1 do KNN na reserva passou de 86,53% com quartis para 75,94% com média e desvio padrão.
- Repetida a busca de 79.326 misturas com a escala comum. Entre 39 finalistas, o trio escolhido usa 32,5% KNN, 42,5% árvore e 25% rede, com limite 45,5%. Teve F1 médio de 91,53% na seleção e 86,49% na reserva.
- Testadas Random Forest e a variante bagging com implementação NumPy. A busca inicial comparou 768 configurações. A segunda seleção incluiu variantes com sorteio de atributos e observou também 300 árvores nas trajetórias estendidas.
- A melhor Random Forest usa nove medidas, mediana, 300 árvores, mínimo de duas amostras por folha, sem limite fixo de profundidade e sorteio pela raiz quadrada do número de atributos. Teve F1 de 89,73% na seleção e 82,63% na reserva.
- O bagging escolhido usa quatro medidas, mediana, 100 árvores, mínimo de duas amostras por folha, profundidade 6 e todos os atributos por nó. Teve F1 de 90,30% na seleção e 87,49% na reserva. Foi a indicação entre as florestas pelo critério de seleção.
- Criados `Mod7_RF/01_Random_forest.ipynb`, modelos e registros. Gerados os CSVs de Random Forest e bagging, ambos com 312 previsões. Os modelos reabertos reproduziram as previsões. Nenhum envio ao Kaggle foi feito nesta execução.

## 2026-11-06 — Pausa e auditoria do pré-processamento

- Por pedido do aluno, pausamos as buscas de modelos e revisamos o pré-processamento e a avaliação.
- O notebook de exploração, executado em memória do início até antes da exportação, reconstruiu byte a byte o CSV padronizado. Conferimos as 20 duplicatas exatas, a preservação dos rótulos e a compatibilidade das transformações usadas na inferência.
- Conferidos os cabeçalhos, IDs, ordem e classes dos CSVs locais. Os dados e modelos foram preservados.
- Quantificados valores extremos, ausências e a mudança do peso relativo dos atributos na distância do KNN após a nova escala. Registradas as premissas sobre as unidades como pontos a discutir.
- Conferida a página oficial no navegador: placar identificado como F1 macro; enunciado solicita também precisão e recalls por classe. Atualizada essa informação na metodologia.
- Registradas as conclusões e limitações em `docs/REVISAO_PREPROCESSAMENTO.md`, com números agregados em `tmp/auditoria_preprocessamento.json`. Nenhum novo classificador foi treinado durante a auditoria.

## 2026-11-06 — Correção de unidades (Mod8 v1)

- Aplicada a hipótese de unidades levantada na revisão: 44 glicoses em mmol/L e 43 hemoglobinas em mmol/mol convertidas.
- KNN K=11 só com glicose e HbA1c (mín-máx, Euclidiana): F1 0,887 na validação 5×5. Kaggle: 0,85692.
- Média das probabilidades de KNN, árvore e rede: Kaggle 0,86649.

## 2026-11-06 — Um modelo por padrão de ausência (Mod8 v2)

- Diagnóstico: 100% dos diabéticos sem nenhum exame e 35% dos que tinham só glicose eram perdidos pelo KNN v1.
- Cada modelo passou a ter 4 submodelos (os dois exames / só glicose / só HbA1c / nenhum), com atributos clínicos quando falta exame.
- Testada também a estimativa dos ausentes por KNN (KNNImputer): pior, cerca de 0,88.
- Validação 5×4: voto dos 3 0,913; média dos 3 0,914 (v1: 0,899 nas mesmas partes). Escolha na semente 2026, confirmação na 777.
- Kaggle: voto dos 3 = **0,89900**.

## 2026-11-07 — Random Forest e análise dos erros

- Random Forest por padrão de ausência: 0,909–0,917 sozinha, sem ganho ao combinar. Não adotada.
- Erros restantes: 39% são diabéticos com os dois exames normais; usar clínicos nesse padrão piorou o resultado.
- Detalhes completos em `Mod8_Unidades/README.md`.

## 2026-11-08 — Modelos 9, 10 e 11 (componentes separados)

- Criados `Mod9_KNN_Padroes/`, `Mod10_AD_Padroes/` e `Mod11_RN_Padroes/`, cada um com notebook executado, README detalhado, `limpeza.py`, `padroes.py` e CSV de submissão.
- Busca refeita em cada notebook (semente 2026) e avaliação final com a semente 777: KNN 0,896; árvore 0,894; rede 0,887.
- Conferido que o voto da maioria entre os três CSVs é idêntico ao `submissao_voto3_padroes.csv` do Modelo 8.

## 2026-11-08 — Correção da atividade física

- `Moderat` e `Intensive` passaram a ser reconhecidas (antes viravam ausentes). 3 pacientes no treino, 6 no teste.
- Modelos 8 a 11 reexecutados. Voto dos 3: 0,912 na validação (antes 0,913); média dos 3: 0,915. No teste, voto e média mudam 1 paciente cada.
- Na busca da árvore, "sem limite com folha 10" empatou com "profundidade 4 com folha 5" (0,898); mantida a árvore mais compacta.
- Figuras da apresentação regeneradas com os números corrigidos.

