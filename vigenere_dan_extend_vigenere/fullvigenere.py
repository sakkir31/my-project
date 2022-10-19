import re

def fullvigenere(key, text, tabel, isencrypt):
    # Untuk Full Vigenere dengan 26 huruf alfabet
    # Huruf non-alfabet akan hilang saat dienkripsi
    # key       : kunci yang digunakan
    # text      : plainteks
    # tabel     : tabel kunci yang digunakan
    #             isi tabel dianggap sudah benar dan sesuai format
    # isencrypt : true jika mengenkripsi, false jika dekripsi

    if tabel=='':
        return ''

    # 1. Ambil hanya karakter alfabet dari input
    regex = re.compile('[^a-zA-Z]')
    plainteks = text
    kunci = key

    plainteks = regex.sub('', text).upper()
    kunci = regex.sub('', key).upper()
    hasil = ''
    splittabel = tabel.splitlines()
    panjangkunci = len(kunci)

    # 2. Generate ciphertext
    counter = 1
    if isencrypt:
        for char in plainteks:
            idxteks = ord(char) - 65
            idxkey = ord(kunci[counter%panjangkunci-1]) - 65
            
            hasil += splittabel[idxkey][idxteks]
            counter += 1
    else:
        for char in plainteks:
            idxkey = ord(kunci[counter%panjangkunci-1]) - 65
            idxcipher = splittabel[idxkey].find(char)            
            hasil += chr(idxcipher+65)
            counter += 1
    

    return hasil
        
        
