#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("usage: %s <input_filename>\n", argv[0]);
        return 1;
    }

    FILE *fp = fopen(argv[1], "r");
    if (fp == NULL) {
        perror("error opening input file");
        return 1;
    }

    FILE *out_fp = fopen("nqueens_solutions_viz.txt", "w");
    if (out_fp == NULL) {
        perror("error opening output file");
        fclose(fp);
        return 1;
    }

    char line[1024];
    int N = 0;
    int solution_count = 0;

    if (fgets(line, sizeof(line), fp) == NULL || sscanf(line, "solutions for N=%d", &N) != 1 || N <= 0) {
        fprintf(out_fp, "invalid file format or invalid N value\n");
        fclose(fp);
        fclose(out_fp);
        return 1;
    }

    
    while (fgets(line, sizeof(line), fp) != NULL) {
        if (strspn(line, " \t\n") == strlen(line)) {
            continue;  
        }

        int solution[1024];  
        int i = 0;
        char *token = strtok(line, " \t\n");
        while (token && i < N) {
            solution[i++] = atoi(token);
            token = strtok(NULL, " \t\n");
        }

        if (i != N) {
            continue;  
        }

        solution_count++;
        fprintf(out_fp, "solution %d:\n", solution_count);
        fprintf(out_fp, "+");
        for (int col = 0; col < N; col++) {
            fprintf(out_fp, "---");
        }
        fprintf(out_fp, "+\n");

        for (int row = 0; row < N; row++) {
            fprintf(out_fp, "|");
            for (int col = 0; col < N; col++) {
                fprintf(out_fp, " %c ", (solution[col] == row) ? 'Q' : '.');
            }
            fprintf(out_fp, "|\n");
        }

        fprintf(out_fp, "+");
        for (int col = 0; col < N; col++) {
            fprintf(out_fp, "---");
        }
        fprintf(out_fp, "+\n\n");
    }

    fclose(fp);
    fclose(out_fp);
    return 0;
}
