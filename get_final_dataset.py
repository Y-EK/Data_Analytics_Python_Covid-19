import pandas as pd
import numpy as np
import datetime
from getting_started import *
import detect_duplicates_script as script_dd

def get_cleaned_df_pcr(data):
    df_pcr_cleaned = df_pcr.copy()
    # On commence par changer le type de la colonne 'postcode' en string
    df_pcr_cleaned.loc[:,'pcr']= df_pcr_cleaned['pcr'].astype(str)
    # On supprime les espaces avant et après 
    df_pcr_cleaned.loc[:,'pcr'] = df_pcr_cleaned['pcr'].str.strip()
    # Conversion en majuscule 
    df_pcr_cleaned.loc[:,'pcr'] = df_pcr_cleaned['pcr'].str.upper()
    # Normalisation de la colonne pcr
    # 'negative' <- 0 
    df_pcr_cleaned["pcr"].replace({"N": 0}, inplace=True)
    df_pcr_cleaned["pcr"].replace({"NEGATIVE": 0}, inplace=True)
    # 'postive' <- 1
    df_pcr_cleaned["pcr"].replace({"P": 1}, inplace=True)
    df_pcr_cleaned["pcr"].replace({"POSITIVE": 1}, inplace=True)
    #
    return df_pcr_cleaned
    

def get_final_ds(data_patient, data_pcr):
    
    # data frame obtenu après suppression des duplications du jeu de donnée patient
    df_patient_dedup = script_dd.detect_duplicates(data_patient)
    
    # data frame obtenu après un processus de data cleaning appliqué au jeu de donnée
    # sur les données relatifs aux contamination par le Covid19
    df_cleaned_pcr = get_cleaned_df_pcr(data_pcr)
    
    df_final_ds = pd.merge(df_cleaned_pcr,
                           df_patient_dedup,
                           on='patient_id', 
                           how='left')
    
    return df_final_ds
    
    





