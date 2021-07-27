from rsa import common, core, transform, newkeys, PrivateKey
import os

def _pad_for_encryption(message, target_length):

    max_msglength = target_length - 11
    msglength = len(message)

    if msglength > max_msglength:
        raise OverflowError('%i байт нужно для сообщения, но есть только'
                            ' место для %i' % (msglength, max_msglength))

    padding = b''
    padding_length = target_length - msglength - 3

    while len(padding) < padding_length:
        needed_bytes = padding_length - len(padding)

        new_padding = os.urandom(needed_bytes + 5)
        new_padding = new_padding.replace(b'\x00', b'')
        padding = padding + new_padding[:needed_bytes]

    assert len(padding) == padding_length

    return b''.join([b'\x00\x02',
                     padding,
                     b'\x00',
                     message])

def encrypt(message, pub_key):
    message = message.encode()
    keylength = common.byte_size(pub_key.n)
    padded = _pad_for_encryption(message, keylength)
    payload = transform.bytes2int(padded)
    encrypted = core.encrypt_int(payload, pub_key.e, pub_key.n)
    block = transform.int2bytes(encrypted, keylength)
    return block.hex()

def decrypt(crypto, priv_key):
    crypto = bytes.fromhex(crypto)
    blocksize = common.byte_size(priv_key.n)
    encrypted = transform.bytes2int(crypto)
    decrypted = priv_key.blinded_decrypt(encrypted)
    cleartext = transform.int2bytes(decrypted, blocksize)

    if cleartext[0:2] != b'\x00\x02':
        raise DecryptionError('Ошибка расшифровки')

    try:
        sep_idx = cleartext.index(b'\x00', 2)
    except ValueError:
        raise DecryptionError('Ошибка расшифровки')

    return cleartext[sep_idx + 1:].decode()

"""
(pubkey, privkey) = newkeys(82 + 126*8) #Стартовое число 82. На каждую букву в тексте нужно увеличивать это число на 8
print(pubkey)
print(privkey)
name = 'readme.txt'

with open (name, 'r') as f:
    default_data = f.read()
    print(len(default_data))
    print(default_data)
    crypto_data = encrypt(default_data, pubkey)
    print(crypto_data)

    with open (name, 'w') as f:
        f.write(crypto_data)
    with open ('keys.txt', 'w') as f:
        f.write('adsadas')

with open (name, 'r') as f:
    default_data = f.read()
    print(default_data)
    crypto_data = decrypt(default_data, privkey)
    print(crypto_data)
"""