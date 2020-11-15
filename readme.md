# Base de données  

Dans ce projet, nous utilisons une base de données sqlite 'data.db'. 
Rappelons ci-dessous le code Python servant à extraire les tables avec Pandas.

```python
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('sqlite:///data.db', echo=False)
con = engine.connect()
df_patient = pd.read_sql('select * from patient', con=con)
df_pcr = pd.read_sql('select * from test', con=con)
con.close()
```

# Référentiel pour les codes postaux en Australie

Ce document (en format csv) est téléchargeable sur le site https://data.gov.au/. 
- Lien direct : https://data.gov.au/dataset/ds-brisbane-85e262dc-9dfe-46e9-87a8-f9f92f6a7780/distribution/dist-brisbane-f84ed0a2-b3f0-4cc8-bd28-8987e67039ec/details?q=


# Notebooks 

- Le notebook 'Qualite_donnees_NB.ipynb' est consacré à l'étude de la qualité de données 
contenues dans la table "patient" (df_patient). Dans ce fichier, on met évidence les anomalies de notre jeu de  
données comme :
* les duplications dans l'ID des patients (patient_id), 
* l'age dont les valeurs qui sont stockées comme des constantes. 
* la non correspondance entre les code postal et la région. 
D'autres anomalies sont mentionnées dans ce fichier via des exemples concrets. 
C'est notre point de départ pour réaliser la tâche de nettoyage de données.

- Le notebook 'data_analytics_NB.ipynb' contient les représentations graphiques relatives aux résultats 
des tests PCR réalisés sur une population de 8800 personnes dans les différentes régions. 
Le jeu de données utilisé ici est le résultat de l'application de la fonction 'get_final_ds' qui prend en paramètre :
df_patient et df_pcr et le chemin du fichier csv "référentiel" des codes postaux de l'Australie. 


# Modules Python 

- Le module 'getting_started.py' contient le code Python mentionné plus haut dans la partie Base de données.

- Le module 'detect_duplicates_script.py' contient une fonction Python à deux paramètres (df_patient et le "Path" du référentiel), 
permatant de : 
* supprimer les duplications selon l'ID patient (colonne 'patient_id');
* corriger l'accordance entre le code postal et la 'state' (selon le référentiel),
* calculer dynamiquement l'age d'un patient à partir de sa date de naissance.

- Le module 'get_final_dataset.py' contient la fonction Python "get_final_ds" dont les paramètres : df_patient, df_pcr et le "Path" du référentiel. Elle a comme "output" le (dataframe final) le jeu de données final résultant de l'ensemble du procédé de data cleaning 
adopté dans ce projet. 

# Librairies :

Ci-dessous les librairies importée dans les différents modules et notebooks:
Pour l'installation de ces librairies on utilise PyPI.

- Pandas & Numpy: pour la manipulation de données.

```python
pip install pandas
``` 

```python
pip install numpy
```

- Datetime: pour manipulation des dates. 

```python
pip install DateTime
```

- Matplotlib & Seaborn: pour la visualisation de données.

```python
pip install matplotlib
```
 
```python
pip install seaborn
```

- Ainsi, pour pouvoir lancer les tests unitaires, nous utliserons 
la librarie Pytest. 

```python
pip install -U pytest
```
