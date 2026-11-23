# Caderno 08 (Encontro 08) — Modos de Operação

## Tema
**Laboratório de modos reversíveis (CBC e CTR) e limites de contador**

Uma cifra de bloco transforma blocos de tamanho fixo (ex: 128 bits no AES). Para proteger mensagens longas ou arquivos, é indispensável utilizar um **modo de operação**. Este caderno compara os modos **ECB, CBC e CTR**, implementando e auditando suas propriedades funcionais e seus limites de segurança.

---

## 1. Comparação entre Modos de Operação

| Propriedade | ECB (*Electronic Codebook*) | CBC (*Cipher Block Chaining*) | CTR (*Counter*) |
| :--- | :---: | :---: | :---: |
| **Cifração paralela** | ✅ Sim | ❌ Não (dependência sequencial de $C_{i-1}$) | ✅ Sim ($T_i$ independe dos blocos) |
| **Decifração paralela** | ✅ Sim | ✅ Sim ($C_i$ e $C_{i-1}$ estão disponíveis) | ✅ Sim |
| **Tratamento de tamanho** | Requer preenchimento (ex: PKCS #7) | Requer preenchimento (PKCS #7) | **Sem preenchimento** (trunca o fluxo) |
| **Valor Inicial** | Nenhum | **IV imprevisível** (aleatório) | **Nonce único + contador** |
| **Autenticidade própria**| ❌ Não | ❌ Não | ❌ Não (maleável) |
| **Vazamento de padrão** | ⚠️ Crítico (blocos iguais geram cifras iguais) | Protegido pelo encadeamento e IV | Protegido pelo fluxo de chave pseudoaleatório |

---

## 2. Equações e Mecânica

### Modo CBC
* **Cifração:** $C_0 = IV$, e para cada bloco:
  $$C_i = E_K(M_i \oplus C_{i-1})$$
* **Decifração:**
  $$M_i = D_K(C_i) \oplus C_{i-1}$$
  *Observe que o XOR na decifração ocorre após a função $D_K$.*

### Modo CTR
* Transforma a cifra de bloco em uma cifra de fluxo:
  $$T_i = \text{Nonce} \parallel \text{Contador}_i$$
  $$S_i = E_K(T_i) \quad (\text{fluxo de chave})$$
  $$C_i = M_i \oplus S_i$$
* **Decifração em CTR:** A recuperação **não usa $D_K$**! Usa a mesma função $E_K$ sobre o mesmo contador:
  $$M_i = C_i \oplus S_i = (M_i \oplus S_i) \oplus S_i = M_i$$

### Limite e Esgotamento do Contador
* Se um contador atinge seu valor máximo, ele **nunca deve dar a volta (*wrap-around*) silenciosamente**, pois reiniciar o contador sob o mesmo nonce e chave reproduz o fluxo, gerando uma vulnerabilidade fatal de *Two-Time Pad*.
* O código implementado valida e rejeita estritamente qualquer tentativa que exceda a capacidade do contador.

---

## 3. Desafio de Fechamento: O Ataque *Padding Oracle*
* **Cenário:** Um sistema que usa AES-CBC informa respostas ou mensagens de erro distintas para "preenchimento PKCS #7 inválido" e "senha/dados incorretos".
* **Risco:** O adversário manipula os bytes do penúltimo bloco cifrado $C_{k-1}$ e envia ao servidor. Observando se a resposta acusou falha de preenchimento ou não, o atacante descobre o byte decifrado intermediário, permitindo recuperar todo o texto claro bloco por bloco sem jamais conhecer a chave AES.
* **Correção:** Substituir modos não autenticados por **Cifração Autenticada com Dados Associados (AEAD)**, como **AES-GCM** ou **ChaCha20-Poly1305**, onde qualquer alteração no texto cifrado ou preenchimento resulta na rejeição imediata da etiqueta sem fornecer pistas de temporização ou oráculo de erro.

---

## 4. Como Executar os Códigos

### Executar a demonstração:
```bash
python caderno_08_encontro08/atividade_11.py
```

### Executar os testes automatizados:
```bash
python -m unittest discover -s caderno_08_encontro08 -p "test_*.py" -v
```
