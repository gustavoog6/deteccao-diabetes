"""Mod8 v2 — um modelo para cada padrão de exames ausentes + média dos 3 modelos.

Uso:  python3 modelo_padroes.py ../dados/kaggle-training/train.csv ../dados/kaggle-test/test.csv
Saída: submissao_media3_padroes.csv e submissao_voto3_padroes.csv nesta pasta.

Ideia (Aula 2 — valores ausentes: "ignorar" o atributo ausente em vez de inventar um valor):
  - paciente com glicose e HbA1c  -> modelo treinado só com os dois exames
  - paciente sem um dos exames     -> modelo com o exame que existe + atributos clínicos
  - paciente sem nenhum exame      -> modelo só com atributos clínicos
Cada submodelo é treinado com todos os pacientes do treino que têm aqueles exames.

Modelos (Aulas 5 e 6): KNN K=11, árvore com entropia, rede neural com 1 camada oculta sigmoide.
Combinação: média dos apoios (fração de vizinhos, proporção na folha, saída da sigmoide), corte 0,5.
Avaliação (Aula 7): validação cruzada estratificada 5 partes x 4 repetições, somente no treino.
"""
import sys, warnings
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, ClassifierMixin, clone
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score
from limpeza import carregar

warnings.filterwarnings('ignore')
EXAMES = ['GLICOSE', 'HBA1C']
CLINICOS = ['TRIGLIC', 'PA_SIST', 'IMC', 'IDADE', 'HIST_FAMILIA', 'ATIVIDADE']
PADROES = [(1, 1), (1, 0), (0, 1), (0, 0)]  # (tem glicose, tem HbA1c)


class PorPadrao(BaseEstimator, ClassifierMixin):
    def __init__(self, base, clinicos_quando_completo=False):
        self.base = base
        self.clinicos_quando_completo = clinicos_quando_completo

    def colunas(self, padrao):
        exames = [e for e, tem in zip(EXAMES, padrao) if tem]
        if all(padrao) and not self.clinicos_quando_completo:
            return exames
        return exames + CLINICOS

    def fit(self, X, y):
        self.classes_ = np.array([0, 1])
        self.modelos_ = {}
        for padrao in PADROES:
            linhas = np.ones(len(X), bool)
            for e, tem in zip(EXAMES, padrao):
                if tem:
                    linhas &= X[e].notna().values
            cols = self.colunas(padrao)
            # clínicos ausentes: mediana do treino (são poucos)
            modelo = make_pipeline(SimpleImputer(strategy='median'), clone(self.base))
            self.modelos_[padrao] = (cols, modelo.fit(X.loc[linhas, cols].values, y[linhas]))
        return self

    def predict_proba(self, X):
        P = np.zeros((len(X), 2))
        padroes = list(zip(X['GLICOSE'].notna().astype(int), X['HBA1C'].notna().astype(int)))
        for padrao in set(padroes):
            idx = np.array([p == padrao for p in padroes])
            cols, modelo = self.modelos_[padrao]
            P[idx] = modelo.predict_proba(X.loc[idx, cols].values)
        return P

    def predict(self, X):
        return (self.predict_proba(X)[:, 1] >= 0.5).astype(int)


def criar_modelos():
    knn = PorPadrao(make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=11)))
    arvore = PorPadrao(DecisionTreeClassifier(criterion='entropy', max_depth=4, min_samples_leaf=5, random_state=0))
    rede = PorPadrao(make_pipeline(StandardScaler(),
                                   MLPClassifier((8,), activation='logistic', alpha=1e-3, max_iter=3000, random_state=0)),
                     clinicos_quando_completo=True)
    return {'KNN K=11': knn, 'Árvore': arvore, 'Rede neural': rede}


def metricas(y, p):
    return {'f1_macro': f1_score(y, p, average='macro'), 'acuracia': accuracy_score(y, p),
            'precisao_macro': precision_score(y, p, average='macro'),
            'recall_diabetes': recall_score(y, p, pos_label=1), 'recall_controle': recall_score(y, p, pos_label=0)}


if __name__ == '__main__':
    treino, teste = (sys.argv[1], sys.argv[2]) if len(sys.argv) > 2 else ('train.csv', 'test.csv')
    tr, te = carregar(treino, teste)
    y = tr['class'].values

    cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=4, random_state=777)
    res = {}
    for a, b in cv.split(tr, y):
        apoios = {n: m.fit(tr.iloc[a], y[a]).predict_proba(tr.iloc[b])[:, 1] for n, m in criar_modelos().items()}
        prev = {n: (p >= 0.5).astype(int) for n, p in apoios.items()}
        prev['Voto dos 3'] = (sum(prev.values()) >= 2).astype(int)
        prev['Média dos 3'] = (sum(apoios.values()) / 3 >= 0.5).astype(int)
        for n, p in prev.items():
            res.setdefault(n, []).append(metricas(y[b], p))
    print('Validação cruzada 5 partes x 4 repetições (somente treino):')
    for n, lst in res.items():
        df = pd.DataFrame(lst)
        print(f'  {n:12s} ' + '  '.join(f'{c}={df[c].mean():.3f}' for c in df.columns) + f'  (dp f1 {df.f1_macro.std():.3f})')

    apoios = {n: m.fit(tr, y).predict_proba(te)[:, 1] for n, m in criar_modelos().items()}
    media = (sum(apoios.values()) / 3 >= 0.5).astype(int)
    voto = (sum((p >= 0.5).astype(int) for p in apoios.values()) >= 2).astype(int)
    pd.DataFrame({'id': te['id'], 'class': media}).to_csv('submissao_media3_padroes.csv', index=False)
    pd.DataFrame({'id': te['id'], 'class': voto}).to_csv('submissao_voto3_padroes.csv', index=False)
    print('gerados submissao_media3_padroes.csv e submissao_voto3_padroes.csv')
