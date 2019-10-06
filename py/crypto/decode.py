import re

from converter import (
    hex_to_bin,
    bin_to_ascii,
    hex_to_ascii,
    bin_to_hex,
)

from xor import xor_bin

def repeating(charslist, repeats):
    repeating_chars = []
    for chars in charslist:
        repeating_chars.extend([chars * repeats])
    return repeating_chars

def generate_single_keys():
    return permutations([], 0, 128)

def permutations(binstrs, index, num):
    if len(binstrs) == num:
        return binstrs
    elif index > 0:
        previous = pow(2, index)
        new_combinations = []
        for binstr in binstrs:
            combo = binstr[:8 - index - 1] + '1' + binstr[8 - index:]
            new_combinations.extend([combo])
        binstrs.extend(new_combinations)
        return permutations(binstrs, index + 1, num)
    else:
        binstrs = ['00000000', '00000001']
        return permutations(binstrs, index + 1, num)

def xor_keys(binstr, keys):
    messages = []
    for key in keys:
        binstr2 = xor_bin(binstr, key)
        messages.extend([binstr2])
    return messages

def xor_keys_all(binstr, keys):
    messages = {}
    for key in keys:
        binstr2 = xor_bin(binstr, key)
        messages[key] = binstr2
    return messages

def calculate_frequency(key_msg_dict):
    messages = {}
    for k, v in key_msg_dict.items():
        msg = bin_to_ascii(v)
        messages[k] = {
            'msg': msg,
            'frequency': char_frequency(msg)
        }

    return messages

def convert_to_ascii(binlist):
    messages = []
    for binstr in binlist:
        message = bin_to_ascii(binstr)
        messages.extend([message])

    return messages

def char_frequency(ascii_str):
    patt = re.compile('[a-zA-Z]')
    res = re.findall(patt, ascii_str)
    return len(res)

def filter_max_frequency(ascii_str_list):
    current_max = 0
    best_match = ''
    for ascii_str in ascii_str_list:
        new_max = char_frequency(ascii_str)
        if new_max > current_max:
            current_max = new_max
            best_match = ascii_str

    return (best_match, current_max)

def filter_max_frequency_multi(ascii_str_list):
    best_matches = {}
    for ascii_str in ascii_str_list:
        new_max = char_frequency(ascii_str)
        keys = best_matches.keys()
        if len(keys) > 0:
            current_max = best_matches.get(keys[0])
        else:
            current_max = 0
        if new_max > current_max:
            best_matches = {}
            best_matches[ascii_str] = new_max
        elif new_max == current_max:
            best_matches[ascii_str] = new_max

    return best_matches

def filter_max_frequency_keys(key_msg_freq_dict):
    best_matches = {}
    max_frequency = 0
    for k, v in key_msg_freq_dict.items():
        current_frequency = v['frequency']
        if current_frequency > max_frequency:
            best_matches = {}
            best_matches[k] = v
            max_frequency = current_frequency
        elif current_frequency == max_frequency:
            best_matches[k] = v

    return best_matches

def find_keys_by_frequency(binstr):
    charslist = generate_single_keys()
    total_len = len(binstr)
    repeats = total_len / 8
    repeating_charslist = repeating(charslist, repeats)
    key_msg_dict = xor_keys_all(binstr, repeating_charslist)
    key_msg_freq_dict = calculate_frequency(key_msg_dict)
    return filter_max_frequency_keys(key_msg_freq_dict)

# TODO: Inefficient but clean
def decode_bin(binstr):
    charslist = generate_single_keys()
    total_len = len(binstr)
    repeats = total_len / 8
    repeating_charslist = repeating(charslist, repeats)
    potential_results = xor_keys(binstr, repeating_charslist)
    potential_messages = convert_to_ascii(potential_results)
    return filter_max_frequency(potential_messages)


if __name__ == '__main__':
    hexstr = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
    binstr = hex_to_bin(hexstr)
    message, freq = decode_bin(binstr)
    print "message: {}".format(message)
