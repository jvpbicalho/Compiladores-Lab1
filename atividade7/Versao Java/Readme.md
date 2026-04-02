# Scanner Léxico para Textos em Português 

Este projeto é um **Analisador Léxico (Scanner)** construído em Java. Ele lê um arquivo de texto (como um livro), processa o conteúdo e o divide em unidades mínimas de significado chamadas **tokens** (palavras, números e pontuações), respeitando as particularidades da língua portuguesa, como acentuações e palavras compostas.

Os tokens extraídos são exibidos no terminal e salvos em um arquivo `.json`.

##  Como Executar

**Pré-requisitos:** JDK (Java Development Kit) 11 ou superior instalado (necessário para o método `Files.readString`).

No terminal, primeiro compile o arquivo Java e depois execute-o passando o nome do arquivo de texto como argumento:

```bash
# Para compilar o código
javac scannerLivro.java

# Para executar o programa
java scannerLivro <DomCasmurro.txt>
```
##  Como funciona o código

O código segue um fluxo direto: **Ler Texto -> Aplicar Autômato/Regex -> Retornar Tokens -> Salvar Dados**.

### 1. O Padrão Léxico (`PADRAO = Pattern.compile(...)`)
Esta é a base do analisador léxico. A classe `Pattern` do pacote `java.util.regex` compila a expressão regular em um autômato capaz de varrer o texto e agrupar os caracteres válidos. Ele é dividido em quatro regras (separadas por `|`):

* `"[A-Za-zÀ-ÿ]+(?:[-'][A-Za-zÀ-ÿ]+)*"`: **Identificador de Palavras**. Lê letras (incluindo acentos). O bloco `(?:...)*` garante que palavras ligadas por hífen (`guarda-chuva`) ou por apóstrofo (`d'água`) não sejam quebradas ao meio.
* `"|\\d+"`: **Números**. Agrupa dígitos inteiros.
* `"|\\.{2,}"`: **Reticências**. Trata dois ou mais pontos seguidos como um único token léxico.
* `"|[.,;:!?\"()\\[\\]—–\\-]"`: **Pontuação simples**. Captura caracteres unitários de pontuação (necessita de barra dupla `\\` no Java para escapar os caracteres).

### 2. Função `lerArquivo(String caminho)`
Lê o arquivo de texto alvo. Utiliza `Files.readString()` para carregar todo o conteúdo do arquivo de forma direta. O Java já trata a leitura como UTF-8 por padrão neste método, evitando que caracteres especiais do português quebrem a codificação. Retorna o texto bruto em uma única `String`.

### 3. Função `tokenizar(String texto)`
Recebe a string bruta e aplica o scanner léxico. A classe `Matcher` é instanciada para agir como um cursor no texto. O laço `while (matcher.find())` percorre o texto do início ao fim, extraindo os fragmentos que coincidem com a gramática regular definida no `PADRAO` (usando `matcher.group()`) e os adiciona sequencialmente em uma lista do tipo `ArrayList`.

### 4. Função `salvarJson(List<String> tokens, String caminhoSaida)`
Persiste os tokens em um arquivo de texto. Como o Java nativo não possui uma biblioteca embutida simples para JSON, esta função faz a formatação manualmente. Ela utiliza um `BufferedWriter` para escrever linha por linha iterando com um `for` simples, inserindo os colchetes `[]`, as aspas em volta de cada token e as vírgulas `,` necessárias para garantir que o arquivo final seja um JSON estruturalmente válido.

### 5. Função `main(String[] args)`
Executa o fluxo do programa:

* Valida se o usuário informou o arquivo de texto via argumento de linha de comando verificando o tamanho do vetor `args`. Se não, encerra a execução.
* Chama `lerArquivo()` para carregar os dados.
* Chama `tokenizar()` para gerar a `List` léxica.
* Exibe os resultados no terminal (total de itens e um recorte dos 50 primeiros, usando `Math.min` para evitar erros caso o arquivo tenha menos de 50 tokens).
* Chama `salvarJson()` para criar o arquivo de saída definitivo `tokens_output.json`.