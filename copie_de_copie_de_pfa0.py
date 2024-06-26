# -*- coding: utf-8 -*-
"""Copie de Copie de pfa0.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1kyrPLpUIDJsCkKz5fgD37HdQomCs84zE

**cleaning data**
"""

import pandas as pd
import numpy as np

# Spécifiez l'encodage latin-1 lors de la lecture du fichier CSV
dat = pd.read_csv("/content/crimedata.csv", encoding="latin-1")
data=dat

data.head()

data.describe()

data.info()

data.shape

data.isnull().sum()

data.columns

df=data

data.replace("?",np.nan,inplace=True)
data.isna().sum()
t=dict(data.isna().sum())
k = []
for value, key in zip(t.values(), t.keys()):
    if value > 5:
        k.append(key)

data.drop(columns=k,axis=1,inplace=True)
data.dropna(axis=0,inplace=True)
data.shape

#la suppression les lignes catégorials
df.drop(["Êcommunityname","state"],axis=1,inplace=True)

df.tail()

data.columns[-1]

df.reset_index()

df.shape

#essaye du modèle complet avant la repartition de la data
Y=data[data.columns[-1]]
X=data.iloc[:,0:-1]

X.shape

"""le modele complet

"""

from mlxtend.feature_selection import SequentialFeatureSelector as SFS
from sklearn.linear_model import LinearRegression
model=LinearRegression()
model=model.fit(X,Y)
r2 = model.score(X, Y)
n = len(Y)
p = X.shape[1]
adjusted_r2 = 1 - (1 - r2) * (n - 1) / (n - p - 1)
print(adjusted_r2 )

X

print(adjusted_r2)

data.shape

"""**DEVISION DU DATA(90%:train , 10% test)**"""

X_train=data.iloc[0:1985,0:-1 ]

Y_train = data.iloc[0:1985, -1]

X_train.shape

#modèle complet avec la partie de train
from mlxtend.feature_selection import SequentialFeatureSelector as SFS
from sklearn.linear_model import LinearRegression
model=LinearRegression()
model=model.fit(X_train,Y_train)
r2 = model.score(X_train, Y_train)
n = len(Y_train)
p = X_train.shape[1]
adjusted_r2 = 1 - (1 - r2) * (n - 1) / (n - p - 1)
print(adjusted_r2)

"""**utilisation du 10% pour la prediction**"""

X_test=data.iloc[1985:2215,0:-1 ]
Y_test = data.iloc[1985:2215, -1]
Y_pred_test = model.predict(X_test)

Y_pred_test

"""**calcule du mse et mae pour la prediction avce le modèle complet**"""

from sklearn.metrics import mean_squared_error, mean_absolute_error

# Calcul des différentes métriques
mse = mean_squared_error(Y_test, Y_pred_test, squared=False)
mae = mean_absolute_error(Y_test, Y_pred_test)
print("MSE :", mse)
print("mae :", mae)

data.shape

object_columns = data.select_dtypes(include=['object'])

# Remplacer les caractères indésirables dans toutes les colonnes de type objet
object_columns = object_columns.apply(lambda x: x.str.replace("'", "").astype(float))

# Afficher les premières lignes après le remplacement
print(object_columns.dtypes)
data[object_columns.columns]=object_columns

data.shape
data.dtypes

data.shape

data.dtypes

"""**utilisation du backward**"""

from sklearn.metrics import r2_score
import numpy as np

def adjusted_r2_scorer(estimator, X, y):
    r2 = estimator.score(X, y)
    n = X.shape[0]
    p = X.shape[1]
    adjusted_r2 = 1 - (1 - r2) * (n - 1) / (n - p - 1)
    return adjusted_r2

# Utiliser la fonction de score dans SequentialFeatureSelector
sfs = SFS(model,
          k_features="best",
          forward=False,
          scoring=adjusted_r2_scorer,  # Utiliser la fonction de score ajusté R²
          verbose=2,
          cv=0)
sfs.fit(X_train, Y_train)

R1=pd.DataFrame.from_dict(sfs.get_metric_dict()).T
R1

#extraction de la valeur maximale donnée par le backward
max_Rajustée=R1['cv_scores'].max()
print(max_Rajustée)

"""sfs.get_metric_dict() un dictionnaire sur les performances du modele

"""

#pour clarifier
R2=pd.Series(sfs.get_metric_dict())

R2=pd.DataFrame(R2).T
R2

#les indices des features selectionés par le backward
indices_selectionnes = sfs.k_feature_idx_
indices_selectionnes

#convertion des indices en des noms des colonnes
indices_selectionnes = sfs.k_feature_idx_

noms_caracteristiques_selectionnees = [data.columns[i] for i in indices_selectionnes]


print("Noms des caractéristiques sélectionnées :", noms_caracteristiques_selectionnees)

"""**l'entrainement et la prediction en utilisant les variables selectionnés par le backward**"""

X_test_F=X_test[noms_caracteristiques_selectionnees]
model=LinearRegression()
model=model.fit(X_train[noms_caracteristiques_selectionnees],Y_train)
Y_pred_test= model.predict(X_test_F)

from sklearn.metrics import mean_squared_error, mean_absolute_error

# Calcul des différentes métriques
mse = mean_squared_error(Y_test, Y_pred_test, squared=False)
mae = mean_absolute_error(Y_test, Y_pred_test)
print("MSE :", mse)
print("mae :", mae)

"""**l'algorithme génétique**"""

pip install geneticalgorithm

import pandas as pd
import numpy as np
from geneticalgorithm import geneticalgorithm as ga
import statsmodels.api as sm

clmns=X_train.columns

from mlxtend.feature_selection import SequentialFeatureSelector as SFS
from sklearn.linear_model import LinearRegression
def evaluate (features):
    # Sélection des caractéristiques
    selected_features_indice = np.where(features == 1)[0]

    selected_feature_variable = clmns[selected_features_indice]
    model=LinearRegression()
    model=model.fit(X_train[selected_feature_variable],Y_train)
    r2 = model.score(X_train[selected_feature_variable],Y_train)
    n = len(Y_train)
    p = X_train[selected_feature_variable].shape[1]
    adjusted_r2 = 1 - (1 - r2) * (n - 1) / (n - p - 1)
    adjusted_r_squared=adjusted_r2

    return (-1*adjusted_r_squared)

#Définition des limites pour les coefficients
varbound = np.ones(X_train.shape[1])

algorithm_param_R2 = {'max_num_iteration': 500, 'population_size': 400, 'mutation_probability': 0.2,
                      'crossover_probability': 0.5, 'crossover_type': 'uniform', 'max_iteration_without_improv': 200, 'parents_portion': 0.4,'elit_ratio': 0.3}

model_R2 = ga(function=evaluate, dimension=X_train.shape[1], variable_type='bool', variable_boundaries=varbound, algorithm_parameters=algorithm_param_R2)

# Exécution de l'algorithme génétique
model_R2.run()

# Extractionx des caractéristiques sélectionnées du meilleur individu
selected_features_indices_R2 = np.where(model_R2.output_dict['variable'] == 1)[0]

# Récupérer les noms des caractéristiques sélectionnées
selected_feature_names_R2 = clmns[selected_features_indices_R2]

print("nombre de varaible", len(selected_feature_names_R2))
print("Caractéristiques sélectionnées : ", selected_feature_names_R2)

print('R2_ajustée : ',(-1*model_R2.output_dict['function']))

"""la prédiction


"""

X_test_F=X_test[selected_feature_names_R2]

X_test_F.shape[1]

X_test_F=X_test[selected_feature_names_R2]
model=LinearRegression()
model=model.fit(X_train[selected_feature_names_R2],Y_train)
Y_pred_test= model.predict(X_test_F)

from sklearn.metrics import mean_squared_error, mean_absolute_error
X_test_F=X_test[selected_feature_names_R2]
y_pred_test= model.predict(X_test_F)
# Calcul des différentes métriques
mse = mean_squared_error(Y_test, Y_pred_test, squared=False)
mae = mean_absolute_error(Y_test, Y_pred_test)
print("MSE :", mse)
print("mae :", mae)

