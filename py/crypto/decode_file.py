from decode import decode_bin

from converter import (
    hex_to_bin,
)


def decode_file(filepath):
    max_frequency = 0
    candidates = []
    with open(filepath, 'r') as f:
        for hexstr in f:
            binstr = hex_to_bin(hexstr.strip())
            message, frequency = decode_bin(binstr)
            if frequency > max_frequency:
                max_frequency = frequency
                candidates.append({
                    'message': message,
                    'frequency': frequency
                    })

    return candidates


if __name__ == '__main__':
    filepath = './files/4.txt'
    candidates = decode_file(filepath)
    for candidate in candidates:
        print candidate.get('message'), candidate.get('frequency')
