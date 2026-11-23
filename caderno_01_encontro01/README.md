# Caderno 01 (Encontro 01) — Fundamentos e Objetivos da Criptografia

## Tema
**Ataque a uma transferência: SHA-256 versus HMAC**

Este caderno introduz os princípios basilares da segurança da informação e diferencia mecanismos de resumo público (hash) de mecanismos de autenticação com chave simétrica (MAC/HMAC).

---

## 1. Resumo Conceitual e Teórico

### A Tríade e as Propriedades de Segurança
* **Confidencialidade:** Garante que o conteúdo seja acessível apenas por partes autorizadas. Nem SHA-256 nem HMAC fornecem confidencialidade (a mensagem trafega legível).
* **Integridade:** Permite detectar qualquer alteração acidental ou intencional nos dados.
* **Autenticidade:** Fornece garantia sobre a origem da mensagem (quem a produziu).
* **Não Repúdio:** Impede que o autor negue a autoria da mensagem perante terceiros. HMAC **não** oferece não repúdio perante árbitros externos, pois ambas as partes compartilham a mesma chave simétrica e qualquer uma delas pode gerar etiquetas idênticas.

### Princípio de Kerckhoffs
A segurança de um sistema criptográfico não deve depender do sigilo do algoritmo (segurança por obscuridade), mas unicamente do sigilo da chave. Tanto SHA-256 quanto HMAC são algoritmos públicos, padronizados e amplamente auditados.

---

## 2. Comparativo de Propriedades

| Mecanismo | Confidencialidade | Integridade contra Atacante Ativo | Autenticidade | Não Repúdio |
| :--- | :---: | :---: | :---: | :---: |
| **SHA-256 puro** | ❌ Não | ❌ Não (atacante recalcula o hash) | ❌ Não | ❌ Não |
| **HMAC-SHA-256** | ❌ Não | ✅ Sim (exige posse da chave secreta) | ✅ Sim (entre quem tem a chave) | ❌ Não (chave simétrica) |

---

## 3. Explicação do Ataque e da Defesa

1. **Ataque ao SHA-256:**
   * Alice envia para o banco: `M = "destino=ana;valor=100"` acompanhado de `H = SHA256(M)`.
   * Mallory intercepta a mensagem no canal, altera para `M' = "destino=ana;valor=900"` e simplesmente recalcula `H' = SHA256(M')`.
   * O banco verifica se `SHA256(M') == H'`. Como coincidem, aceita a transação fraudada!
   * **Conclusão:** Hash sem chave detecta corrupção acidental em rede (ruído), mas **não protege** contra adversários ativos.

2. **Defesa com HMAC:**
   * Alice e o Banco compartilham uma chave secreta $K$.
   * Alice envia `M` acompanhado de `T = HMAC(K, M)`.
   * Mallory altera para `M'`. Para convencer o Banco, precisaria gerar `T' = HMAC(K, M')`.
   * Como Mallory não conhece $K$, qualquer etiqueta gerada com sua própria chave $K_{atacante}$ resultará em discrepância no banco:
     $$\text{HMAC}(K, M') \ne \text{HMAC}(K_{atacante}, M')$$
   * A mensagem adulterada é imediatamente **rejeitada**.

---

## 4. Como Executar os Códigos

### Executar a demonstração interativa:
```bash
python caderno_01_encontro01/atividade_11.py
```

### Executar os testes automatizados:
```bash
python -m unittest discover -s caderno_01_encontro01 -p "test_*.py" -v
```
