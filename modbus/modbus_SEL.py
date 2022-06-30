import pickle
from helpers import generate_timestamp
import sys
sys.path.append('C:\\Users\\integral\\Documents\\work\\git_repos\\SEL_modbus') #to fetch helpers.py
from helpers import generate_timestamp

path = 'C:\\Users\\integral\\Documents\\work\\git_repos\\SEL_modbus\\Resources\\modbus-sel-dfs.pkl'
with open(path, 'rb') as handle:
    df_dict = pickle.load(handle)

df = df_dict['2']

#to-do: handle NaN stuff better
df = df.dropna()

addresses = df['Address'].values
labels = []
scale_factors = []
for i in addresses:
    labels.append(df.loc[df['Address'] == i]['Label'])
    scale_factors.append(df.loc[df['Address'] == i]['Scale Factor'])

labels = ["Address","Label","Units","Min","Max","Default","Scale Factor","DeviceNet Parameter Numbers"]

def fetch_SEL_dictionary(client):
    d = {}
    d['startReadTime'] = generate_timestamp()
    for n,address in enumerate(addresses):
        regs = client.read_holding_registers(address, 1).registers
        val = regs[0] * scale_factors[n]
        d[labels[n]] = val
    d['endReadTime'] = generate_timestamp()
    return d