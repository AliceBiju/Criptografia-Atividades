# Caderno 10 (Encontro 10) — Fundamentos da Criptografia de Chave Pública

## Tema
**Laboratório de conexões certas e erradas: acordo X25519, derivação HKDF e o ataque do intermediário (MITM)**

Neste caderno é implementado um fluxo criptográfico híbrido moderno completo utilizando curvas elípticas (**X25519**), derivação de chaves contextualizada (**HKDF-SHA256**) e cifração autenticada (**AES-GCM**), analisando os limites de um acordo de chaves puro sem autenticação de identidade.

---

## 1. As Três Operações Assimétricas Distintas

Não se deve confundir as três operações fundamentais de chave pública:
1. **Cifração com a Chave Pública do Destinatário:** Permite que qualquer um envie dados confidenciais a Bob, mas **não autentica** quem enviou.
2. **Assinatura Digital com a Chave Privada do Emissor:** Autentica a autoria de Alice sobre a mensagem, mas **não oculta** o conteúdo (continua em claro).
3. **Acordo de Chaves (Diffie-Hellman / X25519):** Permite que duas partes estabeleçam um segredo comum sobre um canal público sem transmiti-lo diretamente.

---

## 2. O Ataque do Intermediário (*Man-In-The-Middle* / Mallory)

### Como Mallory ataca sem quebrar a matemática
1. O protocolo Diffie-Hellman básico garante apenas que se Alice e Bob trocarem suas chaves públicas diretamente, chegarão ao mesmo segredo $s_{AB} = g^{ab}$.
2. Porém, **o protocolo não autentica de quem é a chave pública recebida**.
3. Mallory intercepta a comunicação no canal:
   * Envia sua chave pública $M$ para Alice (fingindo ser Bob).
   * Envia sua chave pública $M$ para Bob (fingindo ser Alice).
4. Estabelecem-se dois acordos perfeitamente válidos na aritmética:
   * **Conexão 1:** Alice e Mallory acordam $s_{AM} = g^{am}$.
   * **Conexão 2:** Bob e Mallory acordam $s_{BM} = g^{bm}$.
5. Quando Alice envia dados autenticados por AES-GCM, Mallory decifra com a chave 1, lê e modifica o conteúdo em claro se desejar, e recifra com a chave 2 para Bob.
6. Bob decifra o pacote com sucesso e assume erroneamente que falou diretamente com Alice!

> **Lição Crítica:** Uma etiqueta AEAD válida ou uma igualdade aritmética comprovam apenas a posse da chave usada naquela conexão pontual, e **não quem obteve essa chave no mundo real**. A autenticação da chave pública (via certificados digitais X.509 ou chaves de assinatura prévias) é indispensável.

---

## 3. Composição Híbrida em Produção
Para levar essa arquitetura a sistemas reais, o protocolo precisa incorporar:
* **Autenticação mútua:** Assinaturas digitais sobre a negociação (*transcript* não ambíguo).
* **Gestão de Nonce:** Proibição absoluta de repetição sob a mesma chave.
* **Separação de Contexto (HKDF `info`):** Diferenciação de chaves para cada direção de tráfego (Alice $\to$ Bob vs Bob $\to$ Alice).
* **Sigilo Futuro (*Forward Secrecy*):** Uso de chaves efêmeras destruídas da memória ao fim da sessão.

---

## 4. Como Executar os Códigos

### Executar a demonstração:
```bash
python caderno_10_encontro10/atividade_11.py
```

### Executar os testes automatizados:
```bash
python -m unittest discover -s caderno_10_encontro10 -p "test_*.py" -v
```
