# Scanner Léxico para Textos em Português 

Este projeto é um **Analisador Léxico (Scanner)** construído em Python. Ele lê um arquivo de texto (como um livro), processa o conteúdo e o divide em unidades mínimas de significado chamadas **tokens** (palavras, números e pontuações), respeitando as particularidades da língua portuguesa, como acentuações e palavras compostas.

Os tokens extraídos são exibidos no terminal e salvos em um arquivo `.json`.

##  Como Executar

**Pré-requisitos:** Python 3 instalado.

No terminal, execute o script passando o nome do arquivo de texto como argumento:

```bash
python scannerLivro.py <DomCasmurro.txt>
```
## Como funciona o código
O código segue um fluxo direto: **Ler Texto -> Aplicar Autômato/Regex -> Retornar Tokens -> Salvar Dados**. 

Aqui está a explicação detalhada do que cada parte faz:

### 1. O Padrão Léxico (`PADRAO = re.compile(...)`)
Esta é a base do analisador léxico. O `re.compile()` converte a expressão regular em um autômato capaz de varrer o texto e agrupar os caracteres válidos. Ele é dividido em quatro regras (separadas por `|`):
* `r"[A-Za-zÀ-ÿ]+(?:[-'][A-Za-zÀ-ÿ]+)*"`: **Identificador de Palavras**. Lê letras (incluindo acentos). O bloco `(?:...)*` garante que palavras ligadas por hífen, como (`guarda-chuva`) ou por apóstrofo como (`d'água`) não sejam quebradas ao meio.
* `r"|\d+"`: **Números**. Agrupa dígitos inteiros.
* `r"|\.{2,}"`: **Reticências**. Trata dois ou mais pontos seguidos como um único token léxico.
* `r"|[.,;:!?\"()\[\]—–\-]"`: **Pontuação simples**. Captura caracteres unitários de pontuação.

### 2. Função `ler_arquivo(caminho: str)`
Abre o arquivo de texto alvo em modo de leitura e extrai todo o conteúdo. O uso de `encoding="utf-8"` garante que o interpretador leia corretamente os caracteres especiais do português sem gerar erros de codificação. Retorna o texto bruto em uma única string.

### 3. Função `tokenizar(texto: str)`
Recebe a string bruta e aplica o scanner léxico. O método `findall()` percorre o texto do início ao fim, agrupando os caracteres que casam com a gramática regular definida no `PADRAO` e descartando espaços em branco. Retorna uma lista ordenada com os tokens.

### 4. Função `salvar_json(tokens: list, caminho_saida: str)`
Persiste os tokens gerados em um arquivo físico. Usa a biblioteca `json` para formatar a lista Python em um formato `.json`. O parâmetro `ensure_ascii=False` é obrigatório para evitar que acentos virem códigos ilegíveis, mantendo a integridade dos dados lidos.

### 5. Função `main()`
Executa o fluxo do programa:
1. Valida se o usuário informou o arquivo de texto via linha de comando (`sys.argv`). Se não, encerra a execução.
2. Chama `ler_arquivo()` para carregar os dados.
3. Chama `tokenizar()` para gerar a lista léxica.
4. Exibe os resultados no terminal de forma direta (total de itens e um recorte dos 50 primeiros).
5. Chama `salvar_json()` para criar o arquivo de saída definitivo.