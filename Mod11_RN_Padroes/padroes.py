"""Funções comuns aos modelos 8, 9, 10 e 11 (o arquivo é igual nas quatro pastas).

PorPadrao: um submodelo para cada padrão de exames disponíveis (Aula 2 — valores ausentes).
Combinacao: voto da maioria ou média dos apoios (Modelo 8).
validar:   validação cruzada estratificada repetida, só no treino (Aula 7).
"""
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, ClassifierMixin, clone
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.metrics import (f1_score, accuracy_score, precision_score,
                             recall_score, confusion_matrix)

EXAMES = ['GLICOSE', 'HBA1C']
CLINICOS = ['TRIGLIC', 'PA_SIST', 'IMC', 'IDADE', 'HIST_FAMILIA', 'ATIVIDADE']
PADROES = [(1, 1), (1, 0), (0, 1), (0, 0)]  # (tem glicose, tem HbA1c)
NOME_PADRAO = {(1, 1): 'glicose e HbA1c', (1, 0): 'só glicose', (0, 1): 'só HbA1c', (0, 0): 'nenhum exame'}


def padrao_de(X):
    """Lista com o padrão (tem glicose, tem HbA1c) de cada paciente."""
    return list(zip(X['GLICOSE'].notna().astype(int), X['HBA1C'].notna().astype(int)))


class PorPadrao(BaseEstimator, ClassifierMixin):
    """Treina 4 submodelos, um por padrão de exames.

    - glicose e HbA1c -> só os dois exames (ou exames + clínicos, se clinicos_quando_completo=True)
    - só um exame     -> esse exame + atributos clínicos
    - nenhum exame    -> só atributos clínicos
    Cada submodelo usa todos os pacientes do treino que têm os exames que ele precisa.
    Atributos clínicos ausentes (poucos) recebem a mediana do treino.
    """

    def __init__(self, base, clinicos_quando_completo=False):
        self.base = base
        self.clinicos_quando_completo = clinicos_quando_completo

    def colunas(self, padrao):
        exames = [e for e, tem in zip(EXAMES, padrao) if tem]
        if all(padrao) and not self.clinicos_quando_completo:
            return exames
        return exames + CLINICOS

    def fit(self, X, y):
        y = np.asarray(y)
        self.classes_ = np.array([0, 1])
        self.modelos_ = {}
        for padrao in PADROES:
            linhas = np.ones(len(X), bool)
            for e, tem in zip(EXAMES, padrao):
                if tem:
                    linhas &= X[e].notna().values
            cols = self.colunas(padrao)
            modelo = make_pipeline(SimpleImputer(strategy='median'), clone(self.base))
            self.modelos_[padrao] = (cols, modelo.fit(X.loc[linhas, cols].values, y[linhas]))
        return self

    def predict_proba(self, X):
        P = np.zeros((len(X), 2))
        pads = padrao_de(X)
        for padrao in set(pads):
            idx = np.array([p == padrao for p in pads])
            cols, modelo = self.modelos_[padrao]
            P[idx] = modelo.predict_proba(X.loc[idx, cols].values)
        return P

    def predict(self, X):
        return (self.predict_proba(X)[:, 1] >= 0.5).astype(int)


class Combinacao(BaseEstimator, ClassifierMixin):
    """Junta vários modelos (usado no Modelo 8).

    regra='voto':  diabetes quando a maioria dos modelos diz diabetes (apoio >= 0,5).
    regra='media': diabetes quando a média dos apoios é >= 0,5.
    """

    def __init__(self, modelos, regra='voto'):
        self.modelos = modelos
        self.regra = regra

    def fit(self, X, y):
        self.classes_ = np.array([0, 1])
        self.modelos_ = [clone(m).fit(X, y) for m in self.modelos]
        return self

    def apoios(self, X):
        return np.array([m.predict_proba(X)[:, 1] for m in self.modelos_])

    def predict_proba(self, X):
        p = self.apoios(X).mean(0)
        return np.column_stack([1 - p, p])

    def predict(self, X):
        A = self.apoios(X)
        if self.regra == 'voto':
            return ((A >= 0.5).sum(0) * 2 > len(A)).astype(int)
        return (A.mean(0) >= 0.5).astype(int)


def metricas(y, p):
    return {'f1_macro': f1_score(y, p, average='macro'),
            'acuracia': accuracy_score(y, p),
            'precisao_macro': precision_score(y, p, average='macro', zero_division=0),
            'recall_diabetes': recall_score(y, p, pos_label=1),
            'recall_controle': recall_score(y, p, pos_label=0)}


def validar(criar_modelo, X, y, semente, partes=5, repeticoes=4):
    """Validação cruzada estratificada repetida (Aula 7).

    Retorna (tabela com as métricas de cada parte, previsões fora da parte com forma [repetições, n]).
    """
    y = np.asarray(y)
    cv = RepeatedStratifiedKFold(n_splits=partes, n_repeats=repeticoes, random_state=semente)
    linhas, prev = [], np.zeros((repeticoes, len(y)), int)
    for i, (a, b) in enumerate(cv.split(X, y)):
        m = criar_modelo().fit(X.iloc[a], y[a])
        p = m.predict(X.iloc[b])
        prev[i // partes, b] = p
        linhas.append(metricas(y[b], p))
    return pd.DataFrame(linhas), prev


def resumo(tab):
    return pd.DataFrame({'média': tab.mean(), 'desvio padrão': tab.std()}).round(3)


def matriz_confusao(y, prev):
    """Matriz de confusão média por repetição (cada repetição prevê cada paciente uma vez)."""
    m = sum(confusion_matrix(y, p, labels=[0, 1]) for p in prev) / len(prev)
    return pd.DataFrame(m.round(1), index=['real controle (0)', 'real diabetes (1)'],
                        columns=['previsto controle (0)', 'previsto diabetes (1)'])


def erros_por_padrao(X, y, prev):
    y = np.asarray(y)
    erro = (prev != y).mean(0)
    df = pd.DataFrame({'padrão': [NOME_PADRAO[p] for p in padrao_de(X)],
                       'classe': np.where(y == 1, 'diabetes', 'controle'), 'erro': erro})
    return (df.groupby(['padrão', 'classe'])
              .agg(pacientes=('erro', 'size'), erros_medios=('erro', 'sum'), taxa_erro=('erro', 'mean'))
              .round(2))
