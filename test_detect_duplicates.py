# 
# pip install -U pytest
# pip install pandas -U

import pandas as pd
import numpy as np
from pandas._testing import assert_frame_equal
from detect_duplicates_script import detect_duplicates
import datetime

def test_delete_duplicates():
    
    df = pd.DataFrame([
        [771155, 4210, 'QL', 19790108, np.nan],
        [771155, 'null', 'nsss', 19991892.0, 'age of the patient'],
        [771155, '4210', 'nsss', np.nan, 32]
        ], columns = ['patient_id', 'postcode', 'state', 'date_of_birth', 'age'])
    
    df_result = detect_duplicates(df)
    
    df_expected = pd.DataFrame([
        [771155, 4210, 'QLD', datetime.datetime.strptime('1979-01-08', '%Y-%m-%d'), 41]
        ], columns = ['patient_id', 'postcode', 'state', 'date_of_birth', 'age'])
    
    #df_expected.loc[:,'patient_id'] = df_expected['patient_id'].astype(int)
    #df_expected.loc[:,'postcode'] = df_expected['postcode'].astype(int)
    #df_expected.loc[:,'state'] = df_expected['state'].astype(str)
    #df_expected.loc[:,'age'] = df_expected['age'].astype(float)
    
    assert_frame_equal(left=df_expected.reset_index(drop=True), right=df_result.reset_index(drop=True),
                       check_dtype=False)
                       
        
        