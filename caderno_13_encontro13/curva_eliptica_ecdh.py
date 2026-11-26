from typing import Optional, Tuple, Dict, List

# Parâmetros da curva elíptica didática E: y^2 = x^3 + 2x + 2 (mod 17)
P_MOD = 17
A_CURVA = 2
B_CURVA = 2

# Ponto-base e ordem
PONTO_G = (5, 1)
ORDEM_G = 19


def na_curva(ponto: Optional[Tuple[int, int]]) -> bool:
    """Verifica se um par (x, y) ou o ponto no infinito (None) pertence à curva E."""
    if ponto is None:
        return True
    x, y = ponto
    if not (0 <= x < P_MOD and 0 <= y < P_MOD):
        return False
    lado_esquerdo = (y * y) % P_MOD
    lado_direito = (x * x * x + A_CURVA * x + B_CURVA) % P_MOD
    return lado_esquerdo == lado_direito


def inverso(x: int) -> int:
    """Calcula o inverso multiplicativo de x módulo P_MOD."""
    return pow(x % P_MOD, -1, P_MOD)


def somar(ponto_p: Optional[Tuple[int, int]], ponto_q: Optional[Tuple[int, int]]) -> Optional[Tuple[int, int]]:
    """Calcula a soma de pontos P + Q na curva elíptica E módulo 17.
    
    Casos tratados:
    1. Elemento neutro (None): P + O = P e O + Q = Q.
    2. Pontos opostos: xp == xq e (yp + yq) % 17 == 0 -> retorna None (O).
    3. Duplicação de ponto (P == Q): lam = (3*xp^2 + a) * (2*yp)^(-1) mod 17.
    4. Soma de pontos distintos (xp != xq): lam = (yq - yp) * (xq - xp)^(-1) mod 17.
    """
    if ponto_p is None:
        return ponto_q
    if ponto_q is None:
        return ponto_p

    xp, yp = ponto_p
    xq, yq = ponto_q

    # Caso de pontos opostos ou tangente vertical (yp == 0)
    if xp == xq and (yp + yq) % P_MOD == 0:
        return None

    # Cálculo da inclinação (lambda)
    if ponto_p == ponto_q:
        # Duplicação: P + P
        numerador = 3 * xp * xp + A_CURVA
        denominador = 2 * yp
        lam = (numerador * inverso(denominador)) % P_MOD
    else:
        # Soma de pontos distintos
        numerador = yq - yp
        denominador = xq - xp
        lam = (numerador * inverso(denominador)) % P_MOD

    # Coordenadas do ponto resultante R = (xr, yr)
    xr = (lam * lam - xp - xq) % P_MOD
    yr = (lam * (xp - xr) - yp) % P_MOD

    return (xr, yr)


def multiplicar(k: int, ponto: Optional[Tuple[int, int]]) -> Optional[Tuple[int, int]]:
    """Calcula a multiplicação escalar k * P usando o método duplicar e somar (double-and-add).
    
    Rejeita inteiros negativos com ValueError.
    """
    if k < 0:
        raise ValueError("Use k inteiro e não negativo")
    if k == 0 or ponto is None:
        return None

    resultado = None
    atual = ponto

    while k > 0:
        if k % 2 == 1:
            resultado = somar(resultado, atual)
        atual = somar(atual, atual)
        k = k // 2

    return resultado


def acordo_ecdh(priv_a: int, priv_b: int, ponto_base: Tuple[int, int] = PONTO_G) -> Dict:
    """Executa o acordo de chaves Diffie-Hellman em Curvas Elípticas (ECDH).
    
    Alice escolhe escalar privado priv_a e publica A = priv_a * G.
    Bob escolhe escalar privado priv_b e publica B = priv_b * G.
    Ambos calculam o segredo compartilhado:
        S_Alice = priv_a * B
        S_Bob = priv_b * A
    Retorna os públicos e o segredo compartilhado em comum.
    """
    pub_a = multiplicar(priv_a, ponto_base)
    pub_b = multiplicar(priv_b, ponto_base)

    segredo_alice = multiplicar(priv_a, pub_b)
    segredo_bob = multiplicar(priv_b, pub_a)

    assert segredo_alice == segredo_bob, "Os segredos compartilhados calculados em ambos os lados devem ser iguais"

    return {
        "priv_a": priv_a,
        "priv_b": priv_b,
        "pub_a": pub_a,
        "pub_b": pub_b,
        "segredo_compartilhado": segredo_alice
    }


def quebrar_ecdlp_por_forca_bruta(ponto_publico: Tuple[int, int], ponto_base: Tuple[int, int] = PONTO_G, ordem: int = ORDEM_G) -> int:
    """Resolve o ECDLP na curva didática por busca exaustiva (enumeração de escalares).
    
    Dado Q = k * G, testa k de 1 até a ordem de G até encontrar o ponto coincidente.
    """
    for k_candidato in range(1, ordem):
        if multiplicar(k_candidato, ponto_base) == ponto_publico:
            return k_candidato
    raise ValueError(f"Escalar não encontrado para o ponto {ponto_publico}")


def listar_subgrupo_gerado(ponto_base: Tuple[int, int] = PONTO_G, ordem: int = ORDEM_G) -> List[Tuple[int, Optional[Tuple[int, int]]]]:
    """Gera a lista completa dos múltiplos k * G para k de 1 até a ordem."""
    return [(k, multiplicar(k, ponto_base)) for k in range(1, ordem + 1)]
