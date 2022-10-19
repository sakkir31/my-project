import re

def vigenere(key, text, isencrypt, isauto):
    # Untuk Vigenere dengan 26 huruf alfabet
    # Huruf non-alfabet akan hilang saat dienkripsi
    # key       : kunci yang digunakan
    # text      : plainteks
    # isauto    : bernilai true jika merupakan auto-key vigenere
    # isencrypt : true jika mengenkripsi, false jika dekripsi

    # 1. Ambil hanya karakter alfabet dari input
    regex = re.compile('[^a-zA-Z]')
    plainteks = text
    kunci = key

    plainteks = regex.sub('', text).upper()
    kunci = regex.sub('', key).upper()
    hasil = ''

    # 2. Generate ciphertext
    counter = 1
    panjangkunci = len(kunci)

    if panjangkunci == 0:
        return ''
    
    for char in plainteks:
        # Encrypt
        if counter > panjangkunci:
            if isauto:
                # Gunakan plainteks sebagai kunci
                if isencrypt:
                    i = counter - panjangkunci - 1
                    hasil += geser(char,plainteks[i], isencrypt)
                else:
                    i = counter - panjangkunci - 1
                    hasil += geser(char,hasil[i], isencrypt)
                                 
            else:
                # Ulangi kunci jika habis
                i = counter % panjangkunci - 1
                hasil += geser(char,kunci[i],isencrypt)
        else:
            hasil += geser(char,kunci[counter-1], isencrypt)
                
        counter = counter + 1

    return hasil

def geser(char, key, enkripsi):
    # Input char dan key masing-masing 1 karakter uppercase
    # enkripsi: true jika untuk enkripsi, false jika dekripsi
    # Nilai A uppercase ASCII = 65:
    idxA = 65
        
    ordhasil = ord(char) - idxA
    if enkripsi:
        ordhasil = ordhasil + ord(key) - idxA
    else:
        ordhasil = ordhasil - (ord(key) - idxA)
        
    ordhasil = (ordhasil%26) + idxA
    
    return chr(ordhasil)

def vigenerebin(key, plain, isencrypt):
    if key == '':
        return ''

    counter = 1
    result = []
    keynum = []
    
    for x in key:
        keynum.append(ord(x))

    keylen = len(keynum)


    for num in plain:
        if isencrypt:
            result.append((num + keynum[counter%keylen-1]) % 256)
        else:
            result.append((num - keynum[counter%keylen-1]) % 256)
        counter += 1

    return result
