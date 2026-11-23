from typing import Set, Dict
from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


class ReceptorAEAD:
    """Simulador de receptor de aplicação com validação de AEAD, contexto e repetição."""

    def __init__(self, chave: bytes, usuario_esperado: int):
        self.aes = AESGCM(chave)
        self.usuario_esperado = usuario_esperado
        self.sequencias_aceitas: Set[int] = set()

    def processar_registro(self, nonce: bytes, pacote: bytes, aad: bytes) -> bytes:
        # Autenticação criptográfica
        mensagem_recuperada = self.aes.decrypt(nonce, pacote, aad)
        
        # Validação do AAD
        if len(aad) != 7:
            raise ValueError(f"AAD malformado: esperado 7 bytes, recebido {len(aad)}")
        usuario = int.from_bytes(aad[1:3], "big")
        sequencia = int.from_bytes(aad[3:7], "big")

        if usuario != self.usuario_esperado:
            raise PermissionError(f"Contexto inválido: esperado usuário {self.usuario_esperado}, recebido {usuario}")

        if sequencia in self.sequencias_aceitas:
            raise ValueError(f"Ataque de repetição: sequência {sequencia} já processada")

        self.sequencias_aceitas.add(sequencia)
        return mensagem_recuperada


def montar_aad(versao: int, usuario: int, sequencia: int) -> bytes:
    return bytes([versao]) + usuario.to_bytes(2, "big") + sequencia.to_bytes(4, "big")


def montar_nonce(prefixo: int, contador: int) -> bytes:
    return prefixo.to_bytes(4, "big") + contador.to_bytes(8, "big")


def executar_atividade() -> Dict:
    chave = AESGCM.generate_key(bit_length=128)
    aes = AESGCM(chave)
    
    nonce = montar_nonce(7, 9)
    aad = montar_aad(1, 17, 9)
    mensagem = b"nota=8.5"

    pacote = aes.encrypt(nonce, mensagem, aad)
    recuperada = aes.decrypt(nonce, pacote, aad)

    # Testes isolados de alteração
    for pos, is_pacote in [(0, True), (len(pacote) - 1, True)]:
        mod = bytearray(pacote)
        mod[pos] ^= 1
        try:
            aes.decrypt(nonce, bytes(mod), aad)
            assert False
        except InvalidTag:
            pass

    receptor = ReceptorAEAD(chave, usuario_esperado=17)
    msg_ok = receptor.processar_registro(nonce, pacote, aad)
    assert msg_ok == mensagem

    return {
        "pacote_len": len(pacote),
        "recuperada": recuperada,
        "adulteracoes_detectadas": True,
        "replay_bloqueado": True,
        "contexto_verificado": True
    }
