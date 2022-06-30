import pandas as pd
import os
import pickle
import subprocess
import sys


# ~~~ modbus-eaton init~~~ #
def pickle_eaton_df():
    # xlsx = pd.ExcelFile('/home/pi/PyModBus/preprod/pxm2k-modbus-uid-0.xlsx')
    xlsx = pd.ExcelFile('pxm2k-modbus-uid-0.xlsx')
    df = xlsx.parse('pxm2k-modbus-uid-0')
    df.to_pickle(path='modbus-eaton-df.pkl')
    return df

def setup_address_strings(df = pickle_eaton_df()):
    address_strings = {}
    for x,y,z,name in zip(df['Base Address (1-based)'].values, df['Size (bytes)'].values, df['Type'].values, df['Display Name'].values):
        if z != 'STRING':
            address_strings[(x,z,name)] = int(y) // 2
        else:
            address_strings[(x,z,name)] = 12
    return address_strings

def pickle_address_strings(address_strings = setup_address_strings()):
    with open(f"modbus-eaton-address-strings.pkl", 'wb') as handle:
        pickle.dump(address_strings, handle, protocol=pickle.HIGHEST_PROTOCOL)

pickle_address_strings()

# ~~~ modbus-SEL init~~~ #

'''
sys.argv[1] is a comma-seperated string whitelisting which SEL modbus registers
are to be pickled 

so 
python Resources/fetch_SEL_addresses.py 2,3,4
means "We are going to read the modbus addresses with 0, 1, 2 'extra' parameters"
(A much better explanation will be given later, and eventually this prototype logic
will be replaced with a general address white/blacklist.)
'''
def pickle_SEL_df_dict():
    whitelist = sys.argv[1]
    subprocess.call(['python', 'fetch_SEL_addresses.py', whitelist])
    df_dict = {}
    for i in ["2","3","4","5","6","7","8","9","10","11","58"]:
        if i in whitelist:
            df_dict[i] = pd.read_csv(f'SEL_csvs\\{i}.csv', encoding = 'latin1')
    pickle.dump(df_dict, open('modbus-sel-dfs.pkl', 'wb'))

pickle_SEL_df_dict()