from typing import List, Tuple

ALFABETO = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

FREQUENCIA_PT = {
    'A': 14.63, 'E': 12.57, 'O': 10.73, 'S': 7.81, 'R': 6.53,
    'I': 6.18,  'N': 5.05,  'D': 4.99,  'M': 4.74, 'U': 4.63,
    'T': 4.34,  'C': 3.88,  'L': 2.78,  'P': 2.52, 'V': 1.67,
    'G': 1.30,  'H': 1.28,  'Q': 1.20,  'B': 1.04, 'F': 1.02,
    'Z': 0.47,  'J': 0.40,  'X': 0.21,  'K': 0.02, 'Y': 0.01, 'W': 0.01
}

PALAVRAS_COMUNS_PT = ["DE", "A", "QUE", "AO", "O", "DO", "DA", "EM", "UM", "PARA", "COM", "NAO", "SE", "POR", "MAIS", "AS", "OS"]


def cesar(texto: str, chave: int) -> str:
    """Aplica a Cifra de César com deslocamento 'chave' sobre o texto."""
    resultado = []
    chave = chave % 26
    for char in texto:
        if char.upper() in ALFABETO:
            eh_maiuscula = char.isupper()
            idx = ALFABETO.index(char.upper())
            novo_char = ALFABETO[(idx + chave) % 26]
            resultado.append(novo_char if eh_maiuscula else novo_char.lower())
        else:
            resultado.append(char)
    return "".join(resultado)


def decifrar(texto: str, chave: int) -> str:
    """Decifra um texto cifrado com a Cifra de César."""
    return cesar(texto, -chave)


def candidatas(texto_cifrado: str) -> List[Tuple[int, str]]:
    """Gera todas as 26 decifrações possíveis para o texto cifrado."""
    return [(k, decifrar(texto_cifrado, k)) for k in range(26)]


def pontuar_candidata(texto: str) -> float:
    """Calcula pontuação linguística para um texto candidato em português."""
    pontuacao = 0.0
    texto_upper = texto.upper()
    palavras = [p.strip(".,;:!?-") for p in texto_upper.split()]
    
    for p in palavras:
        if p in PALAVRAS_COMUNS_PT:
            pontuacao += 30.0

    for char in texto_upper:
        if char in FREQUENCIA_PT:
            pontuacao += FREQUENCIA_PT[char]
            
    return pontuacao


def ordenar_candidatas(texto_cifrado: str) -> List[Tuple[int, str, float]]:
    """Devolve as 26 hipóteses ordenadas da mais provável para a menos provável."""
    lista = []
    for k, decifrado in candidatas(texto_cifrado):
        score = pontuar_candidata(decifrado)
        lista.append((k, decifrado, score))
    return sorted(lista, key=lambda item: item[2], reverse=True)


def cifrar_composta(palavra: str, chave_cesar: int) -> str:
    """César + Transposição colunar em duas colunas."""
    substituida = cesar(palavra, chave_cesar)
    return substituida[0::2] + substituida[1::2]


def decifrar_composta(cifrado: str, chave_cesar: int) -> str:
    """Desfaz transposição de 2 colunas e em seguida desfaz César."""
    n = len(cifrado)
    metade = (n + 1) // 2
    col1 = cifrado[:metade]
    col2 = cifrado[metade:]
    
    intercalado = []
    for i in range(metade):
        intercalado.append(col1[i])
        if i < len(col2):
            intercalado.append(col2[i])
            
    return decifrar("".join(intercalado), chave_cesar)
