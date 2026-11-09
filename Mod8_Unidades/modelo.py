"""Mod8 — KNN, árvore e rede neural após correção de unidades.

Uso:  python3 modelo.py ../dados/kaggle-training/train.csv ../dados/kaggle-test/test.csv
Saída: submissao_knn11_unidades.csv e submissao_voto3_unidades.csv nesta pasta.

Referências de aula:
- Aula 2: qualidade dos dados (duplicatas, inconsistências, valores ausentes) e pré-processamento
- Aula 5: KNN (normalização mín-máx, distância Euclidiana, voto simples) e árvore (ganho de informação/entropia)
- Aula 6: rede neural com uma camada oculta e ativação sigmoide
- Aula 7: validação cruzada em K partes; precisão, recall e F1
"""
import sys, warnings
import numpy as np
import pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler, StandardScaler, FunctionTransformer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.model_selection import RepeatedStratifiedKFold, cross_validate
from limpeza import carregar

warnings.filterwarnings('ignore')
treino, teste = (sys.argv[1], sys.argv[2]) if len(sys.argv) > 2 else ('train.csv', 'test.csv')
tr, te = carregar(treino, teste)
y = tr['class'].values

EXAMES = ['GLICOSE', 'HBA1C']
CLINICOS = EXAMES + ['TRIGLIC', 'PA_SIST', 'IMC', 'IDADE', 'HIST_FAMILIA', 'ATIVIDADE']


def colunas(cols):
    return FunctionTransformer(lambda X: X[cols].values)


def imputar():
    # mediana calculada só no treino de cada parte + indicador de ausência (Aula 2: estimar valores ausentes)
    return SimpleImputer(strategy='median', add_indicator=True)


knn = make_pipeline(colunas(EXAMES), imputar(), MinMaxScaler(), KNeighborsClassifier(n_neighbors=11))
arvore = make_pipeline(colunas(EXAMES), imputar(),
                       DecisionTreeClassifier(criterion='entropy', max_depth=5, min_samples_leaf=5, random_state=0))
rede = make_pipeline(colunas(CLINICOS), imputar(), StandardScaler(),
                     MLPClassifier(hidden_layer_sizes=(8,), activation='logistic', alpha=1e-3,
                                   max_iter=3000, random_state=0))
voto3 = VotingClassifier([('knn', knn), ('arvore', arvore), ('rede', rede)], voting='hard')

cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=5, random_state=42)
from sklearn.metrics import make_scorer, recall_score
metricas = {'f1_macro': 'f1_macro', 'acuracia': 'accuracy', 'precisao_macro': 'precision_macro',
            'recall_diabetes': 'recall',
            'recall_controle': make_scorer(recall_score, pos_label=0)}

print('Validação cruzada 5 partes x 5 repetições (somente treino):')
for nome, modelo in [('KNN K=11', knn), ('Árvore', arvore), ('Rede neural', rede), ('Voto dos 3', voto3)]:
    r = cross_validate(modelo, tr, y, cv=cv, scoring=metricas)
    print(f'  {nome:12s} ' + '  '.join(f'{k}={r["test_" + k].mean():.3f}' for k in metricas))

for nome, modelo in [('knn11_unidades', knn), ('voto3_unidades', voto3)]:
    modelo.fit(tr, y)
    pd.DataFrame({'id': te['id'], 'class': modelo.predict(te)}).to_csv(f'submissao_{nome}.csv', index=False)
    print('gerado', f'submissao_{nome}.csv')
