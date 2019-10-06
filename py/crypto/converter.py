import re

hexmap = {
    'a': 10,
    'b': 11,
    'c': 12,
    'd': 13,
    'e': 14,
    'f': 15
}

inverse_hexmap = {
    10: 'a',
    11: 'b',
    12: 'c',
    13: 'd',
    14: 'e',
    15: 'f'
}

base64map = {
    0: 'A',
    1: 'B',
    2: 'C',
    3: 'D',
    4: 'E',
    5: 'F',
    6: 'G',
    7: 'H',
    8: 'I',
    9: 'J',
    10: 'K',
    11: 'L',
    12: 'M',
    13: 'N',
    14: 'O',
    15: 'P',
    16: 'Q',
    17: 'R',
    18: 'S',
    19: 'T',
    20: 'U',
    21: 'V',
    22: 'W',
    23: 'X',
    24: 'Y',
    25: 'Z',
    26: 'a',
    27: 'b',
    28: 'c',
    29: 'd',
    30: 'e',
    31: 'f',
    32: 'g',
    33: 'h',
    34: 'i',
    35: 'j',
    36: 'k',
    37: 'l',
    38: 'm',
    39: 'n',
    40: 'o',
    41: 'p',
    42: 'q',
    43: 'r',
    44: 's',
    45: 't',
    46: 'u',
    47: 'v',
    48: 'w',
    49: 'x',
    50: 'y',
    51: 'z',
    52: '0',
    53: '1',
    54: '2',
    55: '3',
    56: '4',
    57: '5',
    58: '6',
    59: '7',
    60: '8',
    61: '9',
    62: '+',
    63: '/'
}

base64_inverse_map = dict([(val, key) for key, val in base64map.items()])

def hex_to_value(ch):
    if (re.match('[0-9]', ch)):
        return int(ch)
    elif re.match('[a-fA-F]', ch):
        return hexmap.get(ch)
    else:
        return None

def value_to_hex(val):
    if val >= 0 and val <= 9:
        return str(val)
    elif val >= 10 and val <= 15:
        return inverse_hexmap.get(val)
    else:
        return None

def int_to_bin(val):
    binstr = ''
    while val > 0:
        if val % 2 == 0:
            binstr = '0' + binstr
        else:
            binstr = '1' + binstr
        val /= 2

    return binstr

def pad8(binstr):
    # Pad left to nearest multiple of 8
    length = len(binstr)
    remainder = length % 8
    diff = 8 - remainder
    binstr = binstr.rjust(length + diff, '0')

    return binstr

def pad6(binstr):
    return binstr.rjust(6, '0')

def hex_to_int(st):
    power = 0
    value = 0
    for i in range(len(st) - 1, -1, -1):
        ch = st[i]
        multiplier = hex_to_value(ch)
        value += multiplier * pow(16, power)
        power += 1

    return value

def bin_to_int(binstr):
    power = 0
    value = 0
    for i in range(len(binstr) - 1, -1, -1):
        ch = binstr[i]
        multiplier = 1 if ch == '1' else 0
        value += multiplier * pow(2, power)
        power += 1

    return value

def bin_to_base64(binstr):
    base64_str = ''
    while len(binstr) > 0:
        substr = binstr[:24]
        binstr = binstr[24:]
        if len(substr) < 24:
            substr = substr.ljust(24, '0')

        for i in range(0, len(substr), 6):
            sixstr = substr[i:i+6]
            intval = bin_to_int(sixstr)
            base64_str += base64map[intval]

    return base64_str

def bin_to_hex(binstr):
    hexstr = ''
    while len(binstr) > 0:
        substr = binstr[0:4]
        binstr = binstr[4:]
        intval = bin_to_int(substr)
        hexval = value_to_hex(intval)
        hexstr += hexval

    return hexstr

def hex_to_bin(hexstr):
    val = hex_to_int(hexstr)
    binstr = pad8(int_to_bin(val))
    return binstr

def hex_to_base64(hexstr):
    val = hex_to_int(hexstr)
    binstr = pad8(int_to_bin(val))
    base64_str = bin_to_base64(binstr)
    return base64_str

def ascii_to_bin(ch):
    val = ord(ch)
    return pad8(int_to_bin(val))

def str_to_bin(st):
    binstr = ''
    for ch in st:
        binstr += ascii_to_bin(ch)

    return binstr

def bin_to_ascii(binstr):
    chrstr = ''
    while len(binstr) > 0:
        substr = binstr[0:8]
        binstr = binstr[8:]
        val = bin_to_int(substr)
        ch = chr(val)
        chrstr += ch

    return chrstr

def hex_to_ascii(hexstr):
    binstr = hex_to_bin(hexstr)
    chrstr = bin_to_ascii(binstr)
    return chrstr

def base64_chr_to_val(ch):
    val = None
    # Accounts for padding
    if ch == '=':
        val = 0
    else:
        val = int(base64_inverse_map.get(ch))

    return val

def base64_val_to_bin(val):
    return pad6(int_to_bin(val))

def base64_to_ascii(base64_str):
    binstr = base64_to_bin(base64_str)
    chrstr = bin_to_ascii(binstr)
    return chrstr

def base64_to_bin(base64_str):
    binstr = ''
    for ch in base64_str:
        binstr += base64_val_to_bin(base64_chr_to_val(ch))

    return binstr

if __name__ == "__main__":
    hexstr = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
    base64res = "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"
    base64_str = hex_to_base64(hexstr)
    print "hex: {}".format(hexstr)
    print "base64: {}".format(base64_str)
    base64_bin = base64_to_bin(base64res)
    hex_bin = hex_to_bin(hexstr)
    assert(base64_bin == hex_bin)
    assert(base64_to_ascii(base64res) == hex_to_ascii(hexstr))

    assert(base64_str == base64res)
