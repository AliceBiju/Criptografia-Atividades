#!/usr/bin/env python3
"""
SISTEMA COMPLETO DE E-MAIL CRIPTOGRAFADO COM AES (ATIVIDADE EM DUPLA)

Possui:
1. Demonstração automática do fluxo em dupla (Você -> Seu Amigo e Seu Amigo -> Você).
2. Menu interativo unificado com as duas versões:
   - Versão 1: Criptografar e gerar e-mail + chave para enviar ao amigo.
   - Versão 2: Descriptografar o e-mail recebido do amigo usando a chave.
"""

import sys
from aes_email import (
    gerar_chave_aes,
    criptografar_email,
    descriptografar_email,
    exportar_codigo_compartilhavel,
    formatar_email_para_exibicao,
)
from criptografar_email import executar_criptografia_interativa
from descriptografar_email import executar_descriptografia_interativa


def demonstrar_atividade_em_dupla() -> None:
    print("=" * 75)
    print(" 🎓 SIMULAÇÃO COMPLETA DA ATIVIDADE EM DUPLA — E-MAIL CRIPTOGRAFADO (AES)")
    print("=" * 75)

    # -------------------------------------------------------------------------
    # ETAPA 1: Você criptografa um e-mail e envia para o seu amigo
    # -------------------------------------------------------------------------
    print("\n[ETAPA 1] Você está criando e criptografando um e-mail para seu amigo...")
    sua_chave = gerar_chave_aes(256)
    seu_envelope = criptografar_email(
        remetente="voce@faculdade.edu.br",
        destinatario="amigo@faculdade.edu.br",
        assunto="Desafio da Atividade de Criptografia AES",
        mensagem="Fala parceiro! Aqui está o meu e-mail criptografado com AES-256-GCM. A palavra secreta do nosso trabalho é: CRIPTOGRAFIA_NOTA_10.",
        chave_str=sua_chave,
        modo="GCM",
    )
    codigo_enviado_ao_amigo = exportar_codigo_compartilhavel(seu_envelope)
    print(formatar_email_para_exibicao(seu_envelope, chave_exibicao=sua_chave))

    # Amigo recebe e descriptografa com a sua chave
    print("\n[ETAPA 1.1] Seu amigo recebeu o código e a chave e executou a descriptografia:")
    email_aberto_pelo_amigo = descriptografar_email(codigo_enviado_ao_amigo, sua_chave)
    print(f"  -> Assunto descoberto pelo amigo : {email_aberto_pelo_amigo['assunto']}")
    print(f"  -> Mensagem descoberta pelo amigo: {email_aberto_pelo_amigo['mensagem']}")

    # -------------------------------------------------------------------------
    # ETAPA 2: Seu amigo criptografa um e-mail e envia para você descriptografar
    # -------------------------------------------------------------------------
    print("\n" + "-" * 75)
    print("[ETAPA 2] Agora seu amigo criptografou um e-mail de resposta e enviou para você!")
    chave_do_amigo = "SenhaSecretaDaDupla2026"
    envelope_do_amigo = criptografar_email(
        remetente="amigo@faculdade.edu.br",
        destinatario="voce@faculdade.edu.br",
        assunto="RE: Desafio da Atividade de Criptografia AES",
        mensagem="Consegui ler sua mensagem! Agora é sua vez de descriptografar a minha resposta usando nossa senha combinada!",
        chave_str=chave_do_amigo,
        modo="GCM",
    )
    codigo_recebido_do_amigo = exportar_codigo_compartilhavel(envelope_do_amigo)
    print(f"  -> Código criptografado recebido: {codigo_recebido_do_amigo[:80]}...")
    print(f"  -> Chave enviada pelo seu amigo : {chave_do_amigo}")

    print("\n[ETAPA 2.1] Você usa a chave do seu amigo para descobrir o que está escrito:")
    email_aberto_por_voce = descriptografar_email(codigo_recebido_do_amigo, chave_do_amigo)
    print(f"  -> Remetente : {email_aberto_por_voce['remetente']}")
    print(f"  -> Assunto   : {email_aberto_por_voce['assunto']}")
    print(f"  -> Mensagem  : {email_aberto_por_voce['mensagem']}")
    print("=" * 75)


def menu_principal() -> None:
    while True:
        print("\n" + "=" * 70)
        print(" 📧 PROJETO: E-MAIL CRIPTOGRAFADO COM AES (ATIVIDADE EM DUPLA)")
        print("=" * 70)
        print("  [1] 🔒 Versão 1: CRIPTOGRAFAR um e-mail para enviar ao meu amigo")
        print("  [2] 🔓 Versão 2: DESCRIPTOGRAFAR um e-mail que recebi do meu amigo")
        print("  [3] 🎓 Rodar simulação automática de exemplo da atividade em dupla")
        print("  [0] Sair")
        escolha = input("\nEscolha uma opção: ").strip()

        if escolha == "1":
            executar_criptografia_interativa()
        elif escolha == "2":
            executar_descriptografia_interativa()
        elif escolha == "3":
            demonstrar_atividade_em_dupla()
        elif escolha == "0":
            print("Encerrando o programa. Boa atividade!")
            break
        else:
            print("Opção inválida. Digite 1, 2, 3 ou 0.")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demonstrar_atividade_em_dupla()
    else:
        menu_principal()
