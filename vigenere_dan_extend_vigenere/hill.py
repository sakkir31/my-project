import numpy as np
from sympy import Matrix
import re


def hill(teks, matriks, isencrypt):
    #Enkripsi Hill Cipher
    #Matriks diasumsikan benar
    #Jika huruf kurang, ditambah huruf A di belakangnya
    matriksarr = tekstomatriks(matriks)
    K = np.array(matriksarr)
    
    if not isencrypt:
        KM = Matrix(K)
        KM = KM.inv_mod(26)
        K = np.array(KM.tolist())
        
    n = len(matriksarr)
    regex = re.compile('[^a-zA-Z]')
    plainteks = regex.sub('', teks).upper()
    plainteks = [plainteks[i:i+n] for i in range(0, len(plainteks), n)]

    plainnum = []
    result = []
    
    for x in plainteks:
        plainnum.append(wordtoarr(x))

    for x in plainnum:
        A = np.array(x)
        result.append(K.dot(A).tolist())

    for i in range(len(result)):
        for j in range(len(result[i])):
            result[i][j] %= 26
            
    cipher = ''
    for x in result:
        cipher += arrtoword(x)
        
    return cipher
    
    

def tekstomatriks(matriks):
    splitmatriks = matriks.splitlines()
    matriksarr = []
    for m in splitmatriks:
        el =  list(map(int, m.split()))
        matriksarr.append(el)
    return matriksarr

def wordtoarr(word):
    #word is uppercase
    arr = []
    for a in word:
        arr.append(ord(a)-65)
    p = len(word)
    while p < 3:
        arr.append(0)
        p += 1
        
    return arr

def arrtoword(arr):
    word = ''
    for x in arr:
        word += chr(x+65)

    return word
