import secrets
from typing import Dict
from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def derivar_chave(segredo_compartilhado: bytes, sal: bytes, info_contexto: bytes) -> bytes:
    """Deriva chave de 32 bytes usando HKDF-SHA256."""
    hkdf = HKDF(algorithm=hashes.SHA256(), length=32, salt=sal, info=info_contexto)
    return hkdf.derive(segredo_compartilhado)


def executar_acordo_legitimo() -> Dict:
    priv_alice = X25519PrivateKey.generate()
    priv_bob = X25519PrivateKey.generate()

    sa = priv_alice.exchange(priv_bob.public_key())
    sb = priv_bob.exchange(priv_alice.public_key())
    assert sa == sb

    sal = secrets.token_bytes(16)
    contexto = b"acordo-legitimo-sessao-01"
    
    chave_alice = derivar_chave(sa, sal, contexto)
    chave_bob = derivar_chave(sb, sal, contexto)

    mensagem = b"nota=8.5"
    nonce = secrets.token_bytes(12)
    aad = b"protocolo=v1;remetente=alice;destinatario=bob"
    
    pacote = AESGCM(chave_alice).encrypt(nonce, mensagem, aad)
    mensagem_recuperada = AESGCM(chave_bob).decrypt(nonce, pacote, aad)
    assert mensagem_recuperada == mensagem

    return {
        "sa": sa,
        "chave_derivada": chave_alice,
        "mensagem": mensagem,
        "mensagem_recuperada": mensagem_recuperada,
        "sal": sal,
        "nonce": nonce,
        "aad": aad,
        "pacote": pacote
    }


def simular_ataque_intermediario_mallory() -> Dict:
    priv_alice = X25519PrivateKey.generate()
    priv_bob = X25519PrivateKey.generate()
    priv_mallory = X25519PrivateKey.generate()

    pub_alice = priv_alice.public_key()
    pub_bob = priv_bob.public_key()
    pub_mallory = priv_mallory.public_key()

    sal = secrets.token_bytes(16)
    contexto = b"sessao-com-mitm"

    s_alice_mallory = priv_alice.exchange(pub_mallory)
    s_mallory_alice = priv_mallory.exchange(pub_alice)
    chave_alice_mallory = derivar_chave(s_alice_mallory, sal, contexto)

    s_bob_mallory = priv_bob.exchange(pub_mallory)
    s_mallory_bob = priv_mallory.exchange(pub_bob)
    chave_mallory_bob = derivar_chave(s_mallory_bob, sal, contexto)

    # Alice cifra para Mallory
    mensagem_alice = b"nota=8.5"
    nonce_am = secrets.token_bytes(12)
    pacote_am = AESGCM(chave_alice_mallory).encrypt(nonce_am, mensagem_alice, b"conversa")

    # Mallory abre e recifra para Bob
    msg_lida_por_mallory = AESGCM(chave_alice_mallory).decrypt(nonce_am, pacote_am, b"conversa")
    nonce_mb = secrets.token_bytes(12)
    pacote_mb = AESGCM(chave_mallory_bob).encrypt(nonce_mb, msg_lida_por_mallory, b"conversa")
    msg_bob = AESGCM(chave_mallory_bob).decrypt(nonce_mb, pacote_mb, b"conversa")
    assert msg_bob == mensagem_alice

    return {
        "alice_mallory_chave_igual": s_alice_mallory == s_mallory_alice,
        "bob_mallory_chave_igual": s_bob_mallory == s_mallory_bob,
        "chaves_conexao_diferentes": chave_alice_mallory != chave_mallory_bob,
        "mensagem_espionada": msg_lida_por_mallory
    }
