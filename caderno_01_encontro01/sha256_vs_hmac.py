import hashlib
import hmac
import secrets


def sha256(mensagem: bytes) -> bytes:
    """Calcula o resumo criptográfico SHA-256 de uma mensagem."""
    return hashlib.sha256(mensagem).digest()


def criar_hmac(chave: bytes, mensagem: bytes) -> bytes:
    """Produz uma etiqueta de autenticação HMAC-SHA-256."""
    return hmac.new(chave, mensagem, hashlib.sha256).digest()


def verificar_hmac(chave: bytes, mensagem: bytes, etiqueta: bytes) -> bool:
    """Verifica uma etiqueta HMAC-SHA-256 com comparação em tempo constante."""
    etiqueta_calculada = criar_hmac(chave, mensagem)
    return hmac.compare_digest(etiqueta_calculada, etiqueta)


def simular_cenario():
    """Simula o cenário completo de transferência bancária, ataque e defesa."""
    original = b"destino=ana;valor=100"
    alterada = b"destino=ana;valor=900"

    hash_original = sha256(original)
    hash_forjado = sha256(alterada)
    assert hash_forjado == sha256(alterada), "O hash forjado deve bater com a mensagem alterada"

    chave_legitima = secrets.token_bytes(32)
    chave_atacante = secrets.token_bytes(32)

    etiqueta_original = criar_hmac(chave_legitima, original)
    assert verificar_hmac(chave_legitima, original, etiqueta_original), "Etiqueta legítima deve ser aceita"

    etiqueta_atacante = criar_hmac(chave_atacante, alterada)
    autenticado = verificar_hmac(chave_legitima, alterada, etiqueta_atacante)
    assert not autenticado, "O servidor deve rejeitar a etiqueta criada com chave inválida"

    return {
        "original": original,
        "alterada": alterada,
        "hash_original_hex": hash_original.hex(),
        "hash_forjado_hex": hash_forjado.hex(),
        "hmac_legitimo_aceito": True,
        "hmac_atacante_aceito": autenticado,
    }


if __name__ == "__main__":
    resultado = simular_cenario()
    print("=== Caderno 01: Demonstração SHA-256 vs HMAC ===")
    print(f"Mensagem Original: {resultado['original'].decode()}")
    print(f"Mensagem Alterada: {resultado['alterada'].decode()}")
    print(f"Hash SHA-256 Original: {resultado['hash_original_hex'][:16]}...")
    print(f"Hash SHA-256 Forjado : {resultado['hash_forjado_hex'][:16]}...")
    print(f"HMAC Legítimo Aceito : {resultado['hmac_legitimo_aceito']}")
    print(f"HMAC Forjado Aceito  : {resultado['hmac_atacante_aceito']}")
