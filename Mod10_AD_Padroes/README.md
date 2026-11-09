# Modelo 10 — Árvore de decisão por padrão de exames

## Resumo

| Item | Valor |
|---|---|
| Algoritmo | Árvore de decisão com ganho de informação (entropia) |
| Controles de tamanho | Profundidade máxima 4; mínimo de 5 pacientes por folha |
| Tratamento de ausentes | Um submodelo por padrão de exames (glicose / HbA1c) |
| F1-macro na validação (semente 777, 5×4) | **0,894 ± 0,027** |
| Submissão | `submissao_arvore_padroes.csv` |
| Origem | Componente árvore do voto do Modelo 8 (0,89900 no Kaggle), separado para submissão individual |

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `prever.py` | **Para executar:** treina com a base de treino e classifica qualquer CSV no formato do Kaggle |
| `validar.py` | Reproduz a validação cruzada 5 partes × 4 repetições e mostra as métricas e a matriz de confusão |
| `modelo_final.py` | Definição do modelo (árvore com entropia, profundidade 4, folha 5) |
| `limpeza.py` | Tratamento da base: duplicatas, grafias, unidades, valores impossíveis, extremos (igual nos Modelos 8 a 11) |
| `padroes.py` | Um submodelo por padrão de exames, combinação, validação cruzada e métricas (igual nos Modelos 8 a 11) |
| `01_Arvore_padroes.ipynb` | Notebook completo e executado, com gráficos |
| `submissao_arvore_padroes.csv` | 312 previsões do teste no formato `id,class` |

## Como executar (Linux / Fedora)

Instale uma vez, na raiz do repositório (detalhes no README principal):

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Depois, nesta pasta:

```bash
cd Mod10_AD_Padroes
python3 prever.py ../dados/kaggle-test/test.csv            # gera previsoes.csv (igual a submissao_arvore_padroes.csv)
python3 prever.py /caminho/para/externo.csv --saida previsoes_externo.csv
python3 validar.py                                         # refaz a validação cruzada do README
```

O tratamento da base (`limpeza.py`) é aplicado automaticamente ao treino e ao arquivo classificado. Se o arquivo tiver a coluna `class`, `prever.py` também mostra F1-macro, precisão, recall de cada classe e a matriz de confusão (VN, FP, FN, VP). O treino vem de `../dados/kaggle-training/train.csv` (outro arquivo: `--treino`).

O notebook `01_Arvore_padroes.ipynb` tem o passo a passo com gráficos. Para reexecutá-lo: `jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=3000 01_Arvore_padroes.ipynb` (menos de 30 segundos).

---


## 1. Limpeza dos dados (Aula 2)

A limpeza é a mesma dos Modelos 9 e 11. A principal correção é a de **unidades**:

- **Glicose:** 44 valores em mmol/L viram mg/dL (× 18,016).
- **HbA1c:** 43 valores em mmol/mol viram % (0,09148 × v + 2,152).

Também foram corrigidos duplicatas, peso em libras, triglicerídeos extremos, altura em metros, pressão como texto e grafias diferentes. O detalhamento está no README do Modelo 9 e em `limpeza.py`.

## 2. Valores ausentes: um submodelo por padrão (Aula 2)

| Padrão | Treino | Teste | Atributos do submodelo |
|---|---|---|---|
| Glicose e HbA1c | 357 | 222 | glicose, HbA1c |
| Só glicose | 104 | 53 | glicose + clínicos |
| Só HbA1c | 41 | 26 | HbA1c + clínicos |
| Nenhum exame | 18 | 11 | só clínicos |

Clínicos: triglicerídeos, pressão sistólica, IMC, idade, histórico familiar e atividade física. Cada paciente vai para a árvore treinada com os atributos que ele tem, em vez de receber um exame "inventado" pela mediana.

## 3. O algoritmo (Aula 5)

Em cada nó, a árvore testa todos os atributos e pontos de corte e escolhe o de **maior ganho de informação**, isto é, a maior queda da **entropia** das classes. Como os atributos são numéricos, cada teste é binário (`atributo <= corte`).

- **Não precisa de normalização:** cada corte compara valores de um único atributo.
- **Profundidade máxima e mínimo por folha** impedem que a árvore decore o treino.
- **Variação testada:** índice de Gini, que deu empate (0,897 contra 0,894). Mantivemos a entropia, que é o critério da aula.

## 4. Escolha dos hiperparâmetros (Aula 7)

Validação cruzada estratificada, 5 partes × 4 repetições, semente 2026. F1-macro:

| Profundidade \ mínimo por folha | 1 | **5** | 10 |
|---|---|---|---|
| 2 | 0,884 | 0,884 | 0,884 |
| 3 | 0,890 | 0,891 | 0,891 |
| **4** | 0,894 | **0,898** | 0,889 |
| 5 | 0,886 | 0,895 | 0,891 |
| 6 | 0,881 | 0,895 | 0,895 |
| sem limite | 0,874 | 0,886 | 0,898 |

O padrão é o esperado da aula: com folha mínima 1 e sem limite de profundidade, a árvore decora o treino e cai para 0,874. Com algum controle, fica entre 0,89 e 0,90.

**Decisão:** profundidade 4 com folha 5 e "sem limite" com folha 10 empatam em 0,898 (diferença na quarta casa decimal, muito menor que o desvio de 0,027). Escolhemos a **árvore mais compacta**, de profundidade 4: é mais fácil de ler e explicar e tende a generalizar melhor (aula 5, árvores compactas). É também a árvore do voto do Modelo 8.

## 5. As regras aprendidas (bom para os slides)

Submodelo **glicose e HbA1c**, treinado com todo o treino (resumido):

```
HbA1c > 6,38  ............................................ diabetes
HbA1c <= 6,38
   glicose > 144  ........................................ diabetes
   glicose <= 144
      glicose <= 122,25  ................................. controle
      glicose > 122,25
         HbA1c <= 5,95  .................................. diabetes
         HbA1c > 5,95  ................................... controle
```

A árvore redescobriu sozinha um corte de HbA1c muito próximo do critério clínico de diabetes (≥ 6,5%). O submodelo "só glicose" usa triglicerídeos, idade, pressão e IMC quando a glicose está abaixo de 120,5. A árvore completa está no notebook.

## 6. Resultado (Aula 7)

Avaliação com **outra semente (777)**:

| Métrica | Média | Desvio padrão |
|---|---|---|
| **F1-macro** | **0,894** | 0,027 |
| Acurácia | 0,894 | 0,027 |
| Precisão macro | 0,895 | 0,026 |
| Recall diabetes | 0,881 | 0,043 |
| Recall controle | 0,907 | 0,042 |

Matriz de confusão (média por repetição):

| | Previsto controle | Previsto diabetes |
|---|---|---|
| **Real controle (250)** | 226,8 | 23,2 |
| **Real diabetes (270)** | 32,0 | 238,0 |

A árvore é a mais equilibrada dos três modelos: tem o maior recall de diabetes (0,88), à custa de mais alarmes falsos que o KNN.

### Onde erra

| Padrão | Classe | Pacientes | Erros médios | Taxa |
|---|---|---|---|---|
| Glicose e HbA1c | controle | 173 | 6,0 | 3% |
| Glicose e HbA1c | diabetes | 184 | 14,5 | 8% |
| Só glicose | controle | 47 | 9,5 | 20% |
| Só glicose | diabetes | 57 | 12,3 | 21% |
| Só HbA1c | ambas | 41 | 5,3 | 13% |
| Nenhum exame | ambas | 18 | 7,8 | 43% |

O ponto fraco é o grupo "nenhum exame": só 18 pacientes, poucos para uma árvore aprender bem.

## 7. Previsão do teste

312 pacientes, 47,8% previstos como diabetes. O arquivo foi conferido no notebook.

## 8. Relação com os outros modelos

| Modelo | F1 validação (777) | % diabetes no teste |
|---|---|---|
| 9 — KNN | 0,896 | 44,6% |
| **10 — Árvore** | **0,894** | 47,8% |
| 11 — Rede neural | 0,886 | 49,4% |
| 8 — Voto dos 3 | 0,912 | 45,8% |

O voto da maioria entre os CSVs dos Modelos 9, 10 e 11 reproduz exatamente o CSV do voto do Modelo 8.

## 9. Perguntas prováveis na apresentação

- **Por que profundidade 4 e folha 5?** Empatou com o maior F1 da busca (0,898), e entre as melhores é a árvore mais compacta, mais fácil de ler e explicar.
- **Por que não usar os atributos clínicos quando há os dois exames?** O resultado piorou (0,891 contra 0,898, semente 2026), e a árvore fica menos legível.
- **A árvore precisa de normalização?** Não. Ela compara valores dentro de cada atributo.
- **O teste foi usado?** Não. Tudo foi escolhido por validação cruzada no treino.
