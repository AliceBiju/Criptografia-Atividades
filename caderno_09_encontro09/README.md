# Caderno 09 (Encontro 09) — Criptografia Autenticada (AEAD)

## Tema
**Registro AEAD: adulteração, contexto e repetição**

A **Cifração Autenticada com Dados Associados (AEAD)** combina a confidencialidade do conteúdo cifrado com garantias rigorosas de integridade e autenticidade para a mensagem e seus metadados públicos (AAD), resolvendo o problema da maleabilidade das cifras convencionais.

---

## 1. Contrato do AEAD e Papel dos Parâmetros

A operação AEAD define duas funções conceituais fundamentais:
$$\text{Seal}(K, N, A, M) \longrightarrow (C, T)$$
$$\text{Open}(K, N, A, C, T) \longrightarrow M \text{ ou } \text{falha (InvalidTag)}$$

* **$K$ (Chave secreta):** Mantida sob sigilo absoluto pelas partes. Nunca é transmitida junto ao registro.
* **$N$ (Nonce - *Number used once*):** Valor público que **nunca deve se repetir sob a mesma chave**. Controla o gerador do modo GCM.
* **$A$ ou AAD (*Additional Authenticated Data*):** Dados associados públicos (cabeçalhos, versão, identificador de usuário, sequência). Trafegam em claro para fins de roteamento, mas são **matematicamente autenticados pela tag $T$**. Qualquer alteração no AAD inviabiliza a tag.
* **$M$ (Mensagem clara):** O dado confidencial.
* **$C$ (Texto cifrado):** Protege o sigilo de $M$.
* **$T$ (Etiqueta de autenticação / Tag):** Garante que $A, N, C$ e $K$ concordam perfeitamente.

---

## 2. A Fronteira entre Autenticação Criptográfica e Política da Aplicação

Passar com sucesso por `decrypt()` significa apenas que o pacote é criptograficamente autêntico. A aplicação ainda deve verificar:
1. **Contexto:** Se o usuário autenticado no AAD é aquele para o qual a requisição foi despachada (evita reatribuição de contexto).
2. **Repetição (*Replay Protection*):** A biblioteca AEAD não guarda histórico de mensagens recebidas. A aplicação receptora deve manter um controle durável de sequências já aceitas para impedir que um atacante reenvie um pacote legítimo já transmitido.

---

## 3. Desafio de Fechamento: Projeto de Registro AEAD
Para armazenar uma mensagem estruturada com segurança:
* **O que é guardado/transmitido no registro:**
  * Cabeçalho AAD: `Versão || ID_Remetente || ID_Destinatário || Número_Sequência || Timestamp`
  * Nonce (12 bytes)
  * Texto cifrado $C$
  * Tag de autenticação $T$ (16 bytes)
* **O que é estritamente secreto:** A chave simétrica $K$ (armazenada em cofre/KMS seguro).
* **O que deve ser estritamente único:** O par $(\text{Chave}, \text{Nonce})$. Se o nonce for composto por `ID_Emissor || Contador`, cada emissor deve incrementar monotonicamente o contador de forma durável.

---

## 4. Como Executar os Códigos

### Executar a demonstração:
```bash
python caderno_09_encontro09/atividade_11.py
```

### Executar os testes automatizados:
```bash
python -m unittest discover -s caderno_09_encontro09 -p "test_*.py" -v
```
