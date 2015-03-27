from humod import at_commands as atc
from humod.GSM0338 import gsm0338_mapping
from datetime import datetime

seq = lambda p, s=2: [p[i*s:(i+1)*s] for i in range(int((len(p)+1)/s))]
digits_only = lambda s: ''.join([x for x in s if x.isdigit()])

def format_no(no):
    n = digits_only(str(no))
    if n:
        return n[:-6]+' '+n[-6:-3]+' '+n[-3:]
    return no # Voicemail, T-Mobile, hidden caller ID

def show_imsi(modem):
    '''Show IMSI (SIM) number.'''
    return atc._common_run(modem, '+CIMI', prefixed=False)[0]

def show_phone_no(modem):
    out = atc._common_run(modem, '+CNUM', prefixed=True)
    try:
        return out[0].replace('"','').split(',')[1]
    except IndexError:
        return ''

def show_operator(modem):
    out = atc._common_run(modem, '+COPS?', prefixed=False)[0]
    data = atc._enlist_data(out.split(': '))
    try:
        return data[1][2] # operator
    except IndexError:
        return ''

def system_info(modem):
    """
    Voice (CS, circuit switched): equivalent to dialup data,
        dial a number and the data flows like in a voice call
    Packet (PS, packet switched): packets of data transmitted
        by GPRS or 3G
    """
    key = [
    ('Service', {
        0: 'No service',
        1: 'Restricted service',
        2: 'Valid service',
        3: 'Restricted regional service',
        4: 'Power-saving and deep sleep state'
        }),
    ('Type', {
        0: 'No service',
        1: 'Voice service only',
        2: 'Packet service only',
        3: 'Packet+Voice service',
        4: 'Voice and packet service not registered, searching'
        }),
    ('Roaming', {
        0: 'Not now',
        1: 'Enabled'
        }),
    ('Mode', {
        0: 'No service',
        1: 'AMPS', # currently
        2: 'CDMA', # not in use 
        3: 'GSM/GPRS',
        4: 'HDR',
        5: 'WCDMA',
        6: 'GPS'
        }),
    ('SIM card state', {
        0: 'Invalid / pin code locked',
        1: 'Valid',
        2: 'Invalid for voice service',
        3: 'Invalid for packet service',
        4: 'Invalid for voice and packet service',
        255: 'SIM card is not existent'
        })
    ]
    
    info = atc._common_run(modem, '^SYSINFO', prefixed=False)[0]
    info = info.replace('^SYSINFO:','').split(',')
    keys = [x for x, y in key]
    out = {}
    for k,v in zip(keys, info):
        out[k] = dict(key)[k][int(v)]
    return out

def is_gsm_encoded(message):
    for x in message:
        if x not in '0123456789ABCDEF':
            return False
    return True

def decode_gsm(message):
    """ Tiny naive translation. For a proper codec try:
    https://github.com/dsch/gsm0338"""
    key = {a[2:]: chr(int(b, 0)) for a,b in gsm0338_mapping.items()}
    done = ''.join([key.get(x, '') for x in seq(message)])
    return done.replace('@', '')

def convert_dtime(d):
    return datetime.strptime(d.split('+')[0], '%y/%m/%d,%H:%M:%S')

BOXES = {
    'inbox': 'ALL',
    'outbox': 'STO UNSENT',
    'sent': 'STO SENT'
}
    
def full_sms_list(modem, box):
    box = BOXES[box]
    ls = []
    if modem: ls = modem.sms_list(box)
    texts = {}
    for l in ls:
        try: id, typ, no, empty, at = l
        # TODO: interpret the SMS concatenation headers n1-4
        except ValueError: id, typ, n1, n2, no, n3, at, at1, n4 = l
        txt = modem.sms_read(id)
        gsm_encoded = is_gsm_encoded(txt)
        multipart = False
        try: multipart = msg['no'] == format_no(no)
        except NameError: pass
        if gsm_encoded or multipart:
            txt = decode_gsm(txt) if gsm_encoded else txt
            if multipart:
                prev = texts[msg['id']]
                prev['txt'] = prev['txt'] + txt
                continue
        texts[id] = msg = {
            'id': id,
            'typ': typ.replace('STO ','').replace('REC ', '').lower(),
            'no': format_no(no),
            'txt': txt,
            'at': convert_dtime(at)
        }
    if texts:
        texts = sorted(texts.items(), key=lambda m: m[1]['at'], reverse=True)
        texts = [y for x,y in texts]
    return texts