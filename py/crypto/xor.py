from converter import (
    hex_to_base64,
    hex_to_bin,
    bin_to_hex
)

def xor_bin(binstr1, binstr2):
    frm = len(binstr1) - 1
    restr = ''
    for i in range(frm, -1, -1):
        v1 = binstr1[i]
        v2 = binstr2[i]
        if v1 == '1':
            if v2 == '0':
                restr = '1' + restr
            else:
                restr = '0' + restr
        elif v2 == '1':
            if v1 == '0':
                restr = '1' + restr
            else:
                restr = '0' + restr
        else:
            restr = '0' + restr

    return restr

def xor_hex(hexstr1, hexstr2):
    binstr1 = hex_to_bin(hexstr1)
    binstr2 = hex_to_bin(hexstr2)
    binstr3 = xor_bin(binstr1, binstr2)

    hexstr = bin_to_hex(binstr3)

    return hexstr

if __name__ == "__main__":
    hexstr1 = '1c0111001f010100061a024b53535009181c'
    hexstr2 = '686974207468652062756c6c277320657965'
    hexstr3 = '746865206b696420646f6e277420706c6179'

    hexstr4 = xor_hex(hexstr1, hexstr2)
    print "hex: {}".format(hexstr4)
    assert(hexstr3 == hexstr4)
