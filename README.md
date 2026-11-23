# Repositório de Atividades Práticas — Introdução à Criptografia

Este repositório reúne as implementações completas, resolvidas, testadas e documentadas das atividades práticas de código referentes aos **12 Cadernos do Aluno (Encontros 01 ao 12)** da disciplina de Introdução à Criptografia.

Cada encontro possui sua própria pasta isolada contendo o código-fonte executável, suíte de testes unitários automatizados com `unittest` e um arquivo explicativo `README.md` detalhando as justificativas matemáticas, propriedades de segurança e respostas aos desafios conceituais.

---

## 📁 Estrutura do Repositório

```text
Cripto/
├── caderno_01_encontro01/    # SHA-256 vs HMAC-SHA256 (Ataque a transferência e integridade)
├── caderno_02_encontro02/    # Aritmética Modular, Inverso (Euclides Estendido), XOR e Nonces
├── caderno_03_encontro03/    # Cifra de César, Análise de Frequência e Cifra Composta
├── caderno_04_encontro04/    # Cifras de Fluxo, Two-Time Pad e Maleabilidade do XOR
├── caderno_05_encontro05/    # Redes de Feistel Reversíveis e Medição do Efeito Avalanche
├── caderno_06_encontro06/    # DES, 3DES, Estimador de Busca Exaustiva e Limite de Aniversário
├── caderno_07_encontro07/    # Multiplicação no Corpo Finito GF(2^8) do AES e MixColumns
├── caderno_08_encontro08/    # Modos de Operação Reversíveis: ECB, CBC e CTR com Limites
├── caderno_09_encontro09/    # Criptografia Autenticada (AEAD com AES-GCM), AAD e Antirrepetição
├── caderno_10_encontro10/    # Acordo X25519, Derivação HKDF e Intermediário (Mallory/MITM)
├── caderno_11_encontro11/    # RSA Didático, Maleabilidade Homomórfica e Padrões OAEP/PSS
├── caderno_12_encontro12/    # Diffie-Hellman em Subgrupo Cíclico, Auditoria e Cifração ElGamal
├── requirements.txt          # Dependências do projeto (cryptography >= 41.0.0)
├── run_all.py                # Orquestrador global de testes automatizados (79 testes)
└── README.md                 # Guia geral de execução e documentação
```

---

## 📚 Visão Geral dos Cadernos

| Caderno / Encontro | Tema Principal | Arquivos Principais | Conceito-Chave |
| :--- | :--- | :--- | :--- |
| **Caderno 01 (Encontro 01)** | SHA-256 vs HMAC | `sha256_vs_hmac.py`, `atividade_11.py` | Por que hash sem chave não garante autenticidade contra atacante ativo. |
| **Caderno 02 (Encontro 02)** | Aritmética Modular e XOR | `inverso_modular_xor.py`, `atividade_11.py` | Algoritmo de Euclides Estendido, inverso modular e geração de nonces. |
| **Caderno 03 (Encontro 03)** | Cifras Clássicas e Frequência | `cesar_frequencia.py`, `atividade_11.py` | Ataque por busca exaustiva ranqueado por heurística linguística em PT-BR. |
| **Caderno 04 (Encontro 04)** | Cifras de Fluxo e OTP | `fluxo_twotimepad.py`, `atividade_11.py` | Ataque *Two-Time Pad* ($C_1 \oplus C_2 = M_1 \oplus M_2$) e maleabilidade. |
| **Caderno 05 (Encontro 05)** | Redes de Feistel | `feistel_reversivel.py`, `atividade_11.py` | Inversibilidade estrutural sem inverter $F$, e cálculo de avalanche. |
| **Caderno 06 (Encontro 06)** | DES, 3DES e Busca Exaustiva | `estimador_forca_bruta.py`, `atividade_11.py` | Força de 56 bits do DES, 112 bits do 3DES (*Meet-in-the-Middle*) e AES. |
| **Caderno 07 (Encontro 07)** | Álgebra do AES ($GF(2^8)$) | `aes_corpo_finito.py`, `atividade_11.py` | Implementação de `xtime`, multiplicação polinomial e *MixColumns*. |
| **Caderno 08 (Encontro 08)** | Modos CBC e CTR | `modos_cbc_ctr.py`, `atividade_11.py` | Encadeamento vs contador, reversão e rejeição de esgotamento. |
| **Caderno 09 (Encontro 09)** | Criptografia Autenticada (AEAD) | `registro_aead.py`, `atividade_11.py` | AES-GCM com AAD, detecção de adulteração (`InvalidTag`) e anti-replay. |
| **Caderno 10 (Encontro 10)** | Chave Pública e MITM | `x25519_hkdf_mitm.py`, `atividade_11.py` | Curvas elípticas X25519, HKDF e simulação de ataque de intermediário. |
| **Caderno 11 (Encontro 11)** | RSA Didático, OAEP e PSS | `rsa_modular_oaep_pss.py`, `atividade_11.py` | Maleabilidade do RSA bruto e padrões seguros RSA-OAEP e RSA-PSS. |
| **Caderno 12 (Encontro 12)** | Diffie-Hellman e ElGamal | `dh_subgrupo_elgamal.py`, `atividade_11.py` | Subgrupo de ordem prima, auditoria e limites da validação matemática. |

---

## 🛠️ Pré-requisitos e Instalação

### Requisitos
* **Python 3.10 ou superior**
* Gerenciador de pacotes `pip` ou ferramenta rápida `uv`

### 1. Clonar o Repositório
```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd Cripto
```

### 2. Configurar o Ambiente Virtual (venv padrão)

#### No Windows (PowerShell):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

#### No Linux / macOS:
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

*(Opcional: Caso utilize o gerenciador `uv`, basta rodar `uv run --with cryptography python run_all.py`)*.

---

## 🚀 Como Executar os Códigos

### Executando o script principal de uma atividade específica:
Você pode executar o arquivo `atividade_11.py` de qualquer caderno:
```bash
python caderno_01_encontro01/atividade_11.py
python caderno_07_encontro07/atividade_11.py
python caderno_12_encontro12/atividade_11.py
```

### Executando os testes unitários de um caderno específico:
```bash
python -m unittest discover -s caderno_01_encontro01 -p "test_*.py" -v
python -m unittest discover -s caderno_09_encontro09 -p "test_*.py" -v
```

---

## 🧪 Execução Global de Todos os Testes

O repositório disponibiliza um script unificado (`run_all.py`) que executa a suíte de testes de todos os 12 cadernos e imprime um relatório consolidado com tempo e status:

```bash
python run_all.py
```

Alternativamente, é possível executar a descoberta nativa do `unittest` a partir da raiz:
```bash
python -m unittest discover -p "test_*.py" -v
```

> **Resultado dos testes:** Todos os **79 testes automatizados** passam com **100% de sucesso**.

---

## 🛡️ Aviso Acadêmico e Limites de Segurança
Os parâmetros reduzidos utilizados em algumas atividades (como chaves de 4 bits no Feistel, blocos de 4 bits nos modos de operação, RSA com primos pequenos $p=7, q=13$ e grupo Diffie-Hellman com $p=23$) têm **finalidade estritamente didática** para permitir cálculos manuais, inspeção passo a passo e compreensão conceitual de vulnerabilidades. Para uso em produção, devem ser utilizadas bibliotecas auditadas (como `cryptography`) com algoritmos e parâmetros padronizados (AES-GCM de 256 bits, Ed25519/X25519, RSA-OAEP/PSS $\ge$ 2048/3072 bits, SHA-256/SHA-512).
