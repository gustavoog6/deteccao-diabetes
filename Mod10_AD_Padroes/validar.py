"""Reproduz a validação cruzada do modelo desta pasta, usando só a base de treino (aula 7).

Uso:
    python3 validar.py              # 5 partes x 4 repetições, semente 777 (números do README)
    python3 validar.py --semente 2026

Mostra a média e o desvio das métricas nas 20 rodadas, a matriz de confusão média
por repetição e os erros por padrão de exames.
"""
import argparse
import os
import time
import warnings

import pandas as pd

from limpeza import carregar_treino
from modelo_final import NOME, criar_modelo
from padroes import erros_por_padrao, matriz_confusao, resumo, validar

warnings.filterwarnings('ignore')
pd.set_option('display.width', 120)
AQUI = os.path.dirname(os.path.abspath(__file__))
TREINO_PADRAO = os.path.join(AQUI, '..', 'dados', 'kaggle-training', 'train.csv')


def main():
    ap = argparse.ArgumentParser(description=f'Validação cruzada do {NOME}')
    ap.add_argument('--treino', default=TREINO_PADRAO)
    ap.add_argument('--semente', type=int, default=777)
    a = ap.parse_args()

    t0 = time.time()
    tr = carregar_treino(a.treino)
    y = tr['class'].values
    print(f'{NOME}\nValidação cruzada estratificada: 5 partes x 4 repetições = 20 rodadas, semente {a.semente}\n')
    tab, prev = validar(criar_modelo, tr, y, semente=a.semente)
    print(resumo(tab).to_string(), '\n')
    print('Matriz de confusão (média por repetição):')
    print(matriz_confusao(y, prev).to_string(), '\n')
    print('Erros por padrão de exames (média por repetição):')
    print(erros_por_padrao(tr, y, prev).to_string())
    print(f'\n({time.time() - t0:.1f} s)')


if __name__ == '__main__':
    main()
