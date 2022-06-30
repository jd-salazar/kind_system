import pdfplumber
import regex as re
import os
import pretty_errors
#UNIMPLEMENTED ADDRESSES ARE IN TO-DO.txt
pdf = pdfplumber.open("751A Manual.pdf")
def fetch_pages(pdf=pdf, first=509, last=564):
    f = open('raw_text.txt','w')
    for pg in pdf.pages[first:last]:
        f.write(pg.extract_text())
    f.close()
fetch_pages(pdf, 509, 564)

f = open('raw_text.txt','r')
text = f.readlines()
f.close()

def unit_sanitizer(l, key):
    units = ["V", "A", "%", "Hz","sec","mA","°C","xVnm","deg","ms","cyc","min","kW","kVAR","kVA","MWhr","MVARh","MVAh","EU","kA","hour","xInm","Hz/s","VA","Hz/sec","xINOM"]
    single_char_units = ["V", "A", "%"]
    multichar_units = ["Hz","sec","mA","°C","xVnm","deg","ms","cyc","min","kW","kVAR","kVA","MWhr","MVARh","MVAh","EU","kA","hour","xInm","Hz/s","VA","Hz/sec","xINOM"]
    l[0] = l[0].replace('\n' , '').replace('na','n/a')
    split = l[0].split()
    counter = -1
    flag = False
    singlechar_found = False
    multichar_found = False
    while not flag:
        if not split[counter].replace('.','').isdigit():
            flag = True
            if re.search(r'–[0-9]+',split[counter].replace('.','')):
                flag = False
        counter -= 1
    counter += 1
    if (len(split[counter]) == 1) and (split[counter] in single_char_units):
        singlechar_found = True
    if split[counter] in multichar_units:
        multichar_found = True
    if (multichar_found == False) and (singlechar_found == False):
        counter += 1
        pass
    return ['_'.join(split[:counter]), ','.join(split[counter:])]

list_sanitaztion_regex = re.compile(r'[0-9] \=|[0-9]{2,3} \=|[0-9]+–[0-9]+|Bit [0-9]+ \=|Bit [0-9]+–Bit [0-9]+ \=|Bit [0-9]+–[0-9]+')
# list_sanitaztion_regex = re.compile(r'[0-9] \=|[0-9]{2,3} \=|[0-9]+–[0-9]+|Bit [0-9]+ \=|Bit [0-9]+–Bit [0-9]+ \=|Bit [0-9]+–[0-9]+|[0-9a-fA-F]+h \=')
def list_sanitizer(l, key, rgx=list_sanitaztion_regex):
    units = ["V", "A", "%", "Hz","sec","mA","°C","xVnm","deg","ms","cyc","min","kW","kVAR","kVA","MWhr","MVARh","MVAh","EU","kA","hour","xInm","Hz/s","VA","Hz/sec","xINOM"]
    single_char_units = ["V", "A", "%"]
    multichar_units = ["Hz","sec","mA","°C","xVnm","deg","ms","cyc","min","kW","kVAR","kVA","MWhr","MVARh","MVAh","EU","kA","hour","xInm","Hz/s","VA","Hz/sec","xINOM"]
    if len(l) >= 2:
        counter = 1
        while rgx.search(l[counter]):
            counter += 1
            if counter == len(l):
                return list_sanitizer([l[0]], key) + l[counter:]
        return list_sanitizer([l[0]], key) + l[1:counter]
    if len(l) == 1:
        return unit_sanitizer(l, key)
        
delimiter_regex = re.compile(r'[0-9]{3,4}A?B?C?D?E?F?H?')
def process_text(text=text, rgx=delimiter_regex):
    d = {}
    d[0] = ['(R)_Reservedc', '0,100,1']
    d[1] = ["(R/W) USER REG #1 610 1947 650 1 101"]
    current_key = 1
    previous_key = 1
    for line in text:
        if delimiter_regex.search(line[0:5]):
            current_key = delimiter_regex.search(line[0:5])[0]
            d[previous_key] = list_sanitizer(d[previous_key], previous_key)
            previous_key = current_key
            d[current_key] = [line]
        else:
            d[current_key].append(line)
    del(d[0]) #gave up on it
    del(d['8000']) #regex can't do everything
    d['264'] =  ['264_(R/W)_EVE_MSG_PTS_EN', 'n/a,0,32,0,1,364', '0 = N', '1–32'] #hacky nonsense
    d['712'] = ['712_(R)_MAX_WINDING_RTD', '°C,–32768,32767,0,1,812', "7FFFh = Open", "8000h = Short", "7FFCh = Comm Fail", "7FF8h = Stat Fail", "7FFEh = Fail", "7FF0h = NA"] #hacky nonsense
    d['1754'] = ['1754_(R)_EVENT_TYPE', 'n/a,0,55,0,1,1854',"0 = TRIP*", "1 = PHASE A1 50 TRIP", "2 = PHASE B1 50 TRIP", "3 = PHASE C1 50 TRIP", "4 = PHASE 50 TRIP", "5 = GND/NEUT 50 TRIP", "6 = NEG SEQ 50 TRIP", "7 = PHASE A 51 TRIP", "8 = PHASE B 51 TRIP", "9 = PHASE C 51 TRIP", "10 = PHASE 51 TRIP", "11 = GND/NEUT 51 TRIP", "12 = NEG SEQ 51 TRIP", "13 = 59 TRIP", "14 = 55 TRIP", "15 = 81 UF TRIP", "16 = 81 OF TRIP", "17 = POWERELEMNT TRIP", "18 = ARC FLASH TRIP", "19 = RTD TRIP", "20 = REMOTE TRIP", "21 = 27 TRIP", "22 = RTD FAIL TRIP", "23 = BREAKER FAILURE TRIP", "24 = COMMIDLELOSSTRIP", "25 = TRIGGER", "26 = ER TRIGGER", "27 = TRIP", "28 = AG fault, no OC trip, GFLT=1", "29 = BG fault, no OC trip, GFLT=1", "30 = ABG fault, no OC trip, GFLT=1", "31 = CG fault, no OC trip, GFLT=1", "32 = CAG fault, no OC trip, GFLT=1", "33 = BCG fault, no OC trip, GFLT=1", "34 = ABC fault, no OC trip, GFLT=1", "35 = AG fault, OC trip, GFLT=1", "36 = BG fault, OC trip, GFLT=1", "37 = ABG fault, OC trip, GFLT=1", "38 = CG fault, OC trip, GFLT=1", "39 = CAG fault, OC trip, GFLT=1", "40 = BCG fault, OC trip, GFLT=1", "41 = ABC fault, OC trip, GFLT=1", "42 = AG fault, no OC trip, GFLT=0", "43 = BG fault, no OC trip, GFLT=0", "44 = AB fault, no OC trip, GFLT=0", "45 = CG fault, no OC trip, GFLT=0", "46 = CA fault, no OC trip, GFLT=0", "47 = BC fault, no OC trip, GFLT=0", "48 = ABC fault, no OC trip, GFLT=0", "49 = AG fault, OC trip, GFLT=0", "50 = BG fault, OC trip, GFLT=0", "51 = AB fault, OC trip, GFLT=0", "52 = CG fault, OC trip, GFLT=0", "53 = CA fault, OC trip, GFLT=0", "54 = BC fault, OC trip, GFLT=0", "55 = ABC fault, OC trip, GFLT=0"]
    #1754 is a one-of-a-kind and relates to faults, so it's worth manually setting
    del(d['400AH']) #note: docs say unused (pg E.79)
    del(d['4011H']) #note: docs say reserved, always return 0 (pg E.80)
    del(d['4018H']) #note: docs say reserved, always return 0 (pg E.80)
    return d

d = process_text()

def delete_addresses(d = d):
    blacklist = ["865", "1665", "1681", "4000H", "4001H", "4002H", "4003H", "4004H", "4005H", "4006H", "4007H", "4008H", "4009H", "400BH", "400DH", "400EH", "400FH", "4010H", "4014H", "4015H", "4016H", "4017H", "1705", "1719", "2110H", "3000H", "3001H", "3002H", "3003H", "3004H", "3005H", "3006H", "3007H", "3008H", "2058", "2000H", "2101H", "2057", "2102H", "2103H", "2104H", "2105H", "2106H", "2107H", "2108H", "2109H", "210AH", "210BH", "210CH", "210DH", "210EH", "210FH", "3009H", "300AH", "300BH", "300CH", "300DH", "300EH", "300FH", "3010H", "3011H", "3012H", "3013H", "3014H", "3015H", "3016H", "3017H", "3018H", "3019H", "301AH", "301BH", "301CH", "301DH", "301EH", "301FH", "3020H", "3021H", "3022H", "3023H", "3024H", "3025H", "3026H", "3027H", "3028H", "3029H", "302AH", "302BH", "302CH", "302DH", "302EH", "302FH", "3030H", "3031H", "3032H", "3033H", "3034H", "3035H", "3036H", "3037H", "3038H", "3039H", "303AH", "303BH", "303CH"]
    for i in blacklist:
        del(d[i])        
    return d

d = delete_addresses()

def process_dict(d = d):
    units = ["V", "A", "%", "Hz","sec","mA","°C","xVnm","deg","ms","cyc","min","kW","kVAR","kVA","MWhr","MVARh","MVAh","EU","kA","hour","xInm","Hz/s","VA","Hz/sec","xINOM"]
    for k in d:
        if k == '266':
            print(d[k])
        sublist = d[k][1].split(',')
        length = len(sublist)
        # if "Reservedc" in d[k][0]:
        #     device_net_param = sublist[-1]
        #     sublist = ['n/a'] + sublist + ['n/a'] + [device_net_param]
        #     length = 0 #invalidates logic 
        if length == 3:
            sublist = ['n/a'] + sublist + ['n/a']
        if length == 4:
            device_net_param = sublist[-1]
            sublist.pop(-1)
            sublist = ['n/a'] + sublist + ['n/a'] + [device_net_param]
        if length == 5:
            if sublist[0] in units:
                #means Units, Min, Max, Default, N/A, DeviceNet
                #where N/A would be Scale Factor
                device_net_param = sublist[-1]
                sublist.pop(-1)
                sublist.append('n/a')
                sublist.append(device_net_param)
            else:
                sublist = ['n/a'] + sublist
        d[k][1] = ','.join(sublist)
        if k == '266':
            print(d[k])
    return d

d = process_dict()
try:
    os.mkdir('SEL_csvs')
except FileExistsError:
    pass

def generate_CSVs(d=d):
    file_dict = {}
    known_lengths = []
    for k in d:
        length = len(d[k])
        addr = k
        label = d[k][0]
        header = "Address,Label,Units,Min,Max,Default,Scale Factor,DeviceNet Parameter Numbers"
        base_params = d[k][1]
        context_params = ''
        if length not in known_lengths:
            addendum = ','.join([f'p{i+1}' for i in range(0,len(d[k])-2)])
            if addendum == '':
                pass
            else:
                addendum  = ',' + addendum
                header += addendum
            header += '\n'
            file_dict[length] = open(f'SEL_csvs\\{length}.csv','w')
            file_dict[length].write(header)
            known_lengths.append(length)
        if length in known_lengths:
            if length > 2:
                context_params = ','.join(d[k][2:]).replace('\n', '')
            file_dict[length].write(f'{addr},{label},{base_params}{context_params}\n')
    for i in known_lengths:
        file_dict[i].close()

generate_CSVs(d)

table_context = {1: '?', 2: '?', 3: 'Min, Max, Default', 4: 'Min, Max, Default, DeviceNet', 
5: 'Min, Max, Default, Scale Factor, DeviceNet', 
6: 'Units, Min, Max, Default, Scale Factor, DeviceNet'}

f = open('SEL_csvs\\processed_text.txt','w')
for k in d:
    length = len(d[k][1].split(','))
    if length < 7:
        f.write(f'{k}: {d[k]} ({table_context[length]}) ({length})\n')
    else:
        f.write(f'{k}: {d[k]} LLAMA ({length})\n')
f.close()

'''
notes
2058 bugged
2000H-2110H bugged
4000H-4016H bugged
'''