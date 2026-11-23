# Caderno 02 (Encontro 02) — Aritmética Modular, XOR e Aleatoriedade

## Tema
**Inverso modular, XOR e aleatoriedade**

Neste encontro, são implementadas as três operações elementares mais recorrentes na criptografia clássica e moderna:
1. **Aritmética modular e inversão** (via Algoritmo de Euclides Estendido);
2. **Operação XOR** sobre bytes e suas propriedades de autoinversão;
3. **Aleatoriedade segura e gestão de nonces** com a biblioteca padrão `secrets`.

---

## 1. Fundamentos Matemáticos

### Algoritmo de Euclides Estendido
Para quaisquer inteiros $a$ e $b$, existem inteiros $x$ e $y$ tais que:
$$a \cdot x + b \cdot y = \gcd(a, b)$$
Quando $\gcd(a, n) = 1$, reduzindo a equação módulo $n$, temos:
$$a \cdot x + n \cdot y \equiv a \cdot x \equiv 1 \pmod n$$
Portanto, $x \pmod n$ é o inverso multiplicativo de $a$ módulo $n$. Se $\gcd(a, n) \ne 1$, o inverso **não existe**.

### O papel do XOR ($\oplus$)
O XOR bit a bit possui três propriedades fundamentais:
* $x \oplus x = 0$ (qualquer valor operado consigo mesmo se anula)
* $x \oplus 0 = x$ (o zero é o elemento neutro)
* $(m \oplus k) \oplus k = m \oplus (k \oplus k) = m \oplus 0 = m$ (reversão direta com a mesma chave)

### Aleatoriedade, Chave, Nonce e Salt
* **Chave:** Deve ser **secreta** e possuir alta **entropia** (imprevisível).
* **Nonce (*Number used once*):** Não precisa ser secreto, mas deve ser estritamente **único** sob a mesma chave.
* **Salt:** Dado público, distinto por registro, usado para evitar tabelas pré-computadas (Rainbow Tables).

---

## 2. Resolução do Desafio
Encontrar $x$ tal que $17x \equiv 1 \pmod{43}$:
* Como 43 é primo e $\gcd(17, 43) = 1$, o inverso é único módulo 43.
* Pelo Algoritmo de Euclides:
  $$43 = 2 \times 17 + 9$$
  $$17 = 1 \times 9 + 8$$
  $$9 = 1 \times 8 + 1 \implies 1 = 9 - 1 \times 8$$
* Substituindo os restos:
  $$1 = 9 - (17 - 9) = 2 \times 9 - 17 = 2(43 - 2 \times 17) - 17 = 2 \times 43 - 5 \times 17$$
  $$-5 \times 17 \equiv 1 \pmod{43} \implies x \equiv -5 \equiv 38 \pmod{43}$$
* Verificação: $17 \times 38 = 646 = 15 \times 43 + 1 \equiv 1 \pmod{43}$.

---

## 3. Como Executar os Códigos

### Executar a demonstração:
```bash
python caderno_02_encontro02/atividade_11.py
```

### Executar os testes automatizados:
```bash
python -m unittest discover -s caderno_02_encontro02 -p "test_*.py" -v
```
