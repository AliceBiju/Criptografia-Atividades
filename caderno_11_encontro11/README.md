# Caderno 11 (Encontro 11) — RSA: Da Conta Modular ao Esquema Seguro

## Tema
**Diagnóstico experimental, não apenas ida e volta: RSA didático, maleabilidade e padrões reais (OAEP e PSS)**

Este caderno aborda o funcionamento aritmético da família **RSA**, demonstra por que a exponenciação modular pura (RSA bruto / *textbook RSA*) é determinística e maleável, e como os padrões **RSA-OAEP** e **RSA-PSS** resolvem essas fragilidades em sistemas reais.

---

## 1. Fundamentos Matemáticos do RSA

### Geração de Chaves
1. Escolhem-se dois números primos distintos $p$ e $q$.
2. Calcula-se o módulo público:
   $$n = p \cdot q$$
3. Calcula-se o totiente de Euler:
   $$\phi(n) = (p - 1)(q - 1)$$
4. Escolhe-se um expoente público $e$ coprimo com $\phi(n)$, ou seja, $\gcd(e, \phi(n)) = 1$.
5. Calcula-se o expoente privado $d$ como o inverso modular de $e$ módulo $\phi(n)$:
   $$d \equiv e^{-1} \pmod{\phi(n)} \iff e \cdot d \equiv 1 \pmod{\phi(n)}$$

### Por que a decifração funciona para qualquer representante $0 \le m < n$?
* Se $\gcd(m, n) = 1$, o **Teorema de Euler** assegura que $m^{\phi(n)} \equiv 1 \pmod n$. Como $ed = 1 + k\phi(n)$:
  $$c^d \equiv (m^e)^d = m^{ed} = m \cdot (m^{\phi(n)})^k \equiv m \cdot 1^k \equiv m \pmod n$$
* Se $\gcd(m, n) \ne 1$ (ou seja, $m$ é múltiplo de $p$ ou $q$):
  * Módulo $p$, se $m \equiv 0 \pmod p$, então $m^{ed} \equiv 0 \equiv m \pmod p$.
  * Se $m \not\equiv 0 \pmod p$, pelo **Pequeno Teorema de Fermat**, $m^{p-1} \equiv 1 \pmod p$. Como $p - 1$ divide $\phi(n)$, temos $m^{ed} \equiv m \pmod p$.
  * O mesmo raciocínio vale módulo $q$.
  * Pelo **Teorema Chinês dos Restos (CRT)**, se $m^{ed} \equiv m \pmod p$ e $m^{ed} \equiv m \pmod q$, então $m^{ed} \equiv m \pmod{pq}$.
  * Logo, **todos os $n$ representantes são recuperados com precisão**.

---

## 2. As Duas Falhas Críticas do RSA Bruto (*Textbook RSA*)

1. **Determinismo:**
   A mesma mensagem clara sempre produz o mesmo texto cifrado para uma dada chave pública. Um atacante pode testar palpites de mensagens cifrando-as e comparando com o tráfego interceptado.
2. **Maleabilidade Homomórfica:**
   Multiplicar o texto cifrado $c = m^e \bmod n$ por $r^e \bmod n$ resulta em:
   $$c' = (c \cdot r^e) \bmod n \implies (c')^d \equiv (m \cdot r) \pmod n$$
   O atacante consegue alterar o texto claro resultante de forma multiplicativa sem jamais conhecer a chave privada $d$.

---

## 3. Os Padrões Modernos: OAEP e PSS

* **RSA-OAEP (*Optimal Asymmetric Encryption Padding*):**
  * Codificação probabilística para **cifração**.
  * Adiciona aleatoriedade a cada cifração: duas cifras da mesma mensagem geram saídas completamente distintas.
  * Capacidade máxima de mensagem para chave de $k$ bytes e hash com saída de $hLen$ bytes:
    $$\text{mLen} \le k - 2 \cdot hLen - 2$$
    Para RSA de 2048 bits ($k = 256$ bytes) e SHA-256 ($hLen = 32$ bytes):
    $$256 - 2(32) - 2 = 190 \text{ bytes}$$
    *Mensagens de 191 bytes são rejeitadas com erro.*
* **RSA-PSS (*Probabilistic Signature Scheme*):**
  * Padrão probabilístico para **assinatura digital**.
  * Incorpora um resumo criptográfico da mensagem e um sal aleatório (*salt*), prevenindo ataques de forja existencial.
  * A verificação é booleana por ausência de exceção (`verify()` bem-sucedido ou `InvalidSignature`).

---

## 4. Como Executar os Códigos

### Executar a demonstração:
```bash
python caderno_11_encontro11/atividade_11.py
```

### Executar os testes automatizados:
```bash
python -m unittest discover -s caderno_11_encontro11 -p "test_*.py" -v
```
