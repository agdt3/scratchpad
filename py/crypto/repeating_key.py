from converter import (
    str_to_bin,
    ascii_to_bin,
    bin_to_hex
)

from xor import xor_bin

# Assumes that total_length % 8 == 0
def generate_repeating_binstr(keystr, total_length):
    repeating_bin_str = ''
    index = 0
    for i in range(0, total_length, 8):
        if index == len(keystr):
            index = 0

        binstr = ascii_to_bin(keystr[index])
        # ICEICEICE and not ECIECIECI, etc
        repeating_bin_str = repeating_bin_str + binstr

        index += 1

    return repeating_bin_str

def encrypt_repeating(message, keystr):
    bin_message = str_to_bin(message.strip())
    bin_key = generate_repeating_binstr(keystr, len(bin_message))
    encrypted_bin_message = xor_bin(bin_message, bin_key)
    encrypted_hex_message = bin_to_hex(encrypted_bin_message)

    return encrypted_hex_message

if __name__ == '__main__':
    message = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
    keystr = 'ICE'
    expected_message = '''0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f'''

    encrypted_message = encrypt_repeating(message, keystr)
    assert(encrypted_message == expected_message)
