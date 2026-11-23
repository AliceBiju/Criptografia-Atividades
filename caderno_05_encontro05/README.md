# Caderno 05 (Encontro 05) — Cifras de Bloco e Redes de Feistel

## Tema
**Rede de Feistel reversível**

Este caderno estuda a arquitetura de **Rede de Feistel**, demonstrando como transformar um bloco de bits através de rodadas iterativas que garantem **inversibilidade matemática** mesmo quando a função interna de rodada $F$ não é inversível por si só.

---

## 1. Fundamentos Teóricos

### Estrutura de Feistel
O bloco de entrada de $n$ bits é dividido em duas metades de $n/2$ bits: $L$ (esquerda) e $R$ (direita).
A cada rodada $i$ com subchave $K_i$:
$$L_{i} = R_{i-1}$$
$$R_{i} = L_{i-1} \oplus F(R_{i-1}, K_i)$$

### Por que a decifração funciona sem inverter $F$?
Para reverter uma rodada:
1. $R_{i-1}$ é recuperado imediatamente de $L_i$, pois $L_i = R_{i-1}$.
2. Com $R_{i-1}$ em mãos, recalculamos a **mesma** função $F(R_{i-1}, K_i)$ (não precisamos de $F^{-1}$!).
3. Aplicamos XOR novamente com $R_i$:
   $$R_i \oplus F(R_{i-1}, K_i) = (L_{i-1} \oplus F(R_{i-1}, K_i)) \oplus F(R_{i-1}, K_i) = L_{i-1}$$
4. Na decifração de múltiplas rodadas, basta percorrer as subchaves na **ordem estritamente inversa**:
   $$K_r, K_{r-1}, \dots, K_1$$

### Reversibilidade vs Segurança Criptográfica
* **Inversibilidade é um requisito funcional**, não uma prova de segurança.
* Uma rede Feistel com uma função $F$ constante ou linear (ou com poucas rodadas) é perfeitamente reversível, porém **completamente insegura** contra criptoanálise linear e diferencial.
* Cifras reais (como o DES) utilizam S-boxes não lineares e permutações de expansão em $F$ ao longo de 16 rodadas para alcançar **confusão** e **difusão**.

### Efeito Avalanche
Mede a propagação de alterações: ao mudar 1 bit na entrada, espera-se que cerca de 50% dos bits de saída sofram alteração após todas as rodadas.

---

## 2. Desafio de Fechamento: Função $F$ fraca
* **Proposta:** Considere $F(R, K) = 0$ (ou $F(R, K) = R \oplus K$, estritamente linear).
* **Consequência:** A cada duas rodadas, a transformação torna-se uma simples permutação de metades com XOR de chaves. Equações algébricas lineares relacionando entrada e saída podem ser resolvidas com poucos pares de texto claro/cifrado conhecido (via Eliminação Gaussiana), quebrando a chave sem necessidade de força bruta.

---

## 3. Como Executar os Códigos

### Executar a demonstração:
```bash
python caderno_05_encontro05/atividade_11.py
```

### Executar os testes automatizados:
```bash
python -m unittest discover -s caderno_05_encontro05 -p "test_*.py" -v
```
