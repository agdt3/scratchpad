from converter import (
    base64_to_bin,
    bin_to_ascii
)

from hammond import (
    hammond_distance
)

from decode import (
    generate_single_keys,
    decode_bin,
    find_keys_by_frequency
)

from xor import xor_bin

def find_keysize(low, high, binstr):
    min_dist = None
    best_keysize = None
    for keysize in range(low, high):
        bytes1 = binstr[0:keysize * 8]
        bytes2 = binstr[keysize * 8:keysize * 8 * 2]
        dist = float(hammond_distance(bytes1, bytes2)) / float(keysize)
        if min_dist is None or dist < min_dist:
            min_dist = dist
            best_keysize = keysize

    return best_keysize

def readfile(filepath):
    base64_message = ''
    with open(filepath, 'r') as f:
        for line in f:
            base64_message += line.strip()

    return base64_message

def transpose_blocks(binstr, blocksize, pos):
    '''
    Lines up nth character in each block of blocksize
    and turns them into a single binstr
    Note: assumes binstr is padded so that binstr % blocksize == 0
    '''
    blocks = len(binstr) / blocksize
    transposed_binstr = ''
    for block in range(0, blocks):
        start = block * blocksize + pos * 8
        end = start + 8
        transposed_binstr += binstr[start:end]

    return transposed_binstr

def iterate_blocks(binstr, blocksize):

    transposed_binstr = ''
    num_pos = len(binstr) / blocksize / 8
    for pos in range(0, num_pos):
        transposed_binstr += transpose_blocks(binstr, blocksize, pos)

    return transposed_binstr

def decrypt_repeating_key(base64_str):
    binstr = base64_to_bin(base64_str)
    keysize = find_keysize(2, 40, binstr)
    key_permutations = generate_single_keys()
    blocksize = keysize * 8
    #transposed_binstr = transpose_blocks(binstr, blocksize)
    print iterate_blocks(binstr, blocksize)
    #find_keys_by_frequency(transposed_binstr)

if __name__ == '__main__':
    base64_str = readfile('files/6.txt')
    decrypt_repeating_key(base64_str)
