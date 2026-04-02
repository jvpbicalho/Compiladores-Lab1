# Analisador Léxico (Dragon Book) e Extrator de E-mails 

Este projeto em Python têm duas partes principais:
1. A implementação de um **Analisador Léxico (Scanner)** conceitual, baseado na estrutura do clássico "Livro do Dragão". Ele tokeniza expressões matemáticas e gera uma Tabela de Símbolos.
2. Um **Extrator de E-mails** que faz uma requisição web e utiliza Expressões Regulares (RegEx) para rastrear endereços válidos em um código-fonte HTML.

##  Como Executar

**Pré-requisitos:** Python 3 e a biblioteca externa `requests`.

No terminal, instale a dependência necessária e execute o script:

```bash
# Instalar a biblioteca requests
pip install requests

# Executar o programa
python regex.py
```

O programa é dividido em blocos lógicos focados na extração e classificação de strings através de Expressões Regulares.

### 1. Padrões de Tokens (`TOKEN_PATTERNS` e `MASTER_RE`)
Define as regras gramaticais estritas do compilador. A lista `TOKEN_PATTERNS` estabelece uma ordem de prioridade para capturar: números (`NUM`), identificadores/variáveis (`ID`), operadores matemáticos (`OP`), operadores relacionais (`RELOP`) e espaços em branco (`WS`).
A variável `MASTER_RE` pega tudo isso e compila em uma única Expressão Regular "mestre" utilizando recursos de grupos nomeados (`?P<nome>`). Isso cria o autômato finito que fará a varredura do texto de uma vez só.

### 2. Função `tokenize(texto: str)`
Atua como o motor do scanner léxico. Recebe a string bruta e usa um laço `while` para avançar caractere por caractere. O método `MASTER_RE.match()` tenta casar os padrões definidos com o fragmento atual do texto. Se houver "match", ele extrai o tipo de token (ex: `'ID'`) e o valor exato, o lexema (ex: `'position'`). A função ignora espaços em branco (`'WS'`) e retorna uma lista organizada contendo essas tuplas.

### 3. Função `tokenizardragao(texto: str)`
Pega a lista bruta do passo anterior e a formata visualmente para o padrão ensinado no Livro do Dragão.
* Inicializa um dicionário `tabela_simbolos` que atua como a memória do compilador para cadastrar variáveis novas.
* Se o token lido for do tipo identificador (`'ID'`), ele verifica se a variável já existe na tabela. Se não, ela é criada e é designada como (`proximo_id`).
* Substitui o nome da variável na string final pela sua referência estrutural, gerando saídas como `<id, 1>`. Números e operadores são impressos diretamente. Retorna os tokens formatados e a tabela construída.

### 4. Função `extrair_emails(url: str)`
Uma ferramenta de extração de dados independente da análise do compilador.
* Usa a biblioteca `requests` para fazer um GET na URL passada e baixar todo o código HTML da página web.
* Aplica a expressão regular `EMAIL_RE` através do método `.findall()` para varrer a string gigante do HTML em busca de sequências de texto que respeitem o formato padrão de um e-mail.
* Utiliza a estrutura matemática de conjunto (`set()` na variável `vistos`) para filtrar e-mails duplicados sem perder a ordem em que foram achados no texto, populando a lista `emails_unicos` apenas com valores inéditos.

## Utilizar o link *https://www.rfc-editor.org/rfc/rfc5322.txt* para varrer e-mails.