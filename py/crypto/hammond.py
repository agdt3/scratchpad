from converter import (
        hex_to_bin,
        str_to_bin
)

def hammond_distance(binstr1, binstr2):
    l1 = len(binstr1)
    l2 = len(binstr2)

    diff = abs(l1 - l2)
    dist = 0

    min_len = l1
    if l2 < l1:
        min_len = l2

    # Leftmost to rightmost differences
    for i in range(0, min_len):
        ch1 = binstr1[i]
        ch2 = binstr2[i]
        if ch1 != ch2:
            dist += 1

    return dist + diff

if __name__ == '__main__':
    hexstr1 = 'this is a test'
    hexstr2 = 'wokka wokka!!!'
    expected_dist = 37
    binstr1 = str_to_bin(hexstr1)
    binstr2 = str_to_bin(hexstr2)
    dist = hammond_distance(binstr1, binstr2)
    assert(dist == expected_dist)
