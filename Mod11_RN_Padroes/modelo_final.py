"""Definição do Modelo 11: rede neural com um submodelo por padrão de exames (aulas 2, 6 e 10)."""
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from padroes import PorPadrao

NOME = 'Modelo 11 - Rede neural (8 neurônios sigmoide) por padrão de exames'


def criar_modelo():
    # usa os 6 dados clínicos também quando o paciente tem os dois exames
    rede = MLPClassifier((8,), activation='logistic', alpha=1e-3, max_iter=3000, random_state=0)
    return PorPadrao(make_pipeline(StandardScaler(), rede), clinicos_quando_completo=True)
