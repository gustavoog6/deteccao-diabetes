"""Definição do Modelo 10: árvore de decisão com um submodelo por padrão de exames (aulas 2 e 5)."""
from sklearn.tree import DecisionTreeClassifier

from padroes import PorPadrao

NOME = 'Modelo 10 - Árvore de decisão (entropia, profundidade 4, folha 5) por padrão de exames'


def criar_modelo():
    # sem padronização: cada corte olha um atributo só
    return PorPadrao(DecisionTreeClassifier(criterion='entropy', max_depth=4, min_samples_leaf=5, random_state=0))
