# Modelo 11 — Rede neural por padrão de exames

## Resumo

| Item | Valor |
|---|---|
| Algoritmo | Rede neural com 1 camada oculta de 8 neurônios sigmoide e saída sigmoide |
| Entrada | Atributos padronizados por média e desvio padrão; exames + clínicos |
| Treino | Retropropagação com otimizador Adam, até 3000 épocas |
| Tratamento de ausentes | Um submodelo por padrão de exames (glicose / HbA1c) |
| F1-macro na validação (semente 777, 5×4) | **0,886 ± 0,031** |
| Submissão | `submissao_rede_padroes.csv` |
| Origem | Componente rede do voto do Modelo 8 (0,89900 no Kaggle), separado para submissão individual |

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `prever.py` | **Para executar:** treina com a base de treino e classifica qualquer CSV no formato do Kaggle |
| `validar.py` | Reproduz a validação cruzada 5 partes × 4 repetições e mostra as métricas e a matriz de confusão |
| `modelo_final.py` | Definição do modelo (rede neural com 8 neurônios) |
| `limpeza.py` | Tratamento da base: duplicatas, grafias, unidades, valores impossíveis, extremos (igual nos Modelos 8 a 11) |
| `padroes.py` | Um submodelo por padrão de exames, combinação, validação cruzada e métricas (igual nos Modelos 8 a 11) |
| `01_Rede_neural_padroes.ipynb` | Notebook completo e executado, com gráficos |
| `submissao_rede_padroes.csv` | 312 previsões do teste no formato `id,class` |

## Como executar (Linux / Fedora)

Instale uma vez, na raiz do repositório (detalhes no README principal):

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Depois, nesta pasta:

```bash
cd Mod11_RN_Padroes
python3 prever.py ../dados/kaggle-test/test.csv            # gera previsoes.csv (igual a submissao_rede_padroes.csv)
python3 prever.py /caminho/para/externo.csv --saida previsoes_externo.csv
python3 validar.py                                         # refaz a validação cruzada do README
```

O tratamento da base (`limpeza.py`) é aplicado automaticamente ao treino e ao arquivo classificado. Se o arquivo tiver a coluna `class`, `prever.py` também mostra F1-macro, precisão, recall de cada classe e a matriz de confusão (VN, FP, FN, VP). O treino vem de `../dados/kaggle-training/train.csv` (outro arquivo: `--treino`).

O notebook `01_Rede_neural_padroes.ipynb` tem o passo a passo com gráficos. Para reexecutá-lo: `jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=3000 01_Rede_neural_padroes.ipynb` (cerca de 4 minutos).

---


## 1. Limpeza dos dados (Aula 2)

A limpeza é a mesma dos Modelos 9 e 10. A principal correção é a de **unidades**:

- **Glicose:** 44 valores em mmol/L viram mg/dL (× 18,016).
- **HbA1c:** 43 valores em mmol/mol viram % (0,09148 × v + 2,152).

O detalhamento está no README do Modelo 9 e em `limpeza.py`.

## 2. Valores ausentes: um submodelo por padrão (Aula 2)

| Padrão | Treino | Teste | Atributos do submodelo |
|---|---|---|---|
| Glicose e HbA1c | 357 | 222 | glicose, HbA1c **+ clínicos** |
| Só glicose | 104 | 53 | glicose + clínicos |
| Só HbA1c | 41 | 26 | HbA1c + clínicos |
| Nenhum exame | 18 | 11 | só clínicos |

Clínicos: triglicerídeos, pressão sistólica, IMC, idade, histórico familiar e atividade física.

**Diferença em relação ao KNN e à árvore:** a rede usa os atributos clínicos **também** para quem tem os dois exames. Ela aprende pesos para cada entrada e pode dar peso pequeno ao que ajuda pouco. No KNN, ao contrário, todo atributo pesa igual na distância. Na validação do Modelo 8, essa versão foi melhor para a rede.

## 3. O algoritmo (Aula 6)

```
entradas padronizadas ──► 8 neurônios ocultos ──► 1 neurônio de saída ──► ≥ 0,5 → diabetes
   (exames + clínicos)      soma ponderada + viés     soma ponderada + viés
                            → sigmoide                → sigmoide
```

| Elemento | Aula 6 |
|---|---|
| Soma ponderada das entradas + viés | p. 6 |
| Ativação sigmoide | p. 7 |
| Propagação para a frente (feed-forward) | p. 9, 10 e 12 |
| Saída binária com limite 0,5 | p. 11 |
| Erro e gradiente | p. 15 e 16 |
| Épocas | p. 17 |
| Número de neurônios escolhido por validação cruzada | p. 19 |
| Retropropagação | p. 21 a 23 |

**Diferença em relação ao slide 17:** o slide atualiza os pesos com gradiente descendente simples após cada exemplo. Aqui usamos o **Adam**, uma variação do gradiente descendente que ajusta o tamanho do passo de cada peso automaticamente, com uma pequena penalização dos pesos grandes (`alpha = 0,001`). A retropropagação e a sigmoide são as mesmas.

No teste feito no Modelo 8, a rede exatamente como no slide 17 teve F1 0,874 sozinha, contra 0,897 com Adam. Dentro do voto dos 3, a diferença cai para 0,911 contra 0,915.

## 4. Escolha do número de neurônios (Aula 6, p. 19, e Aula 7)

Validação cruzada estratificada, 5 partes × 4 repetições, semente 2026:

| Neurônios | 2 | 4 | **8** | 16 |
|---|---|---|---|---|
| F1-macro | 0,899 | 0,890 | **0,894** | 0,897 |
| Desvio padrão | 0,030 | 0,031 | 0,030 | 0,030 |

**Decisão: 8 neurônios.** O maior valor foi com 2, mas a diferença para 8 (0,004) é **muito menor que o desvio padrão** entre as partes (0,03), o que na prática é empate. Mantivemos 8, a configuração usada no voto do Modelo 8. Assim este modelo é exatamente o componente que foi submetido no voto, e os Modelos 9, 10 e 11 reproduzem aquele voto. A decisão está registrada no notebook.

## 5. Sensibilidade à inicialização

A rede começa com pesos sorteados. Repetimos a avaliação com 5 inicializações diferentes (semente 777, 5 partes):

| Inicialização | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| F1-macro | 0,890 | 0,890 | 0,888 | 0,888 | 0,894 |

Variação de 0,888 a 0,894: o resultado não depende de um sorteio de sorte.

## 6. Resultado (Aula 7)

Avaliação com **outra semente (777)**:

| Métrica | Média | Desvio padrão |
|---|---|---|
| **F1-macro** | **0,886** | 0,031 |
| Acurácia | 0,887 | 0,031 |
| Precisão macro | 0,888 | 0,030 |
| Recall diabetes | 0,870 | 0,047 |
| Recall controle | 0,904 | 0,047 |

Matriz de confusão (média por repetição):

| | Previsto controle | Previsto diabetes |
|---|---|---|
| **Real controle (250)** | 226,0 | 24,0 |
| **Real diabetes (270)** | 35,0 | 235,0 |

### Onde erra

| Padrão | Classe | Pacientes | Erros médios | Taxa |
|---|---|---|---|---|
| Glicose e HbA1c | controle | 173 | 13,8 | 8% |
| Glicose e HbA1c | diabetes | 184 | 21,8 | 12% |
| Só glicose | controle | 47 | 7,5 | 16% |
| Só glicose | diabetes | 57 | 8,5 | 15% |
| Só HbA1c | ambas | 41 | 2,5 | 6% |
| Nenhum exame | ambas | 18 | 5,0 | 28% |

A rede é a melhor dos três nos pacientes **sem algum exame** (15% de erro em "só glicose", contra 20% do KNN e da árvore). Isso faz sentido, porque é ela que aproveita melhor os atributos clínicos. Em troca, erra mais controles com os dois exames (8%, contra 1% do KNN). É por isso que os três se complementam no voto.

## 7. Previsão do teste

312 pacientes, 49,4% previstos como diabetes. É o modelo que mais aponta diabetes. O arquivo foi conferido no notebook.

## 8. Relação com os outros modelos

| Modelo | F1 validação (777) | % diabetes no teste |
|---|---|---|
| 9 — KNN | 0,896 | 44,6% |
| 10 — Árvore | 0,894 | 47,8% |
| **11 — Rede neural** | **0,886** | 49,4% |
| 8 — Voto dos 3 | 0,912 | 45,8% |

O voto da maioria entre os CSVs dos Modelos 9, 10 e 11 reproduz exatamente o CSV do voto do Modelo 8.

## 9. Perguntas prováveis na apresentação

- **Por que 8 neurônios se 2 deu mais?** A diferença é muito menor que a variação entre as partes. É empate, e 8 é o componente do voto já validado no Kaggle.
- **Por que Adam e não o gradiente do slide?** Convergiu melhor (0,897 contra 0,874 sozinha). A estrutura da rede, a sigmoide e a retropropagação são as da aula.
- **Por que a rede usa os clínicos mesmo com os dois exames?** Porque ela aprende o peso de cada entrada, e na validação ficou melhor assim.
- **O resultado depende da inicialização?** Pouco: entre 0,888 e 0,894 com 5 inicializações diferentes.
