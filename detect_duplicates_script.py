import pandas as pd
import numpy as np
import datetime

def delete_patientID_duplicates(data):
    # On commence par trier les lignes afin d'afficher d'éventuelles valeurs nulles en premier
    df_sorted = data.sort_values(by=['patient_id', 'date_of_birth', 'postcode'], na_position='first')
    # suppression des doublons selon le champ 'patient_id'
    df_dedup_patient_ID = df_sorted.drop_duplicates(subset=['patient_id'], keep='last')
    return df_dedup_patient_ID

def get_corr_state_from_postcode(data):
    df_patient_res = data[['patient_id', 'postcode', 'date_of_birth']]
    # On supprime les espaces avant et après 
    df_patient_res['postcode'] = data['postcode'].str.strip()
    # On remplace les tabulation par 0
    df_patient_res['postcode'] = df_patient_res['postcode'].replace('\t', 0)
    # On remplace les espaces vides par 0
    df_patient_res['postcode'] = df_patient_res['postcode'].replace(" ", 0)
    # On remplace les NaN par 0
    df_patient_res['postcode'] = df_patient_res['postcode'].replace(np.nan, 0)
    # On remplace les chaines de caractères par 0
    df_patient_res['postcode'] = df_patient_res['postcode'].replace(['.*[a-zA-Z]'], 0, regex=True , inplace=False)
    # On transforme le type des valeurs prises par postcode en int 
    df_patient_res['postcode'] = df_patient_res['postcode'].astype(int)
    # On ajoute un DataFrame pour le référentiel des codes postaux en Australie
    referential_PC = pd.read_csv("data_post_codes.csv", sep = ',')
    # merge 
    df_corrected_state = pd.merge(df_patient_res,
                                referential_PC[['postcode', 'state']],
                                on='postcode', 
                                how='left')
    return df_corrected_state
    

def from_dob_to_age(born):
    today = datetime.date.today()
    return today.year - born.dt.year - ((today.month, today.day) < (born.dt.month.any(), born.dt.day.any()))


def detect_duplicates(df_data):
    if (len(df_data) != 0):
        
        # Application de la fonction delete_patientID_duplicates 
        # pour supprimer les duplications selon le colonne patient_id
        df_patient_dedup = delete_patientID_duplicates(df_data)
        
        # Application de la fonction get_corr_state_from_postcode 
        # pour corriger les nom de villes en se basant sur le code postal 
        df_patient_dedup = get_corr_state_from_postcode(df_patient_dedup)
        
        # Calcul de l'age des patients
        # On remplace les NaN (+ valeurs manquantes ...) par une date de naissance erronée
        df_patient_dedup['date_of_birth'] = df_patient_dedup['date_of_birth'].replace(np.nan, 99999999)
        # Convertion du type de la colonne date_of_birth en entier
        df_patient_dedup['date_of_birth'] = df_patient_dedup['date_of_birth'].astype(int)
        # Convertion des valeurs de la colonne date_of_birth sous un format de dates année-mois-jour
        # les date de naissances érronées sont remplacées par NaT
        df_patient_dedup['date_of_birth'] = pd.to_datetime(df_patient_dedup['date_of_birth'], format='%Y%m%d', errors='coerce')
        # Application de la fonction from_dob_to_age pour le calcul de l'age
        df_patient_dedup['age'] = from_dob_to_age(df_patient_dedup['date_of_birth'])
        return df_patient_dedup
    