from datetime import datetime
import sys
import os

def generate_timestamp():
    now = datetime.utcnow()
    unix_now = datetime.timestamp(now)*1000
    return unix_now

#https://www.delftstack.com/howto/python/python-find-all-indexes-of-a-character-in-string/
def convert_key_toCamelCase(key):
    s = ''
    s += key[0].lower()
    rest_of_string = key[1:]
    if '(' in rest_of_string:
        start = rest_of_string.find('(')
        end = rest_of_string.find(')')
        parenthesis_encl_string = rest_of_string[start:end+1].replace('(','').replace(')','')
        l = parenthesis_encl_string.split(' ')
        s2 = ''
        for i in l:
            s2+=i.capitalize()
        s3 = rest_of_string[0:start] + s2 + rest_of_string[end:]
        s += s3
    else:
        s+=rest_of_string
    s = s.replace(' ','').replace(')','').replace('(','').replace('-','')
    return s


def camelCase_keys(d):
    new_d = {}
    for key in d.keys():
        new_d[convert_key_toCamelCase(key)] = d[key]
    return new_d

def test_CamelCaseConverter(keys):
    for key in keys:
        try:
            # print(key, '{', convert_key_toCamelCase(key), '}')
            print(convert_key_toCamelCase(key))
        except TypeError:
            print(key)

def fetch_temperature():
    if sys.platform == 'linux':
        if os.uname()[1] == 'raspberrypi':
            temperature = subprocess.run(['vcgencmd', 'measure_temp'], stdout=subprocess.PIPE).stdout.decode('utf-8')
            return float(temperature.replace('temp=','').replace("'C",''))
        else:
            temperature = subprocess.run(['sensors'], stdout=subprocess.PIPE).stdout.decode('utf-8')
            return "Not implemented on generic Linux"
    else:
        new_d['cpuTempC'] = "Not implemented on Windows"