"""Definição do Modelo 9: KNN com um submodelo por padrão de exames (aulas 2, 3, 5 e 10)."""
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from padroes import PorPadrao

NOME = 'Modelo 9 - KNN (K=11) por padrão de exames'


def criar_modelo():
    # padronização (valor - média) / desvio do treino + distância Euclidiana + 11 vizinhos
    return PorPadrao(make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=11)))
