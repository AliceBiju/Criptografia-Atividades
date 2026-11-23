# Caderno 03 (Encontro 03) — Cifras Clássicas e Análise de Frequência

## Tema
**Cifra de César e ataque por busca**

Este encontro explora cifras clássicas baseadas em substituição e transposição, demonstrando por que um espaço de chaves pequeno ou a preservação de estruturas estatísticas da linguagem natural tornam esses sistemas vulneráveis à criptoanálise.

---

## 1. Fundamentos Teóricos

### Cifra de César
* Transformação monoalfabética que aplica um deslocamento constante $k$ sobre cada letra:
  $$E_k(x) = (x + k) \pmod{26}$$
  $$D_k(y) = (y - k) \pmod{26}$$
* O espaço de chaves é de apenas 26 valores possíveis ($k \in \{0, \dots, 25\}$).
* A busca exaustiva (força bruta) é trivial e imediata.

### Por que espaços grandes não bastam sozinhos?
* Em uma **substituição monoalfabética arbitrária**, o número de chaves é $26! \approx 4 \times 10^{26}$, o que inviabiliza a busca exaustiva.
* No entanto, a cifra **preserva a frequência das letras**: se a letra 'A' é a mais comum no português, o símbolo que substitui 'A' também será o mais comum no texto cifrado.
* A redundância do idioma (frequência de letras, digramas, palavras comuns como "DE", "QUE", "AO") permite quebrar a cifra sem testar todas as chaves.

### Transposição vs Substituição
* **Substituição:** Altera os símbolos, mas preserva a ordem/posição.
* **Transposição:** Preserva os símbolos exatos (e suas contagens absolutas), mas altera suas posições relativas.
* A combinação de substituição com transposição estabelece as bases dos conceitos de **confusão** e **difusão** formalizados por Claude Shannon para cifras modernas.

---

## 2. Implementação e Ataque Estatístico

1. **`cesar(texto, chave)`**: Desloca letras módulo 26, preservando pontuações e espaços.
2. **`decifrar(texto, chave)`**: Reutiliza `cesar` com deslocamento `-chave`.
3. **`candidatas(texto_cifrado)`**: Retorna todas as 26 decifrações possíveis.
4. **`ordenar_candidatas(texto_cifrado)`**: Aplica uma heurística linguística baseada nas frequências relativas do português e presença de palavras frequentes, colocando o texto claro autêntico no topo do ranking.
5. **Desafio de Fechamento**: Implementa uma cifra híbrida clássica composta (César + Transposição colunar em duas colunas).

---

## 3. Como Executar os Códigos

### Executar a demonstração:
```bash
python caderno_03_encontro03/atividade_11.py
```

### Executar os testes automatizados:
```bash
python -m unittest discover -s caderno_03_encontro03 -p "test_*.py" -v
```
