import unittest
from aes_email import (
    gerar_chave_aes,
    criptografar_email,
    descriptografar_email,
    exportar_codigo_compartilhavel,
)


class TestEmailCriptografadoAES(unittest.TestCase):
    def test_fluxo_dupla_ida_e_volta_aes_gcm(self):
        """Simula o envio de e-mail criptografado (Aluno A -> Aluno B) e resposta (Aluno B -> Aluno A) com AES-256-GCM."""
        # 1. Aluno A envia para Aluno B com chave aleatória de 256 bits
        chave_a = gerar_chave_aes(256)
        envelope_a = criptografar_email(
            remetente="aluno_a@dupla.com",
            destinatario="aluno_b@dupla.com",
            assunto="Segredo da Dupla - Parte 1",
            mensagem="Olá amigo, o código secreto da nossa atividade é 42-AES!",
            chave_str=chave_a,
            modo="GCM",
        )
        codigo_a = exportar_codigo_compartilhavel(envelope_a)

        # Aluno B descriptografa com a chave A
        revelado_b = descriptografar_email(codigo_a, chave_a)
        self.assertEqual(revelado_b["remetente"], "aluno_a@dupla.com")
        self.assertEqual(revelado_b["destinatario"], "aluno_b@dupla.com")
        self.assertEqual(revelado_b["assunto"], "Segredo da Dupla - Parte 1")
        self.assertEqual(revelado_b["mensagem"], "Olá amigo, o código secreto da nossa atividade é 42-AES!")

        # 2. Aluno B responde para Aluno A usando uma senha secreta combinada
        chave_b = "chave-secreta-do-meu-amigo-123"
        envelope_b = criptografar_email(
            remetente="aluno_b@dupla.com",
            destinatario="aluno_a@dupla.com",
            assunto="RE: Segredo da Dupla - Parte 2",
            mensagem="Recebido e descriptografado! Agora descriptografe a minha mensagem!",
            chave_str=chave_b,
            modo="GCM",
        )
        codigo_b = exportar_codigo_compartilhavel(envelope_b)

        # Aluno A descriptografa com a chave B
        revelado_a = descriptografar_email(codigo_b, chave_b)
        self.assertEqual(revelado_a["mensagem"], "Recebido e descriptografado! Agora descriptografe a minha mensagem!")

    def test_criptografia_e_descriptografia_modo_cbc(self):
        """Verifica funcionamento no modo clássico AES-256-CBC com padding PKCS7."""
        chave = gerar_chave_aes(256)
        envelope = criptografar_email(
            remetente="alice@cripto.br",
            destinatario="bob@cripto.br",
            assunto="Teste AES-CBC",
            mensagem="Mensagem com acentuação: criptografia simétrica em blocos!",
            chave_str=chave,
            modo="CBC",
        )
        self.assertEqual(envelope["modo"], "CBC")
        revelado = descriptografar_email(envelope, chave)
        self.assertEqual(revelado["mensagem"], "Mensagem com acentuação: criptografia simétrica em blocos!")

    def test_chave_incorreta_bloqueia_leitura(self):
        """Garante que uma chave errada não consegue descobrir o que está escrito no e-mail."""
        chave_correta = gerar_chave_aes(256)
        chave_errada = gerar_chave_aes(256)

        envelope = criptografar_email(
            remetente="alice@cripto.br",
            destinatario="bob@cripto.br",
            assunto="Confidencial",
            mensagem="Apenas quem tem a chave correta pode ler isto.",
            chave_str=chave_correta,
            modo="GCM",
        )
        with self.assertRaises(ValueError):
            descriptografar_email(envelope, chave_errada)

    def test_adulteracao_de_ciphertext_ou_cabecalho_detectada(self):
        """Garante que qualquer alteração no e-mail criptografado ou no remetente/assunto invalida a tag GCM."""
        chave = gerar_chave_aes(256)
        envelope = criptografar_email(
            remetente="alice@cripto.br",
            destinatario="bob@cripto.br",
            assunto="Integridade Garantida",
            mensagem="Valor do PIX: R$ 100,00",
            chave_str=chave,
            modo="GCM",
        )
        envelope_adulterado = dict(envelope)
        envelope_adulterado["assunto"] = "Assunto Falso Modificado por Atacante"
        with self.assertRaises(ValueError):
            descriptografar_email(envelope_adulterado, chave)


if __name__ == "__main__":
    unittest.main()
