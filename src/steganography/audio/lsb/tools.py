# split array every n element
def split_array(seq, num):
    out = []
    last = 0

    while last < len(seq):
        out.append(seq[int(last):int(last + num)])
        last += num
    return out

def vigenere_extended(plain,key):
    result = ""

    key = key.upper()
    for c in range(0,len(plain)):
        if c>=len(key):
            key+=key[c-len(key)]
        result+=chr((ord(plain[c])+ord(key[c]))%256)
    
    return result

def vigenere_extended_decryption(encrypted,key):
    result = ""
    
    key = key.upper()
    for c in range(0,len(encrypted)):
        if c>=len(key):
            key+=key[c-len(key)]
        result+=chr((ord(encrypted[c])-ord(key[c]))%256)
    
    return result