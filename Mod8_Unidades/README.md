# Mod8 — Modelo final: voto dos 3 por padrão de exames

Este é o **modelo final** do trabalho: KNN, árvore e rede neural, cada um com um submodelo por padrão de exames, combinados pelo voto da maioria. F1-macro de 0,912 na validação cruzada e 0,89900 no placar público do Kaggle. Os três componentes também estão separados nos Modelos 9, 10 e 11.

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `prever.py` | **Para executar:** treina com a base de treino e classifica qualquer CSV no formato do Kaggle |
| `validar.py` | Reproduz a validação cruzada 5 partes × 4 repetições e mostra as métricas e a matriz de confusão |
| `modelo_final.py` | Definição do modelo (voto da maioria entre KNN, árvore e rede neural) |
| `limpeza.py` | Tratamento da base: duplicatas, grafias, unidades, valores impossíveis, extremos (igual nos Modelos 8 a 11) |
| `padroes.py` | Um submodelo por padrão de exames, combinação, validação cruzada e métricas (igual nos Modelos 8 a 11) |
| `submissao_media3_padroes.csv` | Previsões da média dos 3 (troque `REGRA = 'media'` em `modelo_final.py`) |
| `modelo.py`, `modelo_padroes.py` | Scripts originais da v1 e da v2, mantidos como registro |
| `submissao_*_unidades.csv`, `submissao_rf_padroes.csv` | Submissões antigas (v1 e teste com Random Forest) |
| `submissao_voto3_padroes.csv` | 312 previsões do teste no formato `id,class` |

## Como executar (Linux / Fedora)

Instale uma vez, na raiz do repositório (detalhes no README principal):

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Depois, nesta pasta:

```bash
cd Mod8_Unidades
python3 prever.py ../dados/kaggle-test/test.csv            # gera previsoes.csv (igual a submissao_voto3_padroes.csv)
python3 prever.py /caminho/para/externo.csv --saida previsoes_externo.csv
python3 validar.py                                         # refaz a validação cruzada do README
```

O tratamento da base (`limpeza.py`) é aplicado automaticamente ao treino e ao arquivo classificado. Se o arquivo tiver a coluna `class`, `prever.py` também mostra F1-macro, precisão, recall de cada classe e a matriz de confusão (VN, FP, FN, VP). O treino vem de `../dados/kaggle-training/train.csv` (outro arquivo: `--treino`).

---

A partir daqui, o README registra a evolução do Modelo 8 (v1 e v2), na ordem em que foi feita.


## Ideia central

A coluna `GLUCOSE` mistura duas unidades: 44 valores entre 3,1 e 21,3 (mmol/L) e o restante entre 47 e 500 (mg/dL). A coluna `HEMOGLOBIN` também: a maioria entre 4,7 e 13,1 (HbA1c em %) e 43 valores entre 27 e 116 (HbA1c em mmol/mol, padrão IFCC). É um problema de **qualidade dos dados (Aula 2: inconsistência)**. Corrigido isso, os dois exames separam bem as classes, e modelos simples passam de 0,88.

## Pré-processamento (`limpeza.py`)

| Etapa | Regra | Aula |
|---|---|---|
| Duplicatas | Remove 20 linhas idênticas exceto `id` | 2 |
| Glicose | Valor < 35 → × 18,016 (mmol/L → mg/dL) | 2 |
| HbA1c | Valor > 20 → 0,09148 × v + 2,152 (IFCC → NGSP %) | 2 |
| Categóricos | Unifica grafias (`F`, `female`, `FEMALE`…) | 2 |
| Altura | Valor < 3 → × 100 (m → cm); cria IMC | 2 |
| Pressão | Separa `120/80` em sistólica e diastólica; `?` vira ausente | 2 |
| Ausentes | Mediana do **treino de cada parte** + indicador de ausência | 2 |

## Modelos (`modelo.py`)

| Modelo | Atributos | Configuração | Aula |
|---|---|---|---|
| KNN | glicose, HbA1c | K=11, mín-máx, Euclidiana, voto simples | 5 |
| Árvore | glicose, HbA1c | entropia (ganho de informação), profundidade 5, mín. 5 por folha | 5 |
| Rede neural | glicose, HbA1c, triglicerídeos, PA sistólica, IMC, idade, histórico familiar, atividade | 1 camada oculta com 8 neurônios sigmoide | 6 |
| Voto dos 3 | — | maioria simples | 5–6 |

## Resultados — validação cruzada 5 partes × 5 repetições, só no treino (Aula 7)

| Modelo | F1-macro | Acurácia | Precisão macro | Recall diabetes | Recall controle |
|---|---|---|---|---|---|
| KNN K=11 | 0,887 | 0,888 | 0,901 | 0,801 | 0,981 |
| Árvore | 0,883 | 0,883 | 0,893 | 0,810 | 0,962 |
| Rede neural | 0,882 | 0,882 | 0,885 | 0,856 | 0,911 |
| Voto dos 3 | 0,888 | 0,889 | 0,900 | 0,812 | 0,972 |

Grade testada antes da escolha: K ∈ {5, 7, 11, 15, 21}; profundidade ∈ {2, 3, 4, 5, livre} × folha ∈ {5, 10}; neurônios ∈ {4, 8, 16}; 4 conjuntos de atributos. Foi uma grade pequena, de propósito, para reduzir o risco de sobreajuste à validação.

O conjunto de teste não foi usado em nenhuma escolha.

## Como executar a v1 (registro)

```bash
cd Mod8_Unidades
python3 modelo.py ../dados/kaggle-training/train.csv ../dados/kaggle-test/test.csv
```

## Ponto fraco da v1

O recall de diabetes (≈0,80) é mais baixo que o de controle. Os erros se concentram em pacientes sem glicose e/ou HbA1c. A rede, que usa mais atributos clínicos, tem o melhor recall de diabetes.

Kaggle (placar público): KNN v1 = 0,85692; média dos 3 v1 = 0,86649.

---

# v2 — Um modelo por padrão de ausência (`modelo_padroes.py`)

## Diagnóstico

Na v1, um exame ausente virava a mediana, ou seja, um valor normal, e o paciente parecia saudável. Erros do KNN v1 na validação:

| Situação | Diabéticos | Perdidos |
|---|---|---|
| Com os dois exames | 184 | 21 (11%) |
| Só glicose | 57 | 20 (35%) |
| Nenhum exame | 7 | 7 (100%) |

## Solução (Aula 2: ignorar o atributo ausente em vez de inventar um valor)

Cada modelo (KNN, árvore, rede) é, na verdade, um conjunto de 4 submodelos, e o paciente vai para o submodelo do seu padrão de exames:

| Padrão do paciente | Atributos usados |
|---|---|
| Glicose e HbA1c | glicose, HbA1c (a rede usa também os clínicos) |
| Só glicose | glicose + clínicos |
| Só HbA1c | HbA1c + clínicos |
| Nenhum | só clínicos |

Clínicos: triglicerídeos, PA sistólica, IMC, idade, histórico familiar, atividade física. Cada submodelo é treinado com todos os pacientes do treino que têm aqueles exames.

## Limpeza adicional (`limpeza.py`)

| Regra | Motivo |
|---|---|
| Peso > 140 → ÷ 2,2046 | 23 valores em libras (IMC de até 84 caía para 25 a 35) |
| Triglicerídeos limitados a 1000 | Valores extremos (até 5.310) dominavam a escala |

Essas regras afetam só os atributos clínicos. A v1, quando rodada de novo, fica levemente diferente dos CSVs enviados.

## Configuração

KNN K=11 com padronização (média e desvio padrão); árvore com entropia, profundidade 4 e mínimo 5 por folha; rede com 8 neurônios sigmoide. A combinação é a média dos apoios com corte em 0,5.

## Resultados — validação cruzada 5×4, só treino, sementes não usadas na escolha

| Modelo | F1-macro | Acurácia | Recall diabetes | Recall controle |
|---|---|---|---|---|
| KNN K=11 | 0,896 | 0,896 | 0,854 | 0,942 |
| Árvore | 0,894 | 0,894 | 0,881 | 0,907 |
| Rede neural | 0,886 | 0,887 | 0,870 | 0,904 |
| Voto dos 3 | 0,912 | 0,912 | 0,885 | 0,942 |
| **Média dos 3** | **0,915** | **0,915** | **0,891** | **0,941** |
| Média dos 3 da v1 (mesmas partes) | 0,899 | — | — | — |

A escolha foi feita com outra semente (2026). As 18 combinações próximas testadas (K 11/15, profundidade 3/4/5, 3 variações de rede) ficaram todas entre 0,917 e 0,920 naquela semente. O ganho, portanto, vem da ideia, não de um ajuste fino.

```bash
python3 modelo_padroes.py ../dados/kaggle-training/train.csv ../dados/kaggle-test/test.csv
```

## Kaggle (placar público, cerca de 70% do teste)

| Arquivo | Versão | Score |
|---|---|---|
| submissao_knn11_unidades.csv | v1 KNN | 0,85692 |
| submissao_media3_unidades.csv | v1 média dos 3 | 0,86649 |
| submissao_voto3_padroes.csv (enviado como `submissao_voto3_exames_separados.csv`) | v2 voto dos 3 | **0,89900** |
| submissao_media3_padroes.csv | v2 média dos 3 | a enviar |

## Análise dos erros que restam (v2, voto dos 3, média de 4 rodadas)

| Situação | Pacientes | Erros |
|---|---|---|
| Diabéticos com os dois exames normais | 184 | 17,5 (39% dos erros) |
| Só glicose (as duas classes) | 104 | 15 |
| Nenhum exame | 18 | 5 |
| Controles com os dois exames | 173 | 4,5 |
| Só HbA1c | 41 | 3 |

O maior grupo de erros são diabéticos com glicose e HbA1c normais. Usar os atributos clínicos também nesse padrão piorou o resultado (voto 0,913 → 0,903). Provavelmente não há sinal adicional nesses pacientes.

## Teste com Random Forest (não adotado)

Random Forest no mesmo esquema por padrão: 300 árvores, entropia, sorteio de √atributos por nó, mínimo 5 por folha, clínicos também para o padrão completo. Foram testadas 12 configurações (atributos por nó √ ou todos × folha 1/3/5 × clínicos no padrão completo sim/não) com a semente 2026.

| Sorteio | RF sozinha | Média dos 3 | KNN + RF + rede | 4 modelos |
|---|---|---|---|---|
| 2026 (escolha) | 0,917 | 0,918 | 0,917 | 0,917 |
| 777 | 0,911 | 0,914 | 0,913 | 0,909 |
| 99 | 0,909 | 0,914 | 0,914 | 0,914 |

Ficou empatada ou pouco abaixo da média dos 3 e não está no material das aulas. Por isso não foi adotada. O CSV `submissao_rf_padroes.csv` fica como registro.

## Variações testadas só com conteúdo das aulas (07/11)

Validação 5×3, semente 2026. Base: voto dos 3 = 0,9147.

| Variação | Aula | Resultado |
|---|---|---|
| KNN Manhattan em vez de Euclidiana | 3 | 0,901 vs 0,902 sozinho. Sem ganho |
| KNN K=15 Manhattan | 3, 5 | 0,899. Sem ganho |
| KNN mín-máx em vez de média/desvio | 5, 10 | 0,885 vs 0,902. **Pior**, mantém média/desvio |
| Árvore com Gini em vez de entropia | 5 | 0,897 vs 0,894. Empate |
| Rede como no slide 17: SGD exemplo a exemplo, sem momentum e sem regularização | 6 | 0,874 vs 0,897 sozinha; no voto, 0,911 vs 0,915 |
| Retirar um atributo clínico por vez | 2 (seleção) | Retirar triglicerídeos, pressão, IMC ou idade piora (0,902 a 0,906). Sem histórico familiar: 0,919, mas nas sementes 777 e 99 deu −0,003 e +0,003, ou seja, ruído |
| Acrescentar PA diastólica, sexo, sódio ou fumante | 2 (seleção) | 0,907 a 0,914. Sem ganho |

Conclusão: dentro do conteúdo das aulas, o desempenho está estável. Nenhuma variação traz ganho consistente.

## Modelo final indicado

**Voto dos 3 por padrão de exames** (`modelo_padroes.py`): F1-macro 0,912 na validação e 0,899 no Kaggle. A média dos 3 é a segunda opção para as 2 submissões finais.

## Correção de 08/11: grafias da atividade física

A limpeza não reconhecia duas grafias da atividade física, `Moderat` e `Intensive`, que viravam ausentes e recebiam a mediana (atividade leve). Eram 3 pacientes no treino e 6 no teste. A regra passou a convertê-las em moderada (2) e intensa (3).

Efeito: os números da v2 acima já são os corrigidos (mudanças na terceira casa decimal). No teste, o voto dos 3 muda em 1 paciente e a média dos 3 em 1 paciente. Os CSVs `submissao_voto3_padroes.csv` e `submissao_media3_padroes.csv` desta pasta foram regenerados; o arquivo enviado ao Kaggle com 0,89900 é a versão anterior. Os CSVs da v1 (`*_unidades.csv`) e da Random Forest ficam como registro do que foi enviado ou testado antes da correção.

