import pandas as pd
import numpy as np
import datetime

# fonction permettant de supprimer les lignes avec des duplications sur 'patient_id'
# tout en gardant un représentant de telles lignes. 
# La logique conciste à garder celle qui contient le moins d'anomalies selon les champs: 
# date_of_birth et postcode
def delete_patientID_duplicates(data):
    # On commence par trier les lignes afin d'afficher d'éventuelles valeurs nulles en premier
    df_sorted = data.sort_values(by=['patient_id', 'date_of_birth', 'postcode'], na_position='first')
    # suppression des doublons selon le champ 'patient_id'
    df_dedup_patient_ID = df_sorted.drop_duplicates(subset=['patient_id'], keep='last')
    # suppression des valeurs manquantes au niveau du champ patient_id
    df_dedup_patient_ID = df_dedup_patient_ID[df_dedup_patient_ID['patient_id'].notnull()]
    return df_dedup_patient_ID

# Fonction pour calculer l'age à partir de la date de naissance
def from_dob_to_age(born):
    today = datetime.date.today()
    return today.year - born.dt.year - ((today.month, today.day) < (born.dt.month.any(), born.dt.day.any()))

# À l'aide des deux fonctions précédentes, on construit notre fonction qui nous permettra de 
# supprimer et corriger les anomalies de notre jeu de données de départ.
def detect_duplicates(df_data, path_referential):
    if (len(df_data) != 0):
        
        # Construction d'une colonne state en se basant sur un référentiel 
        #
        df_patient_dup = df_data.loc[:,['patient_id', 'postcode', 'date_of_birth']]
        
        # On commence par changer le type de la colonne 'postcode' en string
        df_patient_dup.loc[:,'postcode']= df_patient_dup['postcode'].astype(str) 
        
        # On supprime les espaces avant et après 
        df_patient_dup.loc[:,'postcode'] = df_patient_dup['postcode'].str.strip()
        
        # On remplace les tabulation par 0
        df_patient_dup.loc[:,'postcode'] = df_patient_dup['postcode'].replace('\t', 0)
        
        # On remplace les espaces vides par 0
        df_patient_dup.loc[:,'postcode'] = df_patient_dup['postcode'].replace(" ", 0)
        
        # On remplace les NaN par 0
        df_patient_dup.loc[:,'postcode'] = df_patient_dup['postcode'].replace(np.nan, 0)
        
        # On remplace les chaines de caractères par 0
        df_patient_dup.loc[:,'postcode'] = df_patient_dup['postcode'].replace(['.*[a-zA-Z]'], 0, regex=True , inplace=False)
        
        # On transforme le type des valeurs prises par postcode en floet (int) 
        df_patient_dup.loc[:,'postcode'] = df_patient_dup['postcode'].astype(float) # (int)
        
        # Traitements sur la colonne postcode 
        # On remplace les valeurs n'appartenants pas à l'intervalle des vaeurs valides par 0
        df_patient_dup.loc[df_patient_dup['postcode']>9020, 'postcode'] = 0
        df_patient_dup.loc[df_patient_dup['postcode']<200, 'postcode'] = 0
        
        # On ajoute un DataFrame pour le référentiel des codes postaux en Australie
        # path_referential = './data_post_codes.csv'
        referential_PC = pd.read_csv(path_referential, sep = ',') # definir comme paramètre de la fonction
       
        # On fusionne les dataframe df_patient_dup et referential_PC selon la colonne 'postcode'
        # "left join"
        df_patient_dup = pd.merge(df_patient_dup,
                                      referential_PC[['postcode', 'state']],
                                      on='postcode', 
                                      how='left')
        
        # On remplace les NaN dans 'state' par "UNKNOWN" comme valeur.
        df_patient_dup['state'].replace(to_replace = np.nan,
                                        value ="UNKNOWN",
                                        inplace=True)
        
        # Calcul de l'age des patients
        # On remplace les NaN (+ valeurs manquantes ...) par une date de naissance erronée
        df_patient_dup.loc[:,'date_of_birth'] = df_patient_dup['date_of_birth'].replace(np.nan, 99999999)
        
        # Convertion du type de la colonne date_of_birth en entier
        df_patient_dup.loc[:,'date_of_birth'] = df_patient_dup['date_of_birth'].astype(int)
        
        # Convertion des valeurs de la colonne date_of_birth sous un format de dates année-mois-jour
        # les date de naissances érronées sont remplacées par NaT
        df_patient_dup.loc[:,'date_of_birth'] = pd.to_datetime(df_patient_dup['date_of_birth'], format='%Y%m%d', errors='coerce')
        
        # Application de la fonction from_dob_to_age pour le calcul de l'age
        df_patient_dup.loc[:,'age'] = from_dob_to_age(df_patient_dup['date_of_birth'])
        
        # On applique la fonction delete_patientID_duplicates
        # pour supprimer les duplications selon la colonne patient_id
        df_patient_dedup = delete_patientID_duplicates(df_patient_dup)
        
        # On re-ordonne ci-dessous les colonnes
        df_patient_dedup = df_patient_dedup.loc[:,['patient_id', 'postcode', 'state', 'date_of_birth', 'age']]
        
        return df_patient_dedup
    