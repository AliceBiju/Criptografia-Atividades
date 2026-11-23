# Caderno 06 (Encontro 06) — DES, 3DES e Lições de Projeto

## Tema
**Estimador de busca exaustiva e lições de projeto**

Neste caderno, quantificamos a força de segurança de cifras de bloco simétricas históricas e modernas (DES, 3DES, AES), analisando o impacto do tamanho de chave, da taxa de teste e do paralelismo de hardware na viabilidade de ataques de força bruta.

---

## 1. Fundamentos Teóricos e Análise de Segurança

### Chave de 64 bits vs 56 bits efetivos no DES
* A chave informada ao DES possui 64 bits (8 bytes).
* No entanto, o último bit de cada byte é um **bit de paridade** (usado para detecção de falha de hardware).
* Apenas $8 \times 7 = 56$ bits são variáveis e secretos.
* O espaço de busca tem apenas $2^{56}$ chaves, e na média requer $2^{55}$ tentativas.
* A $10^{12}$ testes/segundo:
  $$t_{médio} = \frac{2^{55}}{10^{12}} \approx 36.029 \text{ segundos} \approx 10{,}0 \text{ horas}$$
* Em 1998, a EFF (*Deep Crack*) quebrou uma chave DES em 56 horas, comprovando a obsolescência prática da cifra.

### Por que o 3DES tem ~112 bits de segurança e não 168 bits?
* O Triple DES utiliza 3 chaves de 56 bits na sequência $C = E_{K3}(D_{K2}(E_{K1}(P)))$, totalizando 168 bits de material de chave.
* Contudo, um ataque de **Encontro no Meio (*Meet-in-the-Middle*)** calcula os estados intermediários a partir de $P$ e de $C$:
  * Armazenando $2^{56}$ estados calculados para a primeira etapa e comparando com a decifração da segunda/terceira, a complexidade cai drasticamente para a ordem de $2^{112}$ operações.
* **Composição de cifras não equivale à soma direta de bits de segurança!**

### A Limitação do Tamanho de Bloco (64 bits)
* Mesmo que a chave fosse infinita, blocos de 64 bits sofrem com o **Paradoxo do Aniversário**:
  * Ao processar $q \approx 2^{32}$ blocos sob a mesma chave (~34,4 GB), a probabilidade de repetição de blocos ou colisões internas atinge ~39% (ataques do tipo *Sweet32*).
  * Por isso, o AES foi padronizado com blocos de **128 bits**, elevando o limiar do aniversário para a ordem inatingível de $2^{64}$ blocos.

---

## 2. Resultados Numéricos do Estimador

| Algoritmo | Bits de Segurança | 1 Máquina ($10^{12}$/s) | $10^3$ Máquinas | $10^6$ Máquinas |
| :--- | :---: | :---: | :---: | :---: |
| **DES** | 56 | ~10,0 horas | ~36 segundos | ~36 milissegundos |
| **3DES** | 112 | ~$1,6 \times 10^{14}$ anos | ~$1,6 \times 10^{11}$ anos | ~$1,6 \times 10^8$ anos |
| **AES-128** | 128 | ~$1,0 \times 10^{19}$ anos | ~$1,0 \times 10^{16}$ anos | ~$1,0 \times 10^{13}$ anos |

> A razão entre os tempos médios de busca do AES-128 e do DES é exatamente $2^{128-56} = 2^{72} \approx 4{,}72 \times 10^{21}$. Mesmo com paralelismo massivo em nível planetário, o AES-128 é inalcançável por força bruta clássica.

---

## 3. Como Executar os Códigos

### Executar o estimador:
```bash
python caderno_06_encontro06/atividade_11.py
```

### Executar os testes automatizados:
```bash
python -m unittest discover -s caderno_06_encontro06 -p "test_*.py" -v
```
