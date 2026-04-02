
#Lê um arquivo .txt em UTF-8 (exemplo usado: livro do Project Gutenberg Dom Casmurro de Machado de Assis) quebrando em tokens usando expressoes regulares respeitando o português
#Saída: 50 primeiros tokens no terminal e todos os tokens em arquivo json chamado "tokens_output.json"
#Uso: python scannerLivro.py <nomedolivro.txt>

import re
import json
import sys

PADRAO = re.compile( #intreprete do regex
    r"[A-Za-zÀ-ÿ]+(?:[-'][A-Za-zÀ-ÿ]+)*"  # palavras (com hífen ou apóstrofo)
    r"|\d+"                                   # números inteiros
    r"|\.{2,}"                                # reticências
    r"|[.,;:!?\"()\[\]—–\-]",                # pontuação
)


def ler_arquivo(caminho: str) -> str: #Lê o conteúdo de um arquivo de texto em UTF-8. caminho é aonde o arquivo esta localizado, retorna uma string com o conteudo do arquivo
    with open(caminho, encoding="utf-8") as f: #abre como utf-8 o arquivo direcionado
        return f.read()

def tokenizar(texto: str) -> list[str]: #    O parametro "texto" é o que deve ser tokenizado.
    return PADRAO.findall(texto)        #    Retorna uma lista ordenada dos tokens achados
                                        #    Aplica o scanner léxico ao texto e retorna a lista de tokens. Cada token é uma string que pode representar palavras, numeros, etc.

def salvar_json(tokens: list[str], caminho_saida: str) -> None:
    with open(caminho_saida, "w", encoding="utf-8") as f: #Salva a lista de tokens em um arquivo JSON com encoding UTF-8.
        json.dump(tokens, f, ensure_ascii=False, indent=2)

def main(): #Executa o programa e lê o arquivo passado como argumento, tokeniza o texto, exibe os primeiros 50 tokens e salva os restantes em 'tokens_output.json'
    if len(sys.argv) < 2:
        print("Uso: python scannerLivro.py <caminho_do_arquivo.txt>") # Verifica se o usuário passou o arquivo como argumento
        sys.exit(1)
    caminho = sys.argv[1]
    print(f"Lendo arquivo: {caminho}")
    texto = ler_arquivo(caminho)

    print("Tokenizando...")
    tokens = tokenizar(texto)

    print(f"\nTotal de tokens encontrados: {len(tokens)}")
    print(f"\nPrimeiros 50 tokens:\n{tokens[:50]}")

    saida = "tokens_output.json" #arquivo em que sera salvo todos os tokens
    salvar_json(tokens, saida) #coloca os tokens dentro do arquivo json
    print(f"\nTokens salvos")


if __name__ == "__main__":
    main()