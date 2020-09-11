# Nous rappelons ici la commande pour installer 
# le package python pytest :
# pip install -U pytest

import pandas as pd
import numpy as np
from pandas._testing import assert_frame_equal
from detect_duplicates_script import detect_duplicates
import datetime

# chemin relatif du fichier csv utilisé comme référentiel des codes postaux
path_referential = './data_post_codes.csv';


# Dans ce test nous vérifions que la fonction detect_duplicates 
# supprime les duplications en respectons la condition :
# garder la ligne avec le moins de valeurs nulles (non valides) au niveau des 
# champs postcode et date_of_birth
def test_delete_duplicates():
    
    df = pd.DataFrame([
        [771155, 4210, 'QL', 19790108, np.nan],
        [771155, 'null', 'nsss', 19991892.0, 'age of the patient'],
        [771155, '4210', 'nsss', np.nan, 32]
        ], columns = ['patient_id', 'postcode', 'state', 'date_of_birth', 'age'])
    
    df_result = detect_duplicates(df, path_referential)
    
    df_expected = pd.DataFrame([
        [771155, 4210, 'QLD', datetime.datetime.strptime('1979-01-08', '%Y-%m-%d'), 41]
        ], columns = ['patient_id', 'postcode', 'state', 'date_of_birth', 'age'])
    
    #df_expected.loc[:,'patient_id'] = df_expected['patient_id'].astype(int)
    #df_expected.loc[:,'postcode'] = df_expected['postcode'].astype(int)
    #df_expected.loc[:,'state'] = df_expected['state'].astype(str)
    #df_expected.loc[:,'age'] = df_expected['age'].astype(float)
    
    assert_frame_equal(left=df_expected.reset_index(drop=True), right=df_result.reset_index(drop=True),
                       check_dtype=False)

# Ici on vérifie que notre fonction supprime les lignes avec un patient_id contenant une valeur nulle.    
def test_delete_duplicates_nv():
    
    df = pd.DataFrame([
        [104136, 812, 'NT', 19801222, 40],
        [np.nan, 4221, 'QLD', 19771201, 43],
        [None, 2087, 'NSW', 19330815, 87]
        ], columns = ['patient_id', 'postcode', 'state', 'date_of_birth', 'age'])
    
    df_result = detect_duplicates(df, path_referential)
    
    df_expected = pd.DataFrame([
        [104136, 812, 'NT', datetime.datetime.strptime('1980-12-22', '%Y-%m-%d'), 40]
        ], columns = ['patient_id', 'postcode', 'state', 'date_of_birth', 'age'])
    
    assert_frame_equal(left=df_expected.reset_index(drop=True), right=df_result.reset_index(drop=True),
                       check_dtype=False)

# Dans ce test on vérifie que notre fonction calcule correctement l'age
# à partir de la date de naissance.
def test_get_corrected_age():
        
    df = pd.DataFrame([
        [100064, 4208, 'QLD', 19810905.0, np.nan],
        [100215, 6107, 'WA', 19061018.0, ''],
        [100363, 3029, 'VIC', 19030606.0, 32]
        ], columns = ['patient_id', 'postcode', 'state', 'date_of_birth', 'age'])
    
    df_result = detect_duplicates(df, path_referential)
    
    df_expected = pd.DataFrame([
        [100064, 4208, 'QLD', datetime.datetime.strptime('1981-09-05', '%Y-%m-%d'), 39],
        [100215, 6107, 'WA', datetime.datetime.strptime('1906-10-18', '%Y-%m-%d') , 114],
        [100363, 3029, 'VIC', datetime.datetime.strptime('1903-06-06', '%Y-%m-%d'), 117]
        ], columns = ['patient_id', 'postcode', 'state', 'date_of_birth', 'age'])
    
    assert_frame_equal(left=df_expected.reset_index(drop=True), right=df_result.reset_index(drop=True),
                       check_dtype=False)  

# Complément du test précédent : 
# ici nous vérifions que notre fonction ne calcul l'age que
# lorsque la date de naissance correspond à une date de naissance valide
def test_get_corrected_age_wdob():
        
    df = pd.DataFrame([
        [378167, 2428, 'NSW', np.nan, 31],
        [427069, 6000, 'WA', 19451796, 75],
        ], columns = ['patient_id', 'postcode', 'state', 'date_of_birth', 'age'])
    
    df_result = detect_duplicates(df, path_referential)
    
    df_expected = pd.DataFrame([
        [378167, 2428, 'NSW', np.datetime64('NaT'), np.nan],
        [427069, 6000, 'WA', np.datetime64('NaT'), np.nan],
        ], columns = ['patient_id', 'postcode', 'state', 'date_of_birth', 'age'])
    
    assert_frame_equal(left=df_expected.reset_index(drop=True), right=df_result.reset_index(drop=True),
                       check_dtype=False)   
    
# Dans le test ci-dessous, on vérifie que notre fonction
# associe le nom de la région lorsqu'un code postale correct est fournit.
def test_get_corrected_state(): 
    
    df = pd.DataFrame([
        [100390, 6155, 'qld', 19160912, 104],
        [100559, 2400, ' ', 19570220, 63],
        [100901, 5333, np.nan, 19750207, 45]
        ], columns = ['patient_id', 'postcode', 'state', 'date_of_birth', 'age'])
    
    df_result = detect_duplicates(df, path_referential)
    
    df_expected = pd.DataFrame([
        [100390, 6155, 'WA', datetime.datetime.strptime('1916-09-12', '%Y-%m-%d'), 104],
        [100559, 2400, 'NSW', datetime.datetime.strptime('1957-02-20', '%Y-%m-%d') , 63],
        [100901, 5333, 'SA', datetime.datetime.strptime('1975-02-07', '%Y-%m-%d'), 45]
        ], columns = ['patient_id', 'postcode', 'state', 'date_of_birth', 'age'])
    
    assert_frame_equal(left=df_expected.reset_index(drop=True), right=df_result.reset_index(drop=True),
                       check_dtype=False)    

# Ici on s'assure que la fonction associe la valeur "UNKNOWN" à toutes valeurs
# érronée du code postal.
def test_get_corrected_state_wpc(): 
    
    df = pd.DataFrame([
        [100126, 199, 'ACT', 19181210, 102],
        [100390, np.nan, 'WA', 19160912, 104],
        [100559, None, 'NSW', 19570220, 63],
        [100901, 10000, 'SA', 19750207, 45]
        ], columns = ['patient_id', 'postcode', 'state', 'date_of_birth', 'age'])
    
    df_result = detect_duplicates(df, path_referential)
    
    df_expected = pd.DataFrame([
        [100126, 0, "UNKNOWN", datetime.datetime.strptime('1918-12-10', '%Y-%m-%d'), 102],
        [100390, 0, "UNKNOWN", datetime.datetime.strptime('1916-09-12', '%Y-%m-%d'), 104],
        [100559, 0, "UNKNOWN", datetime.datetime.strptime('1957-02-20', '%Y-%m-%d'), 63],
        [100901, 0, "UNKNOWN", datetime.datetime.strptime('1975-02-07', '%Y-%m-%d'), 45]
        ], columns = ['patient_id', 'postcode', 'state', 'date_of_birth', 'age'])
    
    assert_frame_equal(left=df_expected.reset_index(drop=True), right=df_result.reset_index(drop=True),
                       check_dtype=False)
                       
        
        