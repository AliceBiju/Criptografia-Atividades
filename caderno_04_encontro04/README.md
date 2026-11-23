# Caderno 04 (Encontro 04) — Cifras de Fluxo e One-Time Pad

## Tema
**Reutilização de fluxo e quebra do sigilo**

Neste caderno são investigadas as propriedades teóricas e práticas das cifras de fluxo e do One-Time Pad (OTP), demonstrando matematicamente por que a reutilização de um mesmo fluxo de chave (*keystream*) causa uma falha catastrófica de confidencialidade (ataque *Two-Time Pad*) e por que cifras de fluxo lineares são maleáveis.

---

## 1. Fundamentos Teóricos

### Condições Estritas do One-Time Pad (OTP)
Para que uma cifra alcance **sigilo perfeito** (segundo Shannon), o fluxo de chave $S$ deve satisfazer:
1. Ser **estatisticamente independente** da mensagem clara $M$;
2. Ter **distribuição perfeitamente uniforme**;
3. Ter **tamanho pelo menos igual** ao da mensagem ($|S| \ge |M|$);
4. Ser mantido em **estrito segredo** e **NUNCA ser reutilizado** ("one-time").

Sob essas condições, observar o texto cifrado $C = M \oplus S$ não altera a distribuição de probabilidade a priori de nenhuma mensagem candidata $M^*$, pois para qualquer $M^*$ existe exatamente uma chave compatível $S^* = C \oplus M^*$.

### O Desastre do *Two-Time Pad* (Reutilização de Fluxo)
Se o mesmo fluxo $S$ for utilizado para cifrar duas mensagens distintas $M_1$ e $M_2$:
$$C_1 = M_1 \oplus S$$
$$C_2 = M_2 \oplus S$$

Um observador passivo no canal simplesmente calcula o XOR entre os dois textos cifrados:
$$C_1 \oplus C_2 = (M_1 \oplus S) \oplus (M_2 \oplus S) = M_1 \oplus M_2 \oplus (S \oplus S) = M_1 \oplus M_2$$

O fluxo $S$ **desaparece completamente** da equação! A partir desse ponto:
* Conhecendo uma mensagem $M_1$ (ou partes/cabeçalhos previsíveis dela), recupera-se a outra:
  $$M_2 = (C_1 \oplus C_2) \oplus M_1$$
* Técnicas de arrasto de palavras (*crib dragging*) permitem recuperar ambas as mensagens mesmo sem conhecer $M_1$ previamente.

### Maleabilidade do XOR
O XOR é uma operação linear. Se um adversário altera um bit de $C$ por uma máscara $\Delta$:
$$C' = C \oplus \Delta \implies M' = C' \oplus S = (C \oplus S) \oplus \Delta = M \oplus \Delta$$
O bit correspondente no texto claro é invertido de forma previsível, sem que o atacante precise saber o texto original ou a chave. Por essa razão, **cifras de fluxo exigem autenticação** (como em construções AEAD do tipo ChaCha20-Poly1305).

---

## 2. Desafio de Fechamento: Frases de Livro no OTP
* **Pergunta:** Por que usar uma frase de livro como fluxo do OTP não preserva o sigilo perfeito, mesmo que a frase nunca se repita?
* **Resposta:** Porque viola a exigência de **distribuição uniforme e independência estatística**. A linguagem natural tem redundância e baixa entropia (~1.0 a 1.5 bits/caractere contra os 8 bits ideais). Padrões gramaticais, espaçamento e frequência de letras vazam informações cruciais sobre $M$.

---

## 3. Como Executar os Códigos

### Executar a demonstração:
```bash
python caderno_04_encontro04/atividade_11.py
```

### Executar os testes automatizados:
```bash
python -m unittest discover -s caderno_04_encontro04 -p "test_*.py" -v
```
