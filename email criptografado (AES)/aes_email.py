"""
Núcleo de Criptografia de E-mail com AES (AES-256-GCM e AES-256-CBC).

Permite:
1. Gerar chave AES aleatória (em formato Base64 fácil de compartilhar) ou derivar chave de uma senha (PBKDF2-HMAC-SHA256).
2. Criptografar um e-mail (Remetente, Destinatário, Assunto e Corpo da mensagem), gerando um pacote Base64 ou arquivo JSON pronto para enviar ao colega.
3. Descriptografar o pacote recebido usando a chave compartilhada para descobrir o conteúdo original.
4. (Opcional) Enviar o e-mail criptografado via servidor SMTP real (ex: Gmail, Outlook) ou salvar/copiar para troca direta na atividade em dupla.
"""

import base64
import json
import os
import smtplib
from email.message import EmailMessage
from datetime import datetime
from typing import Dict, Any, Tuple, Optional

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def gerar_chave_aes(tamanho_bits: int = 256) -> str:
    """
    Gera uma chave AES criptograficamente segura e retorna em Base64
    para facilitar o envio/compartilhamento com a dupla.
    """
    if tamanho_bits not in (128, 192, 256):
        raise ValueError("O tamanho da chave AES deve ser 128, 192 ou 256 bits.")
    chave_bytes = os.urandom(tamanho_bits // 8)
    return base64.b64encode(chave_bytes).decode("utf-8")


def derivar_chave_de_senha(senha: str, salt: Optional[bytes] = None) -> Tuple[bytes, bytes]:
    """
    Deriva uma chave AES de 256 bits (32 bytes) a partir de uma senha/palavra-chave
    combinada entre a dupla usando PBKDF2-HMAC-SHA256.
    """
    if salt is None:
        salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
    )
    chave_bytes = kdf.derive(senha.encode("utf-8"))
    return chave_bytes, salt


def decodificar_chave(chave_str: str, salt_b64: Optional[str] = None) -> Tuple[bytes, Optional[bytes]]:
    """
    Interpreta a chave fornecida pelo usuário:
    - Se for uma chave Base64 válida de 16, 24 ou 32 bytes (e sem salt de senha), usa diretamente.
    - Caso contrário, trata como uma senha em texto e deriva uma chave AES-256 via PBKDF2.
    """
    chave_limpa = chave_str.strip()
    if salt_b64:
        salt = base64.b64decode(salt_b64)
        chave_bytes, _ = derivar_chave_de_senha(chave_limpa, salt)
        return chave_bytes, salt

    # Tenta decodificar como chave AES direta em Base64
    try:
        possiveis_bytes = base64.b64decode(chave_limpa, validate=True)
        if len(possiveis_bytes) in (16, 24, 32) and base64.b64encode(possiveis_bytes).decode("utf-8") == chave_limpa:
            return possiveis_bytes, None
    except Exception:
        pass

    # Também aceita chave em Hexadecimal (32, 48 ou 64 caracteres hex)
    try:
        if len(chave_limpa) in (32, 48, 64):
            possiveis_bytes = bytes.fromhex(chave_limpa)
            return possiveis_bytes, None
    except Exception:
        pass

    # Trata como senha/frase secreta combinada entre a dupla
    chave_bytes, salt = derivar_chave_de_senha(chave_limpa)
    return chave_bytes, salt


def criptografar_email(
    remetente: str,
    destinatario: str,
    assunto: str,
    mensagem: str,
    chave_str: str,
    modo: str = "GCM"
) -> Dict[str, Any]:
    """
    Criptografa o conteúdo de um e-mail utilizando AES (modo GCM ou CBC).

    No modo GCM (padrão recomendado), os cabeçalhos (De, Para, Assunto) também
    são autenticados como AAD (Associated Authenticated Data), e o corpo da
    mensagem é confidencial e autenticado.
    """
    modo = modo.upper().strip()
    if modo not in ("GCM", "CBC"):
        raise ValueError("Modo inválido. Escolha 'GCM' ou 'CBC'.")

    chave_bytes, salt = decodificar_chave(chave_str)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Estrutura completa do conteúdo secreto do e-mail
    conteudo_claro = {
        "remetente": remetente,
        "destinatario": destinatario,
        "assunto": assunto,
        "mensagem": mensagem,
        "data_hora": timestamp,
    }
    dados_bytes = json.dumps(conteudo_claro, ensure_ascii=False).encode("utf-8")

    # Metadados públicos do envelope de e-mail
    cabecalho_aad = f"From:{remetente}|To:{destinatario}|Subj:{assunto}".encode("utf-8")

    if modo == "GCM":
        nonce = os.urandom(12)  # 96 bits recomendados pelo NIST para AES-GCM
        aesgcm = AESGCM(chave_bytes)
        texto_cifrado = aesgcm.encrypt(nonce, dados_bytes, cabecalho_aad)
        iv_ou_nonce_b64 = base64.b64encode(nonce).decode("utf-8")
    else:
        iv = os.urandom(16)  # 128 bits (tamanho do bloco do AES) para CBC
        padder = padding.PKCS7(128).padder()
        dados_padded = padder.update(dados_bytes) + padder.finalize()
        cipher = Cipher(algorithms.AES(chave_bytes), modes.CBC(iv))
        encryptor = cipher.encryptor()
        texto_cifrado = encryptor.update(dados_padded) + encryptor.finalize()
        iv_ou_nonce_b64 = base64.b64encode(iv).decode("utf-8")

    envelope = {
        "algoritmo": f"AES-{len(chave_bytes) * 8}-{modo}",
        "modo": modo,
        "remetente": remetente,
        "destinatario": destinatario,
        "assunto": assunto,
        "iv_nonce": iv_ou_nonce_b64,
        "salt": base64.b64encode(salt).decode("utf-8") if salt else None,
        "ciphertext": base64.b64encode(texto_cifrado).decode("utf-8"),
    }
    return envelope


def exportar_codigo_compartilhavel(envelope: Dict[str, Any]) -> str:
    """
    Transforma o envelope JSON do e-mail criptografado em uma string compacta Base64
    para colar facilmente no WhatsApp, Discord, e-mail ou terminal do colega.
    """
    json_bytes = json.dumps(envelope, ensure_ascii=False).encode("utf-8")
    return base64.b64encode(json_bytes).decode("utf-8")


def importar_codigo_compartilhavel(texto_entrada: str) -> Dict[str, Any]:
    """
    Lê tanto um código compacto em Base64 quanto um JSON formatado.
    """
    limpo = texto_entrada.strip()
    if limpo.startswith("{") and limpo.endswith("}"):
        return json.loads(limpo)
    try:
        decodificado = base64.b64decode(limpo).decode("utf-8")
        return json.loads(decodificado)
    except Exception as exc:
        raise ValueError("Formato de e-mail criptografado inválido! Verifique se copiou todo o código ou JSON.") from exc


def descriptografar_email(envelope_ou_codigo: Any, chave_str: str) -> Dict[str, Any]:
    """
    Descriptografa um e-mail recebido (em dicionário JSON ou código Base64)
    usando a chave AES ou senha fornecida pelo colega.
    """
    if isinstance(envelope_ou_codigo, str):
        envelope = importar_codigo_compartilhavel(envelope_ou_codigo)
    elif isinstance(envelope_ou_codigo, dict):
        envelope = envelope_ou_codigo
    else:
        raise TypeError("O pacote recebido deve ser um dicionário (JSON) ou string (Base64/JSON).")

    modo = envelope.get("modo", "GCM").upper()
    iv_nonce = base64.b64decode(envelope["iv_nonce"])
    texto_cifrado = base64.b64decode(envelope["ciphertext"])
    salt_b64 = envelope.get("salt")

    chave_bytes, _ = decodificar_chave(chave_str, salt_b64=salt_b64)

    remetente = envelope.get("remetente", "")
    destinatario = envelope.get("destinatario", "")
    assunto = envelope.get("assunto", "")
    cabecalho_aad = f"From:{remetente}|To:{destinatario}|Subj:{assunto}".encode("utf-8")

    try:
        if modo == "GCM":
            aesgcm = AESGCM(chave_bytes)
            dados_bytes = aesgcm.decrypt(iv_nonce, texto_cifrado, cabecalho_aad)
        elif modo == "CBC":
            cipher = Cipher(algorithms.AES(chave_bytes), modes.CBC(iv_nonce))
            decryptor = cipher.decryptor()
            dados_padded = decryptor.update(texto_cifrado) + decryptor.finalize()
            unpadder = padding.PKCS7(128).unpadder()
            dados_bytes = unpadder.update(dados_padded) + unpadder.finalize()
        else:
            raise ValueError(f"Modo de operação desconhecido: {modo}")
    except (InvalidTag, ValueError) as exc:
        raise ValueError(
            "Falha ao descriptografar! A chave está incorreta ou o e-mail criptografado foi adulterado."
        ) from exc

    conteudo = json.loads(dados_bytes.decode("utf-8"))
    return conteudo


def formatar_email_para_exibicao(envelope: Dict[str, Any], chave_exibicao: Optional[str] = None) -> str:
    """
    Formata o e-mail criptografado de maneira clara para visualização no terminal
    ou envio ao amigo.
    """
    codigo_compacto = exportar_codigo_compartilhavel(envelope)
    linhas = [
        "=" * 70,
        " 📧 E-MAIL CRIPTOGRAFADO COM AES (PRONTO PARA ENVIAR À SUA DUPLA)",
        "=" * 70,
        f"De        : {envelope['remetente']}",
        f"Para      : {envelope['destinatario']}",
        f"Assunto   : {envelope['assunto']}",
        f"Algoritmo : {envelope['algoritmo']}",
        f"IV / Nonce: {envelope['iv_nonce']}",
    ]
    if envelope.get("salt"):
        linhas.append(f"Salt (KDF): {envelope['salt']}")
    linhas.extend([
        "-" * 70,
        "🔒 CORPO CIFRADO (CIPHERTEXT EM BASE64):",
        envelope["ciphertext"],
        "-" * 70,
        "📦 CÓDIGO COMPLETO PARA ENVIAR AO SEU AMIGO (COPIE TUDO ABAIXO):",
        codigo_compacto,
        "-" * 70,
    ])
    if chave_exibicao:
        linhas.append(f"🔑 CHAVE SECRETA (ENVIE AO SEU AMIGO PARA ELE DESCRIPTOGRAFAR): {chave_exibicao}")
        linhas.append("=" * 70)
    return "\n".join(linhas)


def enviar_email_smtp_real(
    envelope: Dict[str, Any],
    servidor_smtp: str,
    porta_smtp: int,
    usuario_smtp: str,
    senha_smtp: str,
) -> None:
    """
    Envia opcionalmente o e-mail criptografado através de um servidor SMTP real
    (ex: smtp.gmail.com na porta 587 com Senha de App).
    """
    msg = EmailMessage()
    msg["From"] = envelope["remetente"]
    msg["To"] = envelope["destinatario"]
    msg["Subject"] = f"[CRIPTOGRAFADO - AES] {envelope['assunto']}"

    codigo_compacto = exportar_codigo_compartilhavel(envelope)
    corpo_email = (
        "Você recebeu um e-mail criptografado com AES!\n\n"
        f"Algoritmo utilizado: {envelope['algoritmo']}\n"
        "Para descobrir o que está escrito, execute o script 'descriptografar_email.py' "
        "informando a chave secreta e o código abaixo:\n\n"
        "--- INÍCIO DO CÓDIGO CRIPTOGRAFADO ---\n"
        f"{codigo_compacto}\n"
        "--- FIM DO CÓDIGO CRIPTOGRAFADO ---\n\n"
        "JSON Detalhado:\n"
        f"{json.dumps(envelope, indent=2, ensure_ascii=False)}\n"
    )
    msg.set_content(corpo_email)

    with smtplib.SMTP(servidor_smtp, porta_smtp, timeout=15) as server:
        server.starttls()
        server.login(usuario_smtp, senha_smtp)
        server.send_message(msg)
