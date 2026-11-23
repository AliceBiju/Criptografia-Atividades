from typing import Tuple, Dict

P = 23
Q = 11
G = 2


def validar(y) -> bool:
    """Valida se y pertence ao subgrupo permitido de ordem Q=11."""
    if type(y) is not int:
        return False
    if not (2 <= y <= P - 2):
        return False
    return pow(y, Q, P) == 1


def validar_privada(chave) -> bool:
    if type(chave) is not int:
        return False
    return 1 <= chave <= (Q - 1)


def acordo_auditado(a: int, b: int) -> Tuple[int, int, int, int]:
    if not validar_privada(a):
        raise ValueError(f"Chave privada 'a' inválida: {a}")
    if not validar_privada(b):
        raise ValueError(f"Chave privada 'b' inválida: {b}")

    A = pow(G, a, P)
    B = pow(G, b, P)

    if not validar(A):
        raise ValueError(f"Chave pública A={A} inválida")
    if not validar(B):
        raise ValueError(f"Chave pública B={B} inválida")

    s_alice = pow(B, a, P)
    s_bob = pow(A, b, P)
    return A, B, s_alice, s_bob


def simular_ataque_mallory_encontro12() -> Dict:
    a, b = 2, 5
    A = pow(G, a, P)
    B = pow(G, b, P)

    u, v = 1, 2
    U = pow(G, u, P)
    V = pow(G, v, P)

    assert validar(U) is True
    assert validar(V) is True

    s_alice = pow(U, a, P)
    s_mallory_alice = pow(A, u, P)
    assert s_alice == s_mallory_alice

    s_bob = pow(V, b, P)
    s_mallory_bob = pow(B, v, P)
    assert s_bob == s_mallory_bob

    return {
        "U_valido": validar(U),
        "V_valido": validar(V),
        "s_alice_mallory": s_alice,
        "s_bob_mallory": s_bob,
        "segredos_iguais_original": s_alice == 12 and s_bob == 12
    }


def elgamal_cifrar(m: int, y: int, k: int) -> Tuple[int, int]:
    c1 = pow(G, k, P)
    mascara = pow(y, k, P)
    c2 = (m * mascara) % P
    return c1, c2


def elgamal_decifrar(c1: int, c2: int, x: int) -> int:
    mascara = pow(c1, x, P)
    inverso_mascara = pow(mascara, -1, P)
    return (c2 * inverso_mascara) % P
