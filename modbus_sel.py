#  l = ['TEMP', '3I0', '3I0FA', '3I2', '3I2FA', '3V0_MAG', 'RESERVED',
# '3V0FA', 'FREQ', 'I1', 'I1FA', 'IA', 'IAFA', 'IB', 'IBFA', 'IC',
# 'ICFA', 'IG', 'IGFA', 'IN', 'INFA', 'KVAR3', 'RESERVED', 'KVARA',
# 'RESERVED', 'KVARB', 'RESERVED', 'KVARC', 'RESERVED', 'KW3',
# 'RESERVED', 'KWA', 'RESERVED', 'KWB', 'RESERVED', 'KWC',
# 'RESERVED', 'LDPF3', 'LDPFA', 'LDPFB', 'LDPFC', 'PF3', 'PFA',
# 'PFB', 'PFC', 'V1', 'RESERVED', 'V1FA', 'V2', 'RESERVED', 'V2FA',
# 'VA', 'RESERVED', 'VAB', 'RESERVED', 'VABFA', 'VAFA', 'VB',
# 'RESERVED', 'VBC', 'RESERVED', 'VBCFA', 'VBFA', 'VC', 'RESERVED',
# 'VCA', 'RESERVED', 'VCAFA', 'VCFA', 'VDC', 'VS', 'RESERVED',
# 'VSFA', '3I2DEM', '3I2PK', 'IADEM', 'IAPK', 'IBDEM', 'IBPK',
# 'ICDEM', 'ICPK', 'IGDEM', 'IGPK', 'INDEM', 'INPK', 'KVR3DI',
# 'RESERVED', 'KVR3DO', 'RESERVED', 'KVR3PI', 'RESERVED', 'KVR3PO',
# 'RESERVED', 'KVRADI', 'RESERVED', 'KVRADO', 'RESERVED', 'KVRAPI',
# 'RESERVED', 'KVRAPO', 'RESERVED', 'KVRBDI', 'RESERVED', 'KVRBDO',
# 'RESERVED', 'KVRBPI', 'RESERVED', 'KVRBPO', 'RESERVED', 'KVRCDI',
# 'RESERVED', 'KVRCDO', 'RESERVED', 'KVRCPI', 'RESERVED', 'KVRCPO',
# 'RESERVED', 'KW3DI', 'RESERVED', 'KW3DO', 'RESERVED', 'KW3PI',
# 'RESERVED', 'KW3PO', 'RESERVED', 'KWADI', 'RESERVED', 'KWADO',
# 'RESERVED', 'KWAPI', 'RESERVED', 'KWAPO', 'RESERVED', 'KWBDI',
# 'RESERVED', 'KWBDO', 'RESERVED', 'KWBPI', 'RESERVED', 'KWBPO',
# 'RESERVED', 'KWCDI', 'RESERVED', 'KWCDO', 'RESERVED', 'KWCPI',
# 'RESERVED', 'KWCPO', 'RESERVED', 'MVRH3I', 'RESERVED', 'MVRH3O',
# 'RESERVED', 'MVRHAI', 'RESERVED', 'MVRHAO', 'RESERVED', 'MVRHBI',
# 'RESERVED', 'MVRHBO', 'RESERVED', 'MVRHCI', 'RESERVED', 'MVRHCO',
# 'RESERVED', 'MWH3I', 'RESERVED', 'MWH3O', 'RESERVED', 'MWHAI',
# 'RESERVED', 'MWHAO', 'RESERVED', 'MWHBI', 'RESERVED', 'MWHBO',
# 'RESERVED', 'MWHCI', 'RESERVED', 'MWHCO', 'RESERVED', 'IAH01',
# 'IAHR', 'IAHT', 'IBH01', 'IBHR', 'IBHT', 'ICH01', 'ICHR', 'ICHT',
# 'INH01', 'INHR', 'INHT', 'VAH01', 'RESERVED', 'VAHR', 'RESERVED',
# 'VAHT', 'VBH01', 'RESERVED', 'VBHR', 'RESERVED', 'VBHT', 'VCH01',
# 'RESERVED', 'VCHR', 'RESERVED', 'VCHT', 'VSH01', 'RESERVED',
# 'VSHR', 'RESERVED', 'VSHT', 'EVE_TYPE', 'EVESEL', 'FDATE_D',
# 'FDATE_M', 'FDATE_Y', 'FFREQ', 'FGRP', 'FI', 'FIA', 'FIB', 'FIC',
# 'FIG', 'FIN', 'FIQ', 'FLOC', 'FSHO', 'FTIME_H', 'FTIME_M',
# 'FTIME_S', 'NUMEVE', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A',
# 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A',
# 'N/A', 'N/A']

# for n,i in enumerate(l):
#     scaling_factor = 1
#     if i == 'TEMP':
#         scaling_factor = 10
#     if 'FA' in i:
#         scaling_factor = 100
#     if i == 'FREQ':
#         scaling_factor = 100
#     d[n] = [i, scaling_factor]

rules = {0: ['TEMP', 10], 1: ['3I0', 1], 2: ['3I0FA', 100], 3: ['3I2', 1], 4: ['3I2FA', 100], 5: ['3V0_MAG', 1], 6: ['RESERVED', 1], 7: ['3V0FA', 100], 8: ['FREQ', 100], 9: ['I1', 1], 10: ['I1FA', 100], 11: ['IA', 1], 12: ['IAFA', 100], 13: ['IB', 1], 14: ['IBFA', 100], 15: ['IC', 1], 16: ['ICFA', 100], 17: ['IG', 1], 18: ['IGFA', 100], 19: ['IN', 1], 20: ['INFA', 100], 21: ['KVAR3', 1], 22: ['RESERVED', 1], 23: ['KVARA', 1], 24: ['RESERVED', 1], 25: ['KVARB', 1], 26: ['RESERVED', 1], 27: ['KVARC', 1], 28: ['RESERVED', 1], 29: ['KW3', 1], 30: ['RESERVED', 1], 31: ['KWA', 1], 32: ['RESERVED', 1], 33: ['KWB', 1], 34: ['RESERVED', 1], 35: ['KWC', 1], 36: ['RESERVED', 1], 37: ['LDPF3', 1], 38: ['LDPFA', 100], 39: ['LDPFB', 1], 40: ['LDPFC', 1], 41: ['PF3', 1], 42: ['PFA', 100], 43: ['PFB', 1], 44: ['PFC', 1], 45: ['V1', 1], 46: ['RESERVED', 1], 47: ['V1FA', 100], 48: ['V2', 1], 49: ['RESERVED', 1], 50: ['V2FA', 100], 51: ['VA', 1], 52: ['RESERVED', 1], 53: ['VAB', 1], 54: ['RESERVED', 1], 55: ['VABFA', 100], 56: ['VAFA', 100], 57: ['VB', 1], 58: ['RESERVED', 1], 59: ['VBC', 1], 60: ['RESERVED', 1], 61: ['VBCFA', 100], 62: ['VBFA', 100], 63: ['VC', 1], 64: ['RESERVED', 1], 65: ['VCA', 1], 66: ['RESERVED', 1], 67: ['VCAFA', 100], 68: ['VCFA', 100], 69: ['VDC', 1], 70: ['VS', 1], 71: ['RESERVED', 1], 72: ['VSFA', 100], 73: ['3I2DEM', 1], 74: ['3I2PK', 1], 75: ['IADEM', 1], 76: ['IAPK', 1], 77: ['IBDEM', 1], 78: ['IBPK', 1], 79: ['ICDEM', 1], 80: ['ICPK', 1], 81: ['IGDEM', 1], 82: ['IGPK', 1], 83: ['INDEM', 1], 84: ['INPK', 1], 85: ['KVR3DI', 1], 86: ['RESERVED', 1], 87: ['KVR3DO', 1], 88: ['RESERVED', 1], 89: ['KVR3PI', 1], 90: ['RESERVED', 1], 91: ['KVR3PO', 1], 92: ['RESERVED', 1], 93: ['KVRADI', 1], 94: ['RESERVED', 1], 95: ['KVRADO', 1], 96: ['RESERVED', 1], 97: ['KVRAPI', 1], 98: ['RESERVED', 1], 99: ['KVRAPO', 1], 100: ['RESERVED', 1], 101: ['KVRBDI', 1], 102: ['RESERVED', 1], 103: ['KVRBDO', 1], 104: ['RESERVED', 1], 105: ['KVRBPI', 1], 106: ['RESERVED', 1], 107: ['KVRBPO', 1], 108: ['RESERVED', 1], 109: ['KVRCDI', 1], 110: ['RESERVED', 1], 111: ['KVRCDO', 1], 112: ['RESERVED', 1], 113: ['KVRCPI', 1], 114: ['RESERVED', 1], 115: ['KVRCPO', 1], 116: ['RESERVED', 1], 117: ['KW3DI', 1], 118: ['RESERVED', 1], 119: ['KW3DO', 1], 120: ['RESERVED', 1], 121: ['KW3PI', 1], 122: ['RESERVED', 1], 123: ['KW3PO', 1], 124: ['RESERVED', 1], 125: ['KWADI', 1], 126: ['RESERVED', 1], 127: ['KWADO', 1], 128: ['RESERVED', 1], 129: ['KWAPI', 1], 130: ['RESERVED', 1], 131: ['KWAPO', 1], 132: ['RESERVED', 1], 133: ['KWBDI', 1], 134: ['RESERVED', 1], 135: ['KWBDO', 1], 136: ['RESERVED', 1], 137: ['KWBPI', 1], 138: ['RESERVED', 1], 139: ['KWBPO', 1], 140: ['RESERVED', 1], 141: ['KWCDI', 1], 142: ['RESERVED', 1], 143: ['KWCDO', 1], 144: ['RESERVED', 1], 145: ['KWCPI', 1], 146: ['RESERVED', 1], 147: ['KWCPO', 1], 148: ['RESERVED', 1], 149: ['MVRH3I', 1], 150: ['RESERVED', 1], 151: ['MVRH3O', 1], 152: ['RESERVED', 1], 153: ['MVRHAI', 1], 154: ['RESERVED', 1], 155: ['MVRHAO', 1], 156: ['RESERVED', 1], 157: ['MVRHBI', 1], 158: ['RESERVED', 1], 159: ['MVRHBO', 1], 160: ['RESERVED', 1], 161: ['MVRHCI', 1], 162: ['RESERVED', 1], 163: ['MVRHCO', 1], 164: ['RESERVED', 1], 165: ['MWH3I', 1], 166: ['RESERVED', 1], 167: ['MWH3O', 1], 168: ['RESERVED', 1], 169: ['MWHAI', 1], 170: ['RESERVED', 1], 171: ['MWHAO', 1], 172: ['RESERVED', 1], 173: ['MWHBI', 1], 174: ['RESERVED', 1], 175: ['MWHBO', 1], 176: ['RESERVED', 1], 177: ['MWHCI', 1], 178: ['RESERVED', 1], 179: ['MWHCO', 1], 180: ['RESERVED', 1], 181: ['IAH01', 1], 182: ['IAHR', 1], 183: ['IAHT', 1], 184: ['IBH01', 1], 185: ['IBHR', 1], 186: ['IBHT', 1], 187: ['ICH01', 1], 188: ['ICHR', 1], 189: ['ICHT', 1], 190: ['INH01', 1], 191: ['INHR', 1], 192: ['INHT', 1], 193: ['VAH01', 1], 194: ['RESERVED', 1], 195: ['VAHR', 1], 196: ['RESERVED', 1], 197: ['VAHT', 1], 198: ['VBH01', 1], 199: ['RESERVED', 1], 200: ['VBHR', 1], 201: ['RESERVED', 1], 202: ['VBHT', 1], 203: ['VCH01', 1], 204: ['RESERVED', 1], 205: ['VCHR', 1], 206: ['RESERVED', 1], 207: ['VCHT', 1], 208: ['VSH01', 1], 209: ['RESERVED', 1], 210: ['VSHR', 1], 211: ['RESERVED', 1], 212: ['VSHT', 1], 213: ['EVE_TYPE', 1], 214: ['EVESEL', 1], 215: ['FDATE_D', 1], 216: ['FDATE_M', 1], 217: ['FDATE_Y', 1], 218: ['FFREQ', 1], 219: ['FGRP', 1], 220: ['FI', 1], 221: ['FIA', 1], 222: ['FIB', 1], 223: ['FIC', 1], 224: ['FIG', 1], 225: ['FIN', 1], 226: ['FIQ', 1], 227: ['FLOC', 1], 228: ['FSHO', 1], 229: ['FTIME_H', 1], 230: ['FTIME_M', 1], 231: ['FTIME_S', 1], 232: ['NUMEVE', 1], 233: ['N/A', 1], 234: ['N/A', 1], 235: ['N/A', 1], 236: ['N/A', 1], 237: ['N/A', 1], 238: ['N/A', 1], 239: ['N/A', 1], 240: ['N/A', 1], 241: ['N/A', 1], 242: ['N/A', 1], 243: ['N/A', 1], 244: ['N/A', 1], 245: ['N/A', 1], 246: ['N/A', 1], 247: ['N/A', 1], 248: ['N/A', 1], 249: ['N/A', 1]}

def fetch_sel_dictionary(resource, client):
   start = 0
   raw_data = []
   while start < 250:
      raw_data += client.read_holding_registers(start, 125).registers
      start += 125
   rules = resource
   result = dict()
   for n,i in enumerate(raw_data):
      result[raw_data[n][0]] = rules[n] / raw_data[n][1]
   return result