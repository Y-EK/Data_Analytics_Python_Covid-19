import pandas as pd
import numpy as np

def detect_duplicates(df_data):
    if (len(df_data) != 0):
        # On commence par trier les lignes afin d'afficher d'éventuelles valeurs nulles en premier
        df_patient_sorted = df_data.sort_values(by=['patient_id', 'date_of_birth', 'postcode'], na_position='first')
        # suppression des doublons selon le champ 'patient_id'
        df_patient_dedup = df_data.drop_duplicates(subset=['patient_id'], keep='last')
        #referential_PC = pd.read_csv("data_post_codes.csv", sep = ',')
        df_result = df_patient_dedup
        return df_patient_dedup
    