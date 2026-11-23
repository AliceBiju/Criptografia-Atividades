from math import gcd
from typing import Tuple, Dict
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes


def preparar(p: int, q: int, e: int) -> Tuple[int, int]:
    """Prepara os parâmetros RSA didáticos (n, d)."""
    if p <= 1 or q <= 1 or p == q:
        raise ValueError("p e q devem ser primos distintos maiores que 1")
    
    phi = (p - 1) * (q - 1)
    if gcd(e, phi) != 1:
        raise ValueError(f"O expoente e={e} não é coprimo com phi(n)={phi}")
        
    d = pow(e, -1, phi)
    n = p * q
    return n, d


def transformar(m: int, expoente: int, n: int) -> int:
    """Aplica a operação RSA bruta: pow(m, expoente, n)."""
    if not (0 <= m < n):
        raise ValueError(f"m={m} fora do intervalo [0, {n - 1}]")
    return pow(m, expoente, n)


def demonstrar_maleabilidade_rsa_bruto(p: int = 7, q: int = 13, e: int = 5, m: int = 9, r: int = 2) -> Dict:
    n, d = preparar(p, q, e)
    c = transformar(m, e, n)
    fator_publico = transformar(r, e, n)
    c_alterado = (c * fator_publico) % n
    m_decifrado_alterado = transformar(c_alterado, d, n)
    m_esperado = (m * r) % n
    assert m_decifrado_alterado == m_esperado
    
    return {
        "m": m,
        "r": r,
        "c": c,
        "c_alterado": c_alterado,
        "m_decifrado_alterado": m_decifrado_alterado,
        "m_esperado": m_esperado
    }


def demonstrar_rsa_biblioteca() -> Dict:
    chave_cifracao = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    pub_cifracao = chave_cifracao.public_key()

    padding_oaep = padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
    
    msg = b"pedido=7"
    cifra1 = pub_cifracao.encrypt(msg, padding_oaep)
    cifra2 = pub_cifracao.encrypt(msg, padding_oaep)
    assert len(cifra1) == 256
    assert cifra1 != cifra2
    assert chave_cifracao.decrypt(cifra1, padding_oaep) == msg

    # Capacidade máxima: 256 - 64 - 2 = 190 bytes
    cifra_190 = pub_cifracao.encrypt(b"A" * 190, padding_oaep)
    assert len(cifra_190) == 256
    
    excedeu = False
    try:
        pub_cifracao.encrypt(b"A" * 191, padding_oaep)
    except ValueError:
        excedeu = True
    assert excedeu

    # Assinatura PSS
    chave_assinatura = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    pub_assinatura = chave_assinatura.public_key()
    padding_pss = padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=32)
    
    assinatura = chave_assinatura.sign(msg, padding_pss, hashes.SHA256())
    pub_assinatura.verify(assinatura, msg, padding_pss, hashes.SHA256())

    invalida = False
    try:
        pub_assinatura.verify(assinatura, b"pedido=8", padding_pss, hashes.SHA256())
    except InvalidSignature:
        invalida = True
    assert invalida

    return {
        "capacidade_190_ok": True,
        "excedeu_191_rejeitado": excedeu,
        "assinatura_verificada": True,
        "adulteracao_detectada": invalida
    }
