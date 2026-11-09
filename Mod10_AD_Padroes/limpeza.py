"""Limpeza da base (Aula 2: qualidade dos dados e pré-processamento).
Todas as regras são de formato/unidade, aplicadas linha a linha;
nenhuma estatística é calculada aqui (as estatísticas ficam para o treino de cada fold).
"""
import re
import numpy as np
import pandas as pd


def num(x):
    try:
        return float(str(x).strip().replace(',', '.'))
    except Exception:
        return np.nan


def ano_exame(s):
    s = str(s).strip()
    m = re.search(r'(19|20)\d{2}', s)
    return float(m.group(0)) if m else np.nan


def pressao(s):
    m = re.match(r'\s*(\d+)\s*/\s*(\d+)', str(s))
    if not m:
        return np.nan, np.nan
    return float(m.group(1)), float(m.group(2))


def mapa(s, regras):
    if pd.isna(s):
        return np.nan
    t = str(s).strip().lower()
    for chave, vals in regras.items():
        if t in vals:
            return chave
    return np.nan


def limpar(df):
    df = df.copy()
    # coluna que não vier no arquivo vira ausente (o modelo trata ausentes)
    for c in ['GENDER', 'FAMILY_HISTORY', 'PHYSICAL_ACTIVITY', 'SMOKER', 'AGE', 'EXAM_DATE', 'BIRTH_YEAR', 'HEIGHT',
              'WEIGHT', 'BLOOD_PRESSURE', 'GLUCOSE', 'HEMOGLOBIN', 'TRIGLYCERIDES', 'SODIUM']:
        if c not in df:
            df[c] = np.nan
    ids = df['id'] if 'id' in df else pd.Series(range(len(df)), index=df.index)
    out = pd.DataFrame({'id': ids.values}, index=df.index)
    # --- categóricos com grafias inconsistentes (Aula 2: inconsistência) ---
    out['SEXO_F'] = df['GENDER'].map(lambda s: mapa(s, {1: {'f', 'female', 'feminino'}, 0: {'m', 'male', 'masculino'}}))
    out['HIST_FAMILIA'] = df['FAMILY_HISTORY'].map(lambda s: mapa(s, {1: {'yes', 'y', '1', 'sim', 's'}, 0: {'no', 'n', '0', 'não', 'nao'}}))
    act = df['PHYSICAL_ACTIVITY'].map(lambda s: str(s).strip().lower() if pd.notna(s) else np.nan)
    act_map = {'sedentary': 0, 'sedentry': 0, 'light': 1, 'ligth': 1, 'moderate': 2, 'moderat': 2, 'intense': 3, 'intensive': 3}
    out['ATIVIDADE'] = act.map(lambda s: act_map.get(s, np.nan) if pd.notna(s) else np.nan)
    out['FUMANTE'] = df['SMOKER'].map(lambda s: mapa(s, {0: {'never', 'no'}, 1: {'former', 'ex-smoker'}, 2: {'current', 'yes'}}))

    # --- idade: corrigir pela data do exame e ano de nascimento quando faltar ---
    idade = df['AGE'].map(num)
    idade2 = df['EXAM_DATE'].map(ano_exame) - df['BIRTH_YEAR'].map(num)
    out['IDADE'] = idade.where(idade.between(1, 110), idade2)

    # --- altura em m -> cm ; IMC ---
    h = df['HEIGHT'].map(num)
    h = np.where(h < 3, h * 100, h)
    out['ALTURA'] = h
    p = df['WEIGHT'].map(num)
    out['PESO'] = np.where(p > 140, p / 2.2046, p)              # libras -> kg (valores > 140 viram 64-110 kg)
    out['IMC'] = out['PESO'] / (out['ALTURA'] / 100) ** 2

    pa = df['BLOOD_PRESSURE'].map(pressao)
    out['PA_SIST'] = [p[0] for p in pa]
    out['PA_DIAST'] = [p[1] for p in pa]

    # --- exames: unificar unidades ---
    g = df['GLUCOSE'].map(num)
    out['GLICOSE'] = np.where(g < 35, g * 18.016, g)          # mmol/L -> mg/dL
    hb = df['HEMOGLOBIN'].map(num)
    out['HBA1C'] = np.where(hb > 20, 0.09148 * hb + 2.152, hb)  # mmol/mol (IFCC) -> % (NGSP)
    out['TRIGLIC'] = df['TRIGLYCERIDES'].map(num).clip(upper=1000)  # valores extremos limitados a 1000
    out['SODIO'] = df['SODIUM'].map(num)
    if 'class' in df and df['class'].notna().all():
        out['class'] = df['class'].astype(float).astype(int)
    return out


def carregar(caminho_treino, caminho_teste):
    tr = pd.read_csv(caminho_treino, dtype=str)
    te = pd.read_csv(caminho_teste, dtype=str)
    # registros duplicados do mesmo paciente (Aula 2: dados duplicados)
    tr = tr.drop_duplicates(subset=[c for c in tr.columns if c != 'id'])
    return limpar(tr), limpar(te)


def carregar_treino(caminho_treino):
    tr = pd.read_csv(caminho_treino, dtype=str)
    tr = tr.drop_duplicates(subset=[c for c in tr.columns if c != 'id'])
    return limpar(tr).reset_index(drop=True)


def carregar_entrada(caminho):
    return limpar(pd.read_csv(caminho, dtype=str)).reset_index(drop=True)
