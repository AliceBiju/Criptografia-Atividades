#!/usr/bin/env python3
"""
VERSÃO 2: DESCRIPTOGRAFAR E-MAIL RECEBIDO (AES)
Execute este script quando seu amigo te enviar um e-mail criptografado e a chave
para descobrir o que está escrito na mensagem secreta dele!
"""

import json
from pathlib import Path
from aes_email import descriptografar_email


def executar_descriptografia_interativa() -> None:
    print("=" * 70)
    print(" 🔓 VERSÃO 2: DESCRIPTOGRAFAR E-MAIL COM AES (RECEBIDO DA DUPLA)")
    print("=" * 70)

    pasta_atual = Path(__file__).resolve().parent
    caminho_padrao = pasta_atual / "email_criptografado.json"

    print("Como você recebeu o e-mail criptografado do seu amigo?")
    print("  [1] Colar o CÓDIGO Base64 (ou JSON) que meu amigo me enviou")
    print(f"  [2] Ler de um arquivo JSON (padrão: {caminho_padrao.name})")
    opcao = input("Escolha (1 ou 2) [padrão=1]: ").strip() or "1"

    pacote_entrada = None

    if opcao == "2":
        nome_arq = input(f"Nome ou caminho do arquivo [padrão: {caminho_padrao.name}]: ").strip()
        caminho_arq = Path(nome_arq) if nome_arq else caminho_padrao
        if not caminho_arq.is_absolute() and not caminho_arq.exists():
            caminho_arq = pasta_atual / caminho_arq
        if not caminho_arq.exists():
            print(f"\n❌ Arquivo '{caminho_arq}' não encontrado!")
            return
        with open(caminho_arq, "r", encoding="utf-8") as f:
            pacote_entrada = json.load(f)
        print(f"✅ Arquivo '{caminho_arq.name}' carregado com sucesso!")
    else:
        print("\nCole abaixo o CÓDIGO COMPLETO em Base64 (ou JSON) enviado pelo seu amigo:")
        codigo_colado = input("> ").strip()
        if not codigo_colado:
            if caminho_padrao.exists():
                print(f"Nenhum código colado. Carregando automaticamente '{caminho_padrao.name}'...")
                with open(caminho_padrao, "r", encoding="utf-8") as f:
                    pacote_entrada = json.load(f)
            else:
                print("\n❌ Nenhum código criptografado foi informado!")
                return
        else:
            pacote_entrada = codigo_colado

    chave = input("\n🔑 Digite ou cole a CHAVE SECRETA (ou senha) que seu amigo te enviou:\n> ").strip()
    if not chave:
        print("\n❌ Você precisa informar a chave secreta para descriptografar o e-mail!")
        return

    try:
        dados_revelados = descriptografar_email(pacote_entrada, chave)
        print("\n" + "=" * 70)
        print(" 🎉 SUCESSO! E-MAIL DESCRIPTOGRAFADO COM A CHAVE AES:")
        print("=" * 70)
        print(f"De        : {dados_revelados.get('remetente')}")
        print(f"Para      : {dados_revelados.get('destinatario')}")
        print(f"Assunto   : {dados_revelados.get('assunto')}")
        print(f"Data/Hora : {dados_revelados.get('data_hora')}")
        print("-" * 70)
        print("📩 MENSAGEM SECRETA DESCOBERTA:")
        print(dados_revelados.get("mensagem"))
        print("=" * 70)
    except ValueError as erro:
        print("\n" + "=" * 70)
        print(f" ❌ ERRO NA DESCRIPTOGRAFIA: {erro}")
        print("=" * 70)


if __name__ == "__main__":
    executar_descriptografia_interativa()
