"""Definição do Modelo 8 (modelo final): voto da maioria entre KNN, árvore e rede neural,
cada um com um submodelo por padrão de exames (aulas 2, 3, 5, 6 e 10)."""
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

from padroes import Combinacao, PorPadrao

NOME = 'Modelo 8 - Voto dos 3 (KNN, árvore e rede neural) por padrão de exames'
REGRA = 'voto'  # 'voto' (modelo final) ou 'media' (média dos apoios)


def criar_modelo(regra=REGRA):
    knn = PorPadrao(make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=11)))
    arvore = PorPadrao(DecisionTreeClassifier(criterion='entropy', max_depth=4, min_samples_leaf=5, random_state=0))
    rede = PorPadrao(make_pipeline(StandardScaler(), MLPClassifier((8,), activation='logistic', alpha=1e-3,
                                                                    max_iter=3000, random_state=0)),
                     clinicos_quando_completo=True)
    return Combinacao([knn, arvore, rede], regra=regra)
