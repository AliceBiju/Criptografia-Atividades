#!/usr/bin/env python3
"""
VERSÃO 1: CRIPTOGRAFAR E ENVIAR E-MAIL (AES)
Execute este script para escrever seu e-mail, criptografá-lo com AES e gerar
o código/arquivo criptografado + a chave secreta para enviar ao seu amigo da dupla.
"""

import json
from pathlib import Path
from aes_email import (
    gerar_chave_aes,
    criptografar_email,
    formatar_email_para_exibicao,
    exportar_codigo_compartilhavel,
    enviar_email_smtp_real,
)


def executar_criptografia_interativa() -> None:
    print("=" * 70)
    print(" 🔒 VERSÃO 1: CRIPTOGRAFAR E-MAIL COM AES (ENVIAR PARA SUA DUPLA)")
    print("=" * 70)

    remetente = input("Seu e-mail (Remetente) [ex: voce@email.com]: ").strip() or "aluno1@cripto.edu.br"
    destinatario = input("E-mail do seu amigo (Destinatário) [ex: amigo@email.com]: ").strip() or "aluno2@cripto.edu.br"
    assunto = input("Assunto do e-mail: ").strip() or "Mensagem Secreta da Atividade AES"

    print("\nDigite a mensagem secreta do e-mail (pressione ENTER para confirmar):")
    mensagem = input("> ").strip()
    if not mensagem:
        mensagem = "Olá amigo! Se você conseguiu descriptografar este e-mail com a chave AES, nossa atividade em dupla funcionou perfeitamente!"

    print("\nComo deseja definir a chave AES?")
    print("  [1] Gerar uma chave AES-256 aleatória automaticamente (Recomendado)")
    print("  [2] Digitar uma senha ou chave secreta personalizada para combinar com seu amigo")
    opcao_chave = input("Escolha (1 ou 2) [padrão=1]: ").strip() or "1"

    if opcao_chave == "2":
        chave = input("Digite a senha ou chave secreta: ").strip()
        if not chave:
            chave = gerar_chave_aes(256)
            print(f"Nenhuma senha digitada. Chave AES-256 gerada automaticamente: {chave}")
    else:
        chave = gerar_chave_aes(256)

    print("\nQual modo de operação do AES deseja utilizar?")
    print("  [1] AES-256-GCM (Criptografia Autenticada - Padrão Moderno)")
    print("  [2] AES-256-CBC (Criptografia Clássica em Blocos com PKCS7)")
    opcao_modo = input("Escolha (1 ou 2) [padrão=1]: ").strip() or "1"
    modo = "CBC" if opcao_modo == "2" else "GCM"

    envelope = criptografar_email(
        remetente=remetente,
        destinatario=destinatario,
        assunto=assunto,
        mensagem=mensagem,
        chave_str=chave,
        modo=modo,
    )

    print("\n" + formatar_email_para_exibicao(envelope, chave_exibicao=chave))

    # Salva automaticamente em arquivo JSON e TXT para facilitar o envio ao colega
    pasta_atual = Path(__file__).resolve().parent
    caminho_json = pasta_atual / "email_criptografado.json"
    caminho_txt = pasta_atual / "email_para_enviar_ao_amigo.txt"

    with open(caminho_json, "w", encoding="utf-8") as f:
        json.dump(envelope, f, indent=2, ensure_ascii=False)

    codigo_compacto = exportar_codigo_compartilhavel(envelope)
    with open(caminho_txt, "w", encoding="utf-8") as f:
        f.write(formatar_email_para_exibicao(envelope, chave_exibicao=chave) + "\n")

    print(f"\n✅ Arquivo JSON salvo em : {caminho_json.name}")
    print(f"✅ Resumo para envio em : {caminho_txt.name}")
    print("\n👉 O QUE FAZER AGORA NA ATIVIDADE EM DUPLA:")
    print("   1. Envie o 'CÓDIGO COMPLETO' (ou o arquivo 'email_criptografado.json') para o seu amigo.")
    print(f"   2. Envie a CHAVE SECRETA ({chave}) para ele descriptografar no computador dele!")

    # Opção extra de envio real por SMTP
    enviar_real = input("\nDeseja também disparar este e-mail via servidor SMTP real (Gmail/Outlook)? (s/N): ").strip().lower()
    if enviar_real == "s":
        servidor = input("Servidor SMTP [padrão: smtp.gmail.com]: ").strip() or "smtp.gmail.com"
        porta_str = input("Porta SMTP [padrão: 587]: ").strip() or "587"
        usuario_smtp = input(f"Usuário SMTP [padrão: {remetente}]: ").strip() or remetente
        senha_smtp = input("Senha SMTP (ou Senha de App do Gmail): ").strip()
        try:
            enviar_email_smtp_real(envelope, servidor, int(porta_str), usuario_smtp, senha_smtp)
            print("✅ E-mail criptografado enviado com sucesso via SMTP!")
        except Exception as e:
            print(f"⚠️ Não foi possível enviar via SMTP ({e}). Use o código/arquivo gerado acima para enviar ao seu amigo.")


if __name__ == "__main__":
    executar_criptografia_interativa()
