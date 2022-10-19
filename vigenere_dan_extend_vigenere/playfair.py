import re
from typing import Tuple

def __playfair_square(key: str) -> list:
  """ Membentuk "bujursangkar" playfair dari kunci yang diberikan """
  key_unique = list(dict.fromkeys(re.sub(r'(?:[^a-zA-Z]|j)', '', ''.join(key.lower().split())))) # hapus huruf duplikat dan huruf j
  for c in range(26): # iterasi semua huruf dalam alfabet
    if ord('a')+c != ord('j') and chr(ord('a')+c) not in key_unique: # apabila huruf belum ada dalam key dan bukan j
      key_unique += chr(ord('a')+c) # tambahkan huruf ke key
  return key_unique

def __playfair_coords_to_linear(row: int, col: int) -> int:
  """ Menghitung index dalam "bujursangkar" playfair, diberikan baris dan kolom """
  return row*5+col

def __playfair_linear_to_coords(line: int) -> Tuple[int, int]:
  """ Mencari baris dan kolom dari bujursangkar playfair, diberikan indeks linearnya """
  return (line//5, line%5)

def __playfair_shift(bigram: str, playfair_square: list, encrypt: bool) -> str:
  """ "Menggeser" bigram dalam bujursangkar playfair, untuk mencipher atau mendecipher pesan

  ---
  `bigram`: bigram yang akan digeser, berupa str berisi dua huruf  
  `playfair_square`: "bujursangkar" playfair, berupa list linear  
  `encrypt`: `True` untuk mencipher (geser ke kanan/bawah),
    `False` untuk mendecipher (geser ke kiri/atas)
  """
  firstRow, firstCol = __playfair_linear_to_coords(playfair_square.index(bigram[0]))
  secondRow, secondCol = __playfair_linear_to_coords(playfair_square.index(bigram[1]))
  shift = 1 if encrypt else -1
  if firstCol == secondCol:
    # kolomnya sama
    firstCipher = __playfair_coords_to_linear((firstRow+shift)%5, firstCol)
    secondCipher = __playfair_coords_to_linear((secondRow+shift)%5, secondCol)
  elif firstRow == secondRow:
    # barisnya sama
    firstCipher = __playfair_coords_to_linear(firstRow, (firstCol+shift)%5)
    secondCipher = __playfair_coords_to_linear(secondRow, (secondCol+shift)%5)
  else:
    # tidak berada dalam baris atau kolom yang sama
    firstCipher = __playfair_coords_to_linear(firstRow, secondCol)
    secondCipher = __playfair_coords_to_linear(secondRow, firstCol)
  return playfair_square[firstCipher] + playfair_square[secondCipher]

def playfair_cipher(plaintext: str, key: str) -> str:
  """Melakukan Playfair Cipher terhadap plaintext dengan key

  Lebih spesifik, fungsi ini akan membuat matriks lookup untuk cipher playfair
  menggunakan key yang diberikan, kemudian menggunakan matriks tersebut
  untuk melakukan cipher. Apabila ada dua huruf yang sama dalam satu bigram,
  maka algoritma akan mencoba menyisipkan `x` di tengahnya. Apabila bigram yang
  terbentuk adalah `xx`, maka algoritma akan mengganti `x` yang disisipkan
  dengan `z`.

  ---
  `plaintext`: pesan yang akan dienkripsi  
  `key`: kunci yang akan digunakan 
  """
  playfair_square = __playfair_square(key)
  # siapkan plaintext
  # hapus huruf j dan whitespace
  safe_plaintext = re.sub(r'(?:[^a-z]|j)', '', ''.join(plaintext.lower().split()))
  # buat bigram
  bigrams = []
  n = len(safe_plaintext)
  i = 0
  while i < n:
    firstPair = safe_plaintext[i]
    if i+1 == n:
      secondPair = 'x' # apabila huruf terakhir sendiri, tambah x
    else:
      secondPair = safe_plaintext[i+1]
    if firstPair == secondPair: # tidak boleh ada pasangan huruf yang sama
      if firstPair != 'x':
        secondPair = 'x'
      else:
        secondPair = 'z'
      i -= 1 # karena di akhir akan dilompati 1 huruf, maka mundur dulu 1 huruf
    bigrams.append(firstPair+secondPair)
    i += 2 # lompati huruf pasangan
  
  # lakukan cipher dengan aturan Playfair
  cipherText = ''
  for bigram in bigrams:
    cipherText += __playfair_shift(bigram, playfair_square, True)
  return cipherText

def playfair_decipher(ciphertext: str, key: str) -> str:
  """Melakukan decipher dari ciphertext yang dihasilkan oleh algoritma playfair

  Lebih spesifik, karena keterbatasan yang ada, algoritma tidak dapat menghapus
  `x` yang tidak bermakna, karena hal tersebut bersifat kontekstual.

  ---
  `ciphertext`: ciphertext yang akan didecipher  
  `key`: kunci yang digunakan
  """
  safe_ciphertext = re.sub(r'[^a-z]', '', ''.join(ciphertext.lower().split()))
  playfair_square = __playfair_square(key)
  bigrams = [safe_ciphertext[i:i+2] for i in range(0, len(safe_ciphertext), 2)]
  plainText = ''
  for bigram in bigrams:
    plainText += __playfair_shift(bigram, playfair_square, False)
  return plainText 