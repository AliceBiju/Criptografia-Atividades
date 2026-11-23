# Atividade em Dupla - E-mail Criptografado com AES

Este projeto implementa um sistema completo de **envio e recebimento de e-mails criptografados utilizando o algoritmo AES (Advanced Encryption Standard)** para a atividade prática em dupla.

Ele possui as **duas versões** necessárias para a dinâmica entre você e seu amigo:
1. **Versão de Criptografar (`criptografar_email.py`)**: Você escreve o e-mail, escolhe ou gera uma chave AES (de 256 bits ou senha secreta), e o programa gera o **código criptografado** (e o arquivo `email_criptografado.json`) para você enviar ao seu amigo junto com a chave.
2. **Versão de Descriptografar (`descriptografar_email.py`)**: Você cola o código criptografado (ou carrega o arquivo JSON) que o seu amigo te enviou, informa a **chave secreta** dele e descobre imediatamente o que está escrito na mensagem original!

---

## Arquivos da Pasta

* [`aes_email.py`](./aes_email.py): Módulo principal contendo a implementação do **AES-256-GCM** (criptografia autenticada com validação de cabeçalhos `De/Para/Assunto` via AAD), **AES-256-CBC** (com padding PKCS#7), derivação de chave por senha (**PBKDF2-HMAC-SHA256**) e envio opcional por **SMTP**.
* [`criptografar_email.py`](./criptografar_email.py): **Versão 1 (Remetente)** — Interface passo a passo para criar e criptografar um e-mail para enviar ao seu amigo.
* [`descriptografar_email.py`](./descriptografar_email.py): **Versão 2 (Destinatário)** — Interface passo a passo para descriptografar o e-mail recebido do seu amigo usando a chave.
* [`main.py`](./main.py): Menu interativo unificado com as duas versões + modo de simulação automática da dupla (`--demo`).
* [`test_email_aes.py`](./test_email_aes.py): Testes unitários automatizados validando o fluxo de ida e volta da dupla, rejeição de chaves incorretas e proteção contra adulteração.

---

## Passo a Passo para Fazer a Atividade com seu Amigo

### Quando a primeira pessoa enviar o e-mail criptografado para o seu amigo:
No terminal, dentro da pasta principal ou desta pasta, execute:
```bash
python "email criptografado (AES)/criptografar_email.py"
```
1. Digite o seu e-mail, o e-mail do seu amigo, o assunto e a **mensagem secreta**.
2. Escolha se quer **gerar uma chave AES-256 aleatória** (opção `1`) ou **digitar uma senha secreta** (opção `2`).
3. O programa vai exibir na tela (e salvar em `email_criptografado.json` e `email_para_enviar_ao_amigo.txt`):
   * O **CÓDIGO COMPLETO** do e-mail criptografado (em Base64).
   * A **CHAVE SECRETA** utilizada.
4. **Envie o código criptografado (ou o arquivo `.json`) e a chave para o seu amigo** (por e-mail, WhatsApp, Discord, etc., ou dispare diretamente por SMTP real se desejar).

---

### Quando a segunda pessoa enviar o e-mail criptografado dele para você descobrir o que está escrito:
Execute a versão de descriptografar:
```bash
python "email criptografado (AES)/descriptografar_email.py"
```
1. Escolha a opção `1` para **colar o código Base64/JSON** que ele te mandou (ou a opção `2` se ele tiver te enviado o arquivo `email_criptografado.json`).
2. Digite ou cole a **CHAVE SECRETA** que ele te passou.
3. O programa validará a autenticidade do pacote AES e revelará na tela o remetente, assunto, data/hora e a **mensagem secreta original**!

*(O seu amigo fará exatamente esse mesmo passo 2 no computador dele para descobrir o que você escreveu para ele!)*

---

## Menu Completo e Simulação Automática

Você também pode abrir o menu unificado que reúne as duas versões:
```bash
python "email criptografado (AES)/main.py"
```

Ou rodar uma **demonstração automática** simulando você enviando um e-mail criptografado para o seu amigo e ele enviando outro de volta para você:
```bash
python "email criptografado (AES)/main.py" --demo
```

---

## Executando os Testes Automatizados

Para rodar os testes unitários desta atividade:
```bash
python -m unittest discover -s "email criptografado (AES)" -p "test_*.py" -v
```

---

## Como Funciona a Segurança Criptográfica deste Projeto?

1. **Confidencialidade com AES-256**: O conteúdo do e-mail é cifrado com chaves de 256 bits usando a biblioteca `cryptography`. Mesmo que alguém intercepte o e-mail no caminho, verá apenas bytes pseudoaleatórios em Base64 impossíveis de reverter sem a chave.
2. **Vetor de Inicialização (IV / Nonce) Único**: Cada e-mail gera um `nonce` criptograficamente aleatório (`os.urandom`), garantindo que dois e-mails idênticos cifrados com a mesma chave gerem textos cifrados completamente diferentes.
3. **Autenticidade e Integridade (AES-GCM)**: No modo padrão `GCM`, além de esconder a mensagem, é gerada uma *Tag de Autenticação* de 128 bits que protege tanto o corpo do e-mail quanto os metadados (`De`, `Para`, `Assunto`). Se a chave estiver errada em 1 único bit ou se alguém tentar alterar o texto cifrado, a descriptografia detecta imediatamente e bloqueia a leitura.
4. **Suporte a Chave Bruta ou Senha (PBKDF2)**: Aceita tanto chaves AES puras geradas aleatoriamente em Base64 quanto senhas legíveis (derivadas com `PBKDF2-HMAC-SHA256`, `salt` aleatório de 128 bits e `100.000` iterações).
