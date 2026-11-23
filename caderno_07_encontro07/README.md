# Caderno 07 (Encontro 07) — Advanced Encryption Standard (AES)

## Tema
**Multiplicação no corpo finito do AES ($GF(2^8)$) e transformação MixColumns**

Este caderno desenvolve a base matemática da álgebra interna do AES: a representação de bytes como polinômios sobre o corpo finito $GF(2^8)$ e a operação de difusão de colunas (*MixColumns*).

---

## 1. Fundamentos Matemáticos

### O Corpo Finito $GF(2^8)$ no AES
* Um byte $(b_7 b_6 b_5 b_4 b_3 b_2 b_1 b_0)_2$ representa o polinômio:
  $$b(x) = b_7 x^7 + b_6 x^6 + b_5 x^5 + b_4 x^4 + b_3 x^3 + b_2 x^2 + b_1 x + b_0$$
* **Soma e Subtração:** São a mesma operação — o XOR dos coeficientes módulo 2 (sem transporte de bits).
* **Multiplicação:** É a multiplicação usual de polinômios seguida pela redução pelo polinômio irredutível padronizado pelo NIST (FIPS 197):
  $$m(x) = x^8 + x^4 + x^3 + x + 1 \quad (\text{hex: } 0x11B)$$

### A Função `xtime`
Multiplicar por $x$ (byte `0x02`):
1. Desloca o byte 1 posição à esquerda (`valor << 1`).
2. Se o bit $b_7$ original era 0, o resultado cabe em 8 bits.
3. Se $b_7$ era 1, surge o termo $x^8$, que deve ser reduzido por $x^8 \equiv x^4 + x^3 + x + 1$ (ou seja, XOR com `0x1B` nos 8 bits baixos).

### Multiplicação Geral `gf_mul(a, b)`
Decompõe-se o multiplicador $b$ em seus 8 bits. Para cada bit ativo na posição $i$, soma-se (via XOR) a parcela correspondente de $a \cdot x^i$, calculada iterativamente com `xtime`.

---

## 2. A Transformação MixColumns
A etapa *MixColumns* do AES multiplica cada coluna do estado de $4 \times 4$ bytes pela matriz circulante MDS:
$$\begin{bmatrix} s'_{0,c} \\ s'_{1,c} \\ s'_{2,c} \\ s'_{3,c} \end{bmatrix} = \begin{bmatrix} 02 & 03 & 01 & 01 \\ 01 & 02 & 03 & 01 \\ 01 & 01 & 02 & 03 \\ 03 & 01 & 01 & 02 \end{bmatrix} \begin{bmatrix} s_{0,c} \\ s_{1,c} \\ s_{2,c} \\ s_{3,c} \end{bmatrix}$$

* Multiplicar por `01` preserva o byte.
* Multiplicar por `02` usa `xtime`.
* Multiplicar por `03` é calculado como $(02 \cdot a) \oplus a = \text{xtime}(a) \oplus a$.

---

## 3. Desafio de Fechamento: Reuso de Nonce em AES-GCM
* **Pergunta:** Como o reuso de nonce em AES-GCM pode ser catastrófico sem que o algoritmo AES seja quebrado?
* **Resposta:** O GCM utiliza AES no modo CTR para cifração e o autenticador GMAC (baseado em multiplicação polinomial em $GF(2^{128})$ com chave de hash $H = E_K(0)$) para a tag de integridade.
  * O reuso de nonce sob a mesma chave causa um *Two-Time Pad* no modo CTR (expondo o XOR dos textos claros).
  * Além disso, duas etiquetas produzidas com o mesmo nonce permitem ao atacante resolver uma equação polinomial e **recuperar a chave interna de autenticação $H$**, permitindo forjar etiquetas arbitrárias para qualquer mensagem futura, mesmo com a chave AES primária intocada.

---

## 4. Como Executar os Códigos

### Executar a demonstração:
```bash
python caderno_07_encontro07/atividade_11.py
```

### Executar os testes automatizados:
```bash
python -m unittest discover -s caderno_07_encontro07 -p "test_*.py" -v
```
