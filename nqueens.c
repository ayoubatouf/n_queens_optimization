#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <omp.h>

#define BUFFER_INITIAL_CAPACITY (2 * 1024 * 1024)  
#define LINE_BUFFER_SIZE 256

typedef struct {
    char *data;
    size_t size;
    size_t capacity;
} WriteBuffer;

void solve(int row, int cols, int diag1, int diag2, int* current_board, int n, 
           WriteBuffer *buffer);
void solve_n_queens(int n);

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "usage: %s <n>\n", argv[0]);
        return EXIT_FAILURE;
    }

    int n;
    if (sscanf(argv[1], "%d", &n) != 1 || n <= 0) {
        fprintf(stderr, "error: n must be a positive integer\n");
        return EXIT_FAILURE;
    }

    double start_time = omp_get_wtime();  
    solve_n_queens(n);
    double end_time = omp_get_wtime();    

    printf("Total execution time: %.3f seconds\n", end_time - start_time);
    return EXIT_SUCCESS;
}

void solve_n_queens(int n) {
    FILE *fp = fopen("nqueens_solutions.txt", "w");
    if (!fp) {
        perror("error opening file");
        exit(EXIT_FAILURE);
    }

    fprintf(fp, "solutions for N=%d\n", n);

    #pragma omp parallel
    {
        WriteBuffer buf;
        buf.capacity = BUFFER_INITIAL_CAPACITY;
        buf.data = (char*)malloc(buf.capacity);
        buf.size = 0;

        #pragma omp for schedule(dynamic) nowait
        for (int col = 0; col < n; col++) {
            int* board = (int*)malloc(n * sizeof(int));
            board[0] = col;

            int cols_used = 1 << col;
            int diag1 = (1 << col);
            int diag2 = (1 << col);

            solve(1, cols_used, diag1 << 1, diag2 >> 1, board, n, &buf);

            free(board);
        }

        #pragma omp critical
        {
            fwrite(buf.data, 1, buf.size, fp);
        }

        free(buf.data);
    }

    fclose(fp);
    printf("solutions saved to nqueens_solutions.txt\n");
}

void solve(int row, int cols, int diag1, int diag2, int* board, int n, 
           WriteBuffer *buf) {
    if (row == n) {
        int required_size = 0;
        for (int i = 0; i < n; i++) {
            required_size += 12;
        }
        required_size += 2;

        if (buf->size + required_size > buf->capacity) {
            buf->capacity *= 2;
            buf->data = (char*)realloc(buf->data, buf->capacity);
        }

        int pos = 0;
        for (int i = 0; i < n; i++) {
            pos += sprintf(buf->data + buf->size + pos, "%d ", board[i]);
        }
        pos += sprintf(buf->data + buf->size + pos, "\n");
        buf->size += pos;
        return;
    }

    int avail = ~(cols | diag1 | diag2) & ((1 << n) - 1);
    while (avail) {
        int pos = avail & -avail;
        int col = __builtin_ctz(pos);
        board[row] = col;
        solve(row + 1, cols | pos, (diag1 | pos) << 1, (diag2 | pos) >> 1,
              board, n, buf);
        avail ^= pos;
    }
}
