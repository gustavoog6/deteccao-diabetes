"""Treina o modelo desta pasta com a base de treino e classifica qualquer CSV no formato do Kaggle.

Uso:
    python3 prever.py ARQUIVO.csv
    python3 prever.py ARQUIVO.csv --saida previsoes.csv

O tratamento da base (limpeza.py) é aplicado ao treino e ao ARQUIVO antes de classificar.
Se o ARQUIVO tiver a coluna `class` (0 = controle, 1 = diabetes), o script mostra
precisão, recall de cada classe, F1-macro, acurácia e a matriz de confusão.
"""
import argparse
import os
import sys
import time
import warnings

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score

from limpeza import carregar_entrada, carregar_treino
from modelo_final import NOME, criar_modelo

warnings.filterwarnings('ignore')
AQUI = os.path.dirname(os.path.abspath(__file__))
TREINO_PADRAO = os.path.join(AQUI, '..', 'dados', 'kaggle-training', 'train.csv')


def relatorio(y, p):
    vn, fp, fn, vp = confusion_matrix(y, p, labels=[0, 1]).ravel()
    print('\nMétricas (o arquivo tem a coluna class):')
    print(f'  F1-macro          {f1_score(y, p, average="macro"):.4f}')
    print(f'  Acurácia          {accuracy_score(y, p):.4f}')
    print(f'  Precisão diabetes {precision_score(y, p, pos_label=1, zero_division=0):.4f}')
    print(f'  Precisão controle {precision_score(y, p, pos_label=0, zero_division=0):.4f}')
    print(f'  Recall diabetes   {recall_score(y, p, pos_label=1, zero_division=0):.4f}')
    print(f'  Recall controle   {recall_score(y, p, pos_label=0, zero_division=0):.4f}')
    print('\nMatriz de confusão (linhas = real, colunas = previsto):')
    print('                  prev. controle  prev. diabetes')
    print(f'  real controle   {vn:14d}  {fp:14d}   (VN, FP)')
    print(f'  real diabetes   {fn:14d}  {vp:14d}   (FN, VP)')


def main():
    ap = argparse.ArgumentParser(description=f'{NOME}: classifica pacientes em controle (0) ou diabetes (1).')
    ap.add_argument('entrada', help='CSV a classificar (mesmo formato do test.csv do Kaggle)')
    ap.add_argument('--saida', default='previsoes.csv', help='CSV de saída com id,class (padrão: previsoes.csv)')
    ap.add_argument('--treino', default=TREINO_PADRAO, help='CSV de treino (padrão: ../dados/kaggle-training/train.csv)')
    a = ap.parse_args()
    for caminho in (a.entrada, a.treino):
        if not os.path.exists(caminho):
            sys.exit(f'Arquivo não encontrado: {caminho}')

    t0 = time.time()
    tr = carregar_treino(a.treino)      # limpeza + remoção de duplicados
    X = carregar_entrada(a.entrada)     # mesma limpeza, paciente a paciente
    print(f'{NOME}')
    print(f'Treino: {len(tr)} pacientes (sem duplicados) | Entrada: {len(X)} pacientes')
    p = criar_modelo().fit(tr, tr['class'].values).predict(X)
    pd.DataFrame({'id': X['id'], 'class': p}).to_csv(a.saida, index=False)
    print(f'Previsões: {int((p == 1).sum())} diabetes, {int((p == 0).sum())} controle -> {a.saida} '
          f'({time.time() - t0:.1f} s)')
    if 'class' in X:
        relatorio(X['class'].values, p)


if __name__ == '__main__':
    main()
