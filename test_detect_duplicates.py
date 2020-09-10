# 
# pip install -U pytest
# pip install pandas -U

import pandas as pd
import numpy as np
from pandas._testing import assert_frame_equal
from detect_duplicates_script import detect_duplicates
import datetime

path_referential = './data_post_codes.csv';

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

def test_get_corrected_state_wpc(): 
    
    df = pd.DataFrame([
        [100126, 199, 'ACT', 19181210, 102],
        [100390, np.nan, 'WA', 19160912, 104],
        [100559, None, 'NSW', 19570220, 63],
        [100901, 10000, 'SA', 19750207, 45]
        ], columns = ['patient_id', 'postcode', 'state', 'date_of_birth', 'age'])
    
    df_result = detect_duplicates(df, path_referential)
    
    df_expected = pd.DataFrame([
        [100126, 0, np.nan, datetime.datetime.strptime('1918-12-10', '%Y-%m-%d'), 102],
        [100390, 0, np.nan, datetime.datetime.strptime('1916-09-12', '%Y-%m-%d'), 104],
        [100559, 0, np.nan, datetime.datetime.strptime('1957-02-20', '%Y-%m-%d'), 63],
        [100901, 0, np.nan, datetime.datetime.strptime('1975-02-07', '%Y-%m-%d'), 45]
        ], columns = ['patient_id', 'postcode', 'state', 'date_of_birth', 'age'])
    
    assert_frame_equal(left=df_expected.reset_index(drop=True), right=df_result.reset_index(drop=True),
                       check_dtype=False)
                       
        
        