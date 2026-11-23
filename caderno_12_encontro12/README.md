# Caderno 12 (Encontro 12) — Diffie–Hellman e ElGamal: Acordo, Cifração e Limites

## Tema
**Laboratório: um acordo correto pode ser inseguro**

Este caderno investiga a fundamentação algébrica do acordo de chaves **Diffie-Hellman (DH)** e da cifração **ElGamal** sobre subgrupos de ordem prima, auditando a fronteira crítica entre **correção matemática, validação de chaves públicas e autenticação de identidade**.

---

## 1. O Subgrupo Cíclico Didático
* **Parâmetros:** $p = 23$ (primo), $q = 11$ (ordem prima do subgrupo), $g = 2$ (gerador).
* Subgrupo gerado por potências de 2:
  $$G = \{1, 2, 3, 4, 6, 8, 9, 12, 13, 16, 18\}$$
* **Regras de Validação de Chave Pública (`validar(y)`):**
  1. Deve ser do tipo inteiro puro (rejeita `bool`, `float`, etc.);
  2. Faixa válida: $2 \le y \le p - 2$ (o valor 1 é a identidade trivial e $22 \equiv -1$ tem ordem 2, fora do subgrupo de ordem 11);
  3. Pertencimento ao subgrupo: $y^q \equiv 1 \pmod p$ (como $q=11$ é primo, qualquer elemento não-identidade que satisfaz essa congruência gera o subgrupo de ordem $q$).

---

## 2. Acordo Diffie-Hellman Auditado (`acordo_auditado(a, b)`)
* Privadas $a, b \in \{1, \dots, 10\}$.
* Públicas calculadas: $A = g^a \bmod p$ e $B = g^b \bmod p$.
* Ambas as públicas são validadas pela função `validar()`.
* Segredos locais compartilhados:
  $$s_A = B^a \bmod p = (g^b)^a \equiv g^{ab} \pmod p$$
  $$s_B = A^b \bmod p = (g^a)^b \equiv g^{ab} \pmod p$$
* Contrato testado: para $a = 2, b = 5$:
  $$A = 2^2 = 4, \quad B = 2^5 = 9, \quad s_A = 9^2 \equiv 12, \quad s_B = 4^5 \equiv 12 \pmod{23}$$

---

## 3. O que a Enumeração dos 100 Pares Prova e o que NÃO Prova
* **O que prova:** Prova a **correção funcional** da álgebra sobre todos os pares de entradas do domínio didático ($s_A == s_B$ para todos os 100 pares possíveis de $1 \le a, b \le 10$).
* **O que NÃO prova:**
  1. Não prova que o sistema é seguro contra adversários ativos (MITM);
  2. Não prova resistência contra ataque de subgrupo pequeno em parâmetros reais;
  3. Não prova autenticidade de quem enviou os valores.

---

## 4. O Intermediário Mallory e a Falha da Validação Pura
* No ataque simulado:
  * Mallory intercepta a troca e injeta suas próprias públicas $U = 2$ para Alice e $V = 4$ para Bob.
  * $U$ e $V$ **passam com louvor pela validação matemática** (`validar(U) is True`, `validar(V) is True`), pois são elementos legítimos do subgrupo gerado por $g=2$.
  * Alice e Bob calculam segredos válidos com Mallory, e Mallory consegue ler todo o tráfego.
* **Conclusão Teórica:** Validação matemática de parâmetros responde apenas: *"Este número é um elemento matematicamente aceitável do subgrupo?"*. Ela **NÃO responde**: *"Este número realmente pertence a Bob?"*. A autenticação da origem requer credenciais confiáveis (certificados, assinaturas digitais da negociação).

---

## 5. Como Executar os Códigos

### Executar a demonstração:
```bash
python caderno_12_encontro12/atividade_11.py
```

### Executar os testes automatizados:
```bash
python -m unittest discover -s caderno_12_encontro12 -p "test_*.py" -v
```
