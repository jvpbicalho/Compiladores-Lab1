import java.io.*;
import java.nio.file.*;
import java.util.*;
import java.util.regex.*;

public class scannerLivro {

    private static final Pattern PADRAO = Pattern.compile(
            "[A-Za-zÀ-ÿ]+(?:[-'][A-Za-zÀ-ÿ]+)*" +
                    "|\\d+" +
                    "|\\.{2,}" +                                    // Padrão léxico: palavras, números, reticências e pontuação básica
                    "|[.,;:!?\"()\\[\\]—–\\-]"
    );


    public static String lerArquivo(String caminho) throws IOException { // Lê o conteúdo do arquivo em UTF-8
        return Files.readString(Paths.get(caminho));
    }


    public static List<String> tokenizar(String texto) { // Tokeniza o texto
        List<String> tokens = new ArrayList<>();
        Matcher matcher = PADRAO.matcher(texto);

        while (matcher.find()) {
            tokens.add(matcher.group());
        }

        return tokens;
    }


    public static void salvarJson(List<String> tokens, String caminhoSaida) throws IOException { // Salva os tokens em um arquivo JSON
        BufferedWriter writer = new BufferedWriter(new FileWriter(caminhoSaida));
        writer.write("[\n");
        for (int i = 0; i < tokens.size(); i++) {
            writer.write("  \"" + tokens.get(i) + "\"");

            if (i < tokens.size() - 1) {
                writer.write(",");
            }
            writer.write("\n");
        }

        writer.write("]");
        writer.close();
    }


    public static void main(String[] args) throws IOException {  // leitura, tokenização e saída

        if (args.length < 1) {
            System.out.println("Uso: java scannerLivro <nomedolivro.txt>");
            return;
        }

        String caminho = args[0];
        System.out.println("Lendo arquivo: " + caminho); String texto = lerArquivo(caminho);
        System.out.println("Tokenizando..."); List<String> tokens = tokenizar(texto);
        System.out.println("\nTotal de tokens: " + tokens.size());


        System.out.println("\nPrimeiros 50 tokens:");
        for (int i = 0; i < Math.min(50, tokens.size()); i++) { // Exibe os primeiros 50 tokens
            System.out.print("'");
            System.out.print(tokens.get(i) + "' ");
        }

        String saida = "tokens_output.json";
        salvarJson(tokens, saida); //cria o arquivo json com os tokens
    }
}