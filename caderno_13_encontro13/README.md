# Caderno 13 (Encontro 13) — Curvas Elípticas: Das Contas ao Acordo de Chaves

## Tema
**Curvas elípticas sobre corpos finitos ($\mathbb{F}_p$), soma de pontos, multiplicação escalar e acordo ECDH**

Este encontro introduz os fundamentos matemáticos e algorítmicos da **Criptografia de Curvas Elípticas (ECC)**. Em vez de operar com potências modulares sobre inteiros, operamos com **pontos geométricos** sobre um corpo finito $\mathbb{F}_{17}$ que formam um grupo abeliano sob uma lei de soma específica.

---

## 1. Definição da Curva Didática

Usamos a equação de Weierstrass curta:
$$E : y^2 \equiv x^3 + 2x + 2 \pmod{17}$$

* **Parâmetros:** $p = 17$, $a = 2$, $b = 2$.
* **Não singularidade:** Exige $4a^3 + 27b^2 \not\equiv 0 \pmod p$.
  $$4(2)^3 + 27(2)^2 = 32 + 108 = 140 \equiv 4 \not\equiv 0 \pmod{17} \quad (\text{curva não singular})$$
* **Conjunto de Pontos:** A curva possui 18 pontos afins com coordenadas em $\{0, \dots, 16\}$ mais o **ponto no infinito ($\mathcal{O}$)**, totalizando 19 elementos.
* **Ponto-base:** $G = (5, 1)$ com ordem prima $n = 19$, o que significa que $19G = \mathcal{O}$ e $G$ gera todo o grupo.

---

## 2. A Lei de Grupo: Regras de Soma de Pontos

Dado $P = (x_P, y_P)$ e $Q = (x_Q, y_Q)$ em $E$:

1. **Elemento Neutro ($\mathcal{O}$):**
   $$P + \mathcal{O} = P \quad \text{e} \quad \mathcal{O} + Q = Q$$
2. **Ponto Oposto (Inverso Aditivo):**
   $$-P = (x_P, -y_P \bmod 17)$$
   Se $x_P = x_Q$ e $y_P + y_Q \equiv 0 \pmod{17}$, então $P + Q = \mathcal{O}$.
3. **Duplicação de Ponto ($P = Q$ com $y_P \ne 0$):**
   $$\lambda = \frac{3x_P^2 + a}{2y_P} \equiv (3x_P^2 + 2) \cdot (2y_P)^{-1} \pmod{17}$$
   $$x_R = \lambda^2 - 2x_P \pmod{17}$$
   $$y_R = \lambda(x_P - x_R) - y_P \pmod{17}$$
4. **Soma de Pontos Distintos ($x_P \ne x_Q$):**
   $$\lambda = \frac{y_Q - y_P}{x_Q - x_P} \equiv (y_Q - y_P) \cdot (x_Q - x_P)^{-1} \pmod{17}$$
   $$x_R = \lambda^2 - x_P - x_Q \pmod{17}$$
   $$y_R = \lambda(x_P - x_R) - y_P \pmod{17}$$

---

## 3. Algoritmo Duplicar e Somar (*Double-and-Add*)

Para calcular a multiplicação escalar $kP$ de forma eficiente ($O(\log k)$):
1. Inicia `resultado = None` ($\mathcal{O}$) e `atual = P`.
2. Para cada bit de $k$:
   * Se $k$ for ímpar ($k \pmod 2 = 1$), acumula: `resultado = somar(resultado, atual)`.
   * Duplica o ponto atual: `atual = somar(atual, atual)`.
   * Divide $k$ por 2: `k = k // 2`.
3. Invariante: a relação $\text{resultado} + k \cdot \text{atual} = k_{original} \cdot P$ mantém-se constante em cada iteração.

---

## 4. Acordo de Chaves ECDH e Ataque ECDLP

### Acordo ECDH (Exemplo 6)
* Alice guarda o escalar privado $s_A = 2$ e publica $A = 2G = (6, 3)$.
* Bob guarda o escalar privado $s_B = 3$ e publica $B = 3G = (10, 6)$.
* Alice calcula $S_A = s_A \cdot B = 2 \cdot (10, 6) = (16, 13)$.
* Bob calcula $S_B = s_B \cdot A = 3 \cdot (6, 3) = (16, 13)$.
* **Ambos chegam ao mesmo segredo compartilhado $(16, 13)$ sem transmiti-lo**.

### O Problema do Logaritmo Discreto em Curvas Elípticas (ECDLP)
* **Direto:** Dado $k$ e $G$, calcular $Q = kG$ é rápido e computacionalmente fácil.
* **Inverso (ECDLP):** Dado $G$ e $Q = kG$, encontrar $k$ é intratável em curvas criptográficas reais ($n \approx 2^{256}$).
* **Na curva didática pequena ($n = 19$):** Um adversário enumera $1G, 2G, 3G, \dots$ e quebra a chave privada de Bob $s_B = 3$ em apenas 3 tentativas, demonstrando por que parâmetros de brinquedo não oferecem segurança real.

---

## 5. Respostas da Lista de Atividades (Questões 1 a 10)

1. **(0, 6) pertence a $E$?**
   * Lado esquerdo: $y^2 = 6^2 = 36 \equiv 2 \pmod{17}$.
   * Lado direito: $x^3 + 2x + 2 = 0^3 + 2(0) + 2 = 2 \pmod{17}$.
   * Ambos coincidem ($2 \equiv 2$). **Pertence!**
2. **(1, 1) pertence a $E$?**
   * $y^2 = 1^2 = 1 \pmod{17}$.
   * $x^3 + 2x + 2 = 1 + 2 + 2 = 5 \pmod{17}$.
   * A comparação falha pois $1 \not\equiv 5 \pmod{17}$. **Não pertence!**
3. **Multiplicação escalar vs multiplicação de coordenadas:**
   * Multiplicação escalar $kP$ é a **soma iterada do ponto $P$ consigo mesmo $k$ vezes** segundo a lei de grupo.
   * Não é multiplicar as coordenadas: $2G = (6, 3)$, enquanto o dobro das coordenadas seria $(2 \cdot 5, 2 \cdot 1) = (10, 2)$, ponto que sequer pertence à curva ($2^2 = 4 \ne 10^3 + 20 + 2 \equiv 2$).
4. **Associação de mecanismos:**
   * **X25519:** *"Eu o usaria para acordo de chaves Diffie-Hellman moderno de alto desempenho."*
   * **ECDSA:** *"Eu o usaria para gerar assinaturas digitais em infraestruturas baseadas em curvas NIST."*
   * **Ed25519:** *"Eu o usaria para assinaturas digitais rápidas, seguras contra canais laterais e imunes a falhas de gerador de nonce."*
5. **Risco de reuso de nonce secreto em ECDSA:**
   * O nonce $k$ de uma assinatura ECDSA precisa ser estritamente secreto e único por assinatura. Reutilizar o mesmo $k$ para duas mensagens diferentes permite eliminar a incógnita e **recuperar a chave privada do assinante diretamente**. Logo, nem todo nonce é público!
6. **Por que o ponto no infinito ($\mathcal{O}$) é necessário?**
   * $\mathcal{O}$ é o **elemento neutro da adição**. Ele garante que a soma de dois pontos opostos $P + (-P)$ tenha um resultado bem definido dentro do grupo e preserva a estrutura de grupo abeliano.
7. **Multiplicar coordenadas produz $kP$?**
   * Não. Para $G = (5, 1)$, $2G = (6, 3)$. Multiplicar coordenadas daria $(10, 2)$, que não satisfaz a equação $y^2 \equiv x^3 + 2x + 2 \pmod{17}$.
8. **X25519 pode ser usada como assinatura?**
   * Não. X25519 é uma função de acordo de chaves baseada na representação escalar na curva Montgomery Curve25519. Para assinar documentos, deve-se usar um esquema de assinatura digital, como **Ed25519** ou **ECDSA**.
9. **Ligar pontos e medir inclinação em gráfico discreto?**
   * Incorreto. No corpo finito $\mathbb{F}_p$, não há continuidade nem retas euclidianas. As fórmulas analíticas de adição são uma transposição formal da geometria contínua para a aritmética modular, onde a divisão real é substituída pelo **inverso multiplicativo modular**.
10. **Mapa conceitual (ligações essenciais):**
    * Ponto $\xrightarrow{\text{pertence à}}$ Curva Elíptica.
    * Lei de Grupo $\xrightarrow{\text{define a}}$ Soma de Pontos.
    * Ponto no Infinito $\xrightarrow{\text{atua como}}$ Elemento Neutro da Soma.
    * Soma Repetida $\xrightarrow{\text{constrói a}}$ Multiplicação Escalar.
    * Multiplicação Escalar $\xrightarrow{\text{gera a}}$ Chave Pública a partir da Privada.
    * Dificuldade de Inversão $\xrightarrow{\text{sustenta a segurança do}}$ Acordo ECDH.

---

## 6. Como Executar os Códigos

### Executar a demonstração interativa:
```bash
python caderno_13_encontro13/atividade_11.py
```
*(ou `python caderno_13_encontro13/curva13.py`)*

### Executar os testes automatizados deste caderno:
```bash
python -m unittest discover -s caderno_13_encontro13 -p "test_*.py" -v
```
