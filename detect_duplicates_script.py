import pandas as pd
import numpy as np

def detect_duplicates(df_data):
    if (len(df_data) != 0):
        # On commence par trier les lignes afin d'afficher d'éventuelles valeurs nulles en premier
        df_patient_sorted = df_data.sort_values(by=['patient_id', 'date_of_birth', 'postcode'], na_position='first')
        # suppression des doublons selon le champ 'patient_id'
        df_patient_dedup = df_data.drop_duplicates(subset=['patient_id'], keep='last')
        # On se restreint sur les colonnes 'patient_id', 'postcode', 'date_of_birth'
        df_patient_dedup = df_patient_dedup[['patient_id', 'postcode', 'date_of_birth']]
        # On supprime les espaces avant et après 
        df_patient_dedup['postcode'] = df_patient_dedup['postcode'].str.strip()
        # On remplace les tabulation par 0
        df_patient_dedup['postcode'] = df_patient_dedup['postcode'].replace('\t', 0)
        # On remplace les espaces vides par 0
        df_patient_dedup['postcode'] = df_patient_dedup['postcode'].replace(" ", 0)
        # On remplace les NaN par 0
        df_patient_dedup['postcode'] = df_patient_dedup['postcode'].replace(np.nan, 0)
        # On remplace les chaines de caractères par 0
        df_patient_dedup['postcode'] = df_patient_dedup['postcode'].replace(['.*[a-zA-Z]'], 0, regex=True , inplace=False)
        # On transforme le type des valeurs prises par postcode en int 
        df_patient_dedup['postcode'] = df_patient_dedup['postcode'].astype(int)
        # On ajoute un DataFrame pour le référentiel des codes postaux en Australie
        referential_PC = pd.read_csv("data_post_codes.csv", sep = ',')
        df_result = df_patient_dedup
        return df_patient_dedup
    