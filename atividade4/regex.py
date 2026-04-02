import re
import requests
entrada = "position = initial + rate * 60" #exemplo do livro do dragao

regexp = r'[a-zA-Z][a-zA-Z0-9_]*|\d+|[=+\-*]'  # Definindo o Autômato Finito
tokens = re.findall(regexp, entrada)
print("Tokens brutos", tokens)


TOKEN_PATTERNS = [ # Padrões em ordem de prioridade
    ('NUM',    r'\d+(\.\d+)?'),                   # números inteiros ou decimais
    ('ID',     r'[a-zA-Z][a-zA-Z0-9_]*'),         # identificadores
    ('OP',     r'[=+\-*/]'),                      # operadores aritméticos
    ('RELOP',  r'[<>]=?|==|!='),                  # operadores de relacao
    ('WS',     r'\s+'),                           # espaços
]


MASTER_RE = re.compile(
    '|'.join(f'(?P<{nome}>{padrao})' for nome, padrao in TOKEN_PATTERNS) # Compila todos os padrões em uma única expressão regular com grupos nomeados
)

def tokenize(texto: str) -> list[tuple[str, str]]: # PARTE 2 — Função tokenize(texto) com tipos retorna lista de tuplas (tipo, lexema)

    lista_tuplas = []
    pos = 0
    while pos < len(texto):  #Percorre o texto usando o Autômato Finito (MASTER_RE) e retorna uma lista de tuplas (tipo, lexema), ignorando espaços em branco.
        m = MASTER_RE.match(texto, pos)
        tipo = m.lastgroup
        lexema = m.group()
        if tipo != 'WS':          # ignora espaços em branco
            lista_tuplas.append((tipo, lexema))
        pos = m.end()
    return lista_tuplas


# Entrada (trecho do Dragon Book): position = initial + rate * 60 Saída esperada (formato Figura 1.7 do livro): <id, 1>  <=>  <id, 2>  <+>  <id, 3>  <*>  <60> onde a tabela de símbolos mapeia position, initial e rate
def tokenizardragao(texto: str):
    tabela_simbolos: dict[str, int] = {}  # lexema → índice
    proximo_id = 1 #começa no id como 1 e vai incrementando dentro do for caso ja nao esteja na tabela de simbolos
    tokens_formatados = [] #lista que vai ser usada para colocar as duplas
    for tipo, lexema in tokenize(texto):
        if tipo == 'ID':
            if lexema not in tabela_simbolos:
                tabela_simbolos[lexema] = proximo_id
                proximo_id += 1
            idx = tabela_simbolos[lexema]
            tokens_formatados.append(f'<id, {idx}>')
        elif tipo == 'NUM':
            tokens_formatados.append(f'<{lexema}>')
        else:
            tokens_formatados.append(f'<{lexema}>')

    return tokens_formatados, tabela_simbolos



EMAIL_RE = re.compile(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}') # PARTE 3 — Extração de e-mails de página web com requests + regexp

def extrair_emails(url: str):
    resposta = requests.get(url)
    texto = resposta.text
    emails = EMAIL_RE.findall(texto)


    vistos = set() # remove duplicatas mantendo ordem
    emails_unicos = []
    for email in emails:
        if email not in vistos:
            vistos.add(email)
            emails_unicos.append(email)

    print(f"E-mails encontrados em {url}:")
    for email in emails_unicos:
        print(f"  {email}")
    return emails_unicos


if __name__ == '__main__':
    entrada = "position = initial + rate * 60"
    resultado = tokenize(entrada)
    print(f"Entrada: {entrada!r}")
    for t in resultado:
        print(f"  {t}")

    print()     #Figura 1.7 do livro
    tokens_fmt, tabela = tokenizardragao(entrada)
    print("Sequência de tokens:")
    print("  " + "  ".join(tokens_fmt))
    print()
    print("Tabela de símbolos:")
    for lexema, idx in sorted(tabela.items(), key=lambda x: x[1]):
        print(f"  {idx}: {lexema}")

    print()
    extrair_emails("https://www.rfc-editor.org/rfc/rfc5322.txt")