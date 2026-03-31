#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define INITIAL_CAPACITY 100

// Função de comparação para qsort (padrão da biblioteca)
int comparar_strings(const void *a, const void *b) {
    const char *str1 = *(const char **)a;
    const char *str2 = *(const char **)b;
    return strcmp(str1, str2);
}

// Implementação própria de quicksort (para fins didáticos)
void quicksort(char **arr, int low, int high) {
    if (low >= high) {
        return;
    }

    // Escolhe o pivô (último elemento)
    char *pivot = arr[high];
    int i = low - 1;

    for (int j = low; j < high; j++) {
        // Se o elemento atual for menor ou igual ao pivô
        if (strcmp(arr[j], pivot) <= 0) {
            i++;
            // Troca arr[i] e arr[j]
            char *temp = arr[i];
            arr[i] = arr[j];
            arr[j] = temp;
        }
    }

    // Coloca o pivô na posição correta
    char *temp = arr[i + 1];
    arr[i + 1] = arr[high];
    arr[high] = temp;

    int pi = i + 1;  // posição final do pivô

    // Ordena recursivamente as duas partes
    quicksort(arr, low, pi - 1);
    quicksort(arr, pi + 1, high);
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Uso: %s nome_do_arquivo.txt\n", argv[0]);
        return 1;
    }

    const char *nome_arquivo = argv[1];
    FILE *arquivo = fopen(nome_arquivo, "r");
    if (!arquivo) {
        perror("Erro ao abrir o arquivo");
        return 1;
    }

    // Alocação inicial do array de ponteiros
    size_t capacidade = INITIAL_CAPACITY;
    size_t contador = 0;
    char **linhas = malloc(capacidade * sizeof(char *));
    if (!linhas) {
        perror("Erro ao alocar memória");
        fclose(arquivo);
        return 1;
    }

    char buffer[1024];
    while (fgets(buffer, sizeof(buffer), arquivo)) {
        // Remove o \n do final (se existir)
        size_t len = strlen(buffer);
        if (len > 0 && buffer[len - 1] == '\n') {
            buffer[len - 1] = '\0';
        }

        // Duplica a string (aloca memória nova)
        char *linha = strdup(buffer);
        if (!linha) {
            perror("Erro ao duplicar string");
            // Libera o que já foi alocado antes de sair
            for (size_t i = 0; i < contador; i++) {
                free(linhas[i]);
            }
            free(linhas);
            fclose(arquivo);
            return 1;
        }

        // Redimensiona array se necessário
        if (contador >= capacidade) {
            capacidade *= 2;
            char **novo = realloc(linhas, capacidade * sizeof(char *));
            if (!novo) {
                perror("Erro ao realocar memória");
                for (size_t i = 0; i < contador; i++) free(linhas[i]);
                free(linhas);
                free(linha);
                fclose(arquivo);
                return 1;
            }
            linhas = novo;
        }

        linhas[contador++] = linha;
    }

    fclose(arquivo);

    if (contador == 0) {
        printf("O arquivo está vazio ou não contém linhas.\n");
    } else {
        // Ordena usando nossa implementação de quicksort
        quicksort(linhas, 0, contador - 1);

        // Ou poderia usar a função padrão da biblioteca:
        // qsort(linhas, contador, sizeof(char*), comparar_strings);

        printf("Linhas ordenadas alfabeticamente:\n");
        printf("--------------------------------\n");
        for (size_t i = 0; i < contador; i++) {
            printf("%s\n", linhas[i]);
        }
    }

    // Libera memória
    for (size_t i = 0; i < contador; i++) {
        free(linhas[i]);
    }
    free(linhas);

    return 0;
}
