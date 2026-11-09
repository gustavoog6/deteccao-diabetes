# Modelo 9 — KNN por padrão de exames

## Resumo

| Item | Valor |
|---|---|
| Algoritmo | K-vizinhos mais próximos (KNN), K = 11 |
| Distância | Euclidiana, com atributos padronizados por média e desvio padrão |
| Decisão | Voto simples: classe mais frequente entre os 11 vizinhos |
| Tratamento de ausentes | Um submodelo por padrão de exames (glicose / HbA1c) |
| F1-macro na validação (semente 777, 5×4) | **0,896 ± 0,024** |
| Submissão | `submissao_knn_padroes.csv` |
| Origem | Componente KNN do voto do Modelo 8 (0,89900 no Kaggle), separado para submissão individual |

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `prever.py` | **Para executar:** treina com a base de treino e classifica qualquer CSV no formato do Kaggle |
| `validar.py` | Reproduz a validação cruzada 5 partes × 4 repetições e mostra as métricas e a matriz de confusão |
| `modelo_final.py` | Definição do modelo (KNN K=11) |
| `limpeza.py` | Tratamento da base: duplicatas, grafias, unidades, valores impossíveis, extremos (igual nos Modelos 8 a 11) |
| `padroes.py` | Um submodelo por padrão de exames, combinação, validação cruzada e métricas (igual nos Modelos 8 a 11) |
| `01_KNN_padroes.ipynb` | Notebook completo e executado, com gráficos |
| `submissao_knn_padroes.csv` | 312 previsões do teste no formato `id,class` |

## Como executar (Linux / Fedora)

Instale uma vez, na raiz do repositório (detalhes no README principal):

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Depois, nesta pasta:

```bash
cd Mod9_KNN_Padroes
python3 prever.py ../dados/kaggle-test/test.csv            # gera previsoes.csv (igual a submissao_knn_padroes.csv)
python3 prever.py /caminho/para/externo.csv --saida previsoes_externo.csv
python3 validar.py                                         # refaz a validação cruzada do README
```

O tratamento da base (`limpeza.py`) é aplicado automaticamente ao treino e ao arquivo classificado. Se o arquivo tiver a coluna `class`, `prever.py` também mostra F1-macro, precisão, recall de cada classe e a matriz de confusão (VN, FP, FN, VP). O treino vem de `../dados/kaggle-training/train.csv` (outro arquivo: `--treino`).

O notebook `01_KNN_padroes.ipynb` tem o passo a passo com gráficos. Para reexecutá-lo: `jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=3000 01_KNN_padroes.ipynb` (menos de 1 minuto).

---


## 1. Limpeza dos dados (Aula 2 — qualidade dos dados)

| Problema | Correção |
|---|---|
| 20 registros duplicados | Removidos (520 pacientes restantes) |
| Glicose em duas unidades: 44 valores de 3,1 a 21,3 (mmol/L) | Valor < 35 → × 18,016 (para mg/dL) |
| HbA1c em duas unidades: 43 valores de 27 a 116 (mmol/mol) | Valor > 20 → 0,09148 × v + 2,152 (para %) |
| Peso em libras (23 valores > 140) | ÷ 2,2046 |
| Triglicerídeos extremos (até 5.310) | Limitados a 1000 |
| Altura em metros, pressão como texto, grafias diferentes, idade 0/999 | Padronizados (ver `limpeza.py`) |

A correção de unidades é a decisão que mais pesa no resultado. Antes dela, a mesma glicose "7" (mmol/L) parecia um valor absurdamente baixo, quando na verdade equivale a 126 mg/dL, o limite de diabetes.

## 2. Valores ausentes: um submodelo por padrão (Aula 2)

| Padrão | Treino | Teste | Atributos do submodelo |
|---|---|---|---|
| Glicose e HbA1c | 357 (69%) | 222 (71%) | glicose, HbA1c |
| Só glicose | 104 (20%) | 53 (17%) | glicose + clínicos |
| Só HbA1c | 41 (8%) | 26 (8%) | HbA1c + clínicos |
| Nenhum exame | 18 (3%) | 11 (4%) | só clínicos |

Clínicos: triglicerídeos, pressão sistólica, IMC, idade, histórico familiar e atividade física.

**Por quê:** preencher o exame ausente com a mediana fazia o paciente parecer saudável. No KNN antigo, 100% dos diabéticos sem exame e 35% dos que só tinham glicose eram classificados como controle. A aula 2 lista "ignorar o atributo ausente" como opção. Aqui, cada paciente é comparado só com atributos que ele realmente tem.

Cada submodelo é treinado com **todos** os pacientes do treino que têm os exames de que ele precisa. Por exemplo, o submodelo "só glicose" usa os 461 pacientes com glicose, não só os 104 sem HbA1c.

## 3. O algoritmo (Aulas 3, 5 e 10)

1. **Padronização:** `(valor − média) / desvio padrão` (Aula 10, p. 16), com média e desvio calculados só no treino de cada parte. Sem isso, a glicose (≈ 100) dominaria a HbA1c (≈ 6) na distância.
2. **Distância Euclidiana** (Aulas 3 e 5) até os pacientes do treino.
3. **11 vizinhos mais próximos.**
4. **Voto simples:** classe mais frequente. Com K ímpar não há empate.

O notebook mostra um paciente de fronteira (glicose 79, HbA1c 6,4) cujos 11 vizinhos votam 6 × 5. É um bom exemplo para os slides.

## 4. Escolha de K (Aula 7 — validação cruzada)

Validação cruzada estratificada, 5 partes × 4 repetições, semente 2026, só no treino.

| K | 3 | 5 | 7 | 9 | **11** | 15 | 21 |
|---|---|---|---|---|---|---|---|
| F1-macro | 0,887 | 0,893 | 0,895 | 0,898 | **0,900** | 0,896 | 0,892 |

Com K pequeno, o modelo segue o ruído de poucos vizinhos. Com K grande, mistura pacientes diferentes, e o recall de diabetes cai de 0,86 para 0,84.

**Variações testadas e descartadas:** normalização mín-máx da aula 5 (0,883, pior); distância Manhattan da aula 3 (0,900, empate).

## 5. Resultado (Aula 7 — métricas)

Avaliação com **outra semente (777)**, diferente da usada na escolha de K:

| Métrica | Média | Desvio padrão |
|---|---|---|
| **F1-macro** | **0,896** | 0,024 |
| Acurácia | 0,896 | 0,023 |
| Precisão macro | 0,900 | 0,022 |
| Recall diabetes | 0,854 | 0,040 |
| Recall controle | 0,942 | 0,027 |

Matriz de confusão (média por repetição):

| | Previsto controle | Previsto diabetes |
|---|---|---|
| **Real controle (250)** | 235,5 | 14,5 |
| **Real diabetes (270)** | 39,5 | 230,5 |

O KNN é o mais "conservador" dos três modelos: quase não dá alarme falso (recall de controle 0,94), mas deixa passar mais diabéticos.

### Onde erra

| Padrão | Classe | Pacientes | Erros médios | Taxa |
|---|---|---|---|---|
| Glicose e HbA1c | controle | 173 | 2,3 | 1% |
| Glicose e HbA1c | diabetes | 184 | 22,3 | 12% |
| Só glicose | controle | 47 | 9,3 | 20% |
| Só glicose | diabetes | 57 | 11,5 | 20% |
| Só HbA1c | ambas | 41 | 4,8 | 12% |
| Nenhum exame | ambas | 18 | 4,0 | 22% |

O maior grupo de erros são diabéticos com glicose e HbA1c normais (provavelmente pacientes tratados ou ruído da parte artificial da base). Só com os exames, o KNN não tem como identificá-los.

## 6. Previsão do teste

312 pacientes, 44,6% previstos como diabetes. O arquivo foi conferido no notebook: mesmas linhas e ordem de `id` do teste, classes 0/1.

## 7. Relação com os outros modelos

| Modelo | F1 validação (777) | % diabetes no teste |
|---|---|---|
| **9 — KNN** | **0,896** | 44,6% |
| 10 — Árvore | 0,894 | 47,8% |
| 11 — Rede neural | 0,886 | 49,4% |
| 8 — Voto dos 3 | 0,912 | 45,8% |

O voto da maioria entre os CSVs dos Modelos 9, 10 e 11 reproduz exatamente o CSV do voto do Modelo 8.

## 8. Perguntas prováveis na apresentação

- **Por que K = 11?** Foi o maior F1 na validação cruzada, e os vizinhos (9 e 15) ficam próximos, então não é um pico isolado.
- **Por que padronizar?** Para a glicose, que vai até 500, não dominar a HbA1c, que vai até 13.
- **O teste foi usado?** Não. K foi escolhido por validação cruzada no treino, e a avaliação final usa outra semente.
- **Por que o KNN não usa os atributos clínicos quando tem os dois exames?** Com padronização, cada atributo clínico pesaria na distância tanto quanto um exame, e o resultado piorou (0,875 contra 0,900 com só os exames, semente 2026).
