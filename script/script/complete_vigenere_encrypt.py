import re

plain_text = 'thisplaintextz'
key = 'sony'
print(plain_text)
print(key)

def generate_table_random() :
    import random
    import string
    import numpy as np
    list_random = []
    for index in range (0,26) :
        my_randoms = random.sample(string.ascii_uppercase, 26)
        list_random.append(my_randoms)
    return(np.array(list_random))

def full_vigenere_encrypt(plain_text, key) :
    table = generate_table_random()
    base  = ord('a')
    key_idx = 0
    crypt_text = ''
    plain_text = plain_text.lower()
    key = key + plain_text
    for word in plain_text :
        if (word.isalpha()) :
            crypt_word = table[ord(key[key_idx]) - base][ord(word) - base]
            key_idx = (key_idx + 1) % len(key)
        else :
            crypt_word = word
        crypt_text = crypt_text + crypt_word
    return (crypt_text.upper(), table)
crypt_text, table = full_vigenere_encrypt(plain_text, key)
print(crypt_text)