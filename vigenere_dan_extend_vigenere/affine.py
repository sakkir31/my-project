def __euclid_gcd(a: int, b: int) -> int:
  if b == 0: return a
  elif a < b: return __euclid_gcd(b, a)
  else:
    return __euclid_gcd(b, a % b)

def __extended_euclid(a: int, m: int) -> int:
  """Menghitung balikan modulo a dalam m"""
  u = a
  v = m
  x1 = 1
  x2 = 0
  while u != 1:
    q = v//u
    r = v%u
    x = x2-(q*x1)
    v = u
    u = r
    x2 = x1
    x1 = x
  return x1 % m

n = 26 # ukuran alfabet untuk Affine Cipher
def affine_cipher(plaintext: str, m: int, b: int) -> str:
  if __euclid_gcd(m, n) != 1:
    return ''
  safe_plaintext = [ord(P) - ord('a') for P in ''.join(plaintext.lower().split())]
  return ''.join(
    [
      chr(((m*P+b)%n)+ord('a'))
        for P in safe_plaintext 
        if (0 <= P and P <= 26)
    ]
  )

def affine_decipher(ciphertext: str, m: int, b: int) -> str:
  if __euclid_gcd(m, n) != 1:
    return ''
  m_inv = __extended_euclid(m, n)
  safe_ciphertext = [ord(P) - ord('a') for P in ''.join(ciphertext.lower().split())]
  return ''.join(
    [
      chr(((m_inv*(P-b))%n)+ord('a'))
        for P in safe_ciphertext
        if (0 <= P and P <= 26)
    ]
  )