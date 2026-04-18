#include <stdio.h>
#include <stdlib.h>
#include <cuda_runtime.h>

__global__ void matrixMulKernel(const double* A, const double* B, double* C, int N) {
    int row = blockIdx.y * blockDim.y + threadIdx.y;
    int col = blockIdx.x * blockDim.x + threadIdx.x;
    if (row < N && col < N) {
        double sum = 0.0;
        for (int k = 0; k < N; ++k) {
            sum += A[row * N + k] * B[k * N + col];
        }
        C[row * N + col] = sum;
    }
}

int main(int argc, char* argv[]) {
    int N = (argc > 1) ? atoi(argv[1]) : 800;
    size_t total_elements = (size_t)N * N;
    size_t size_bytes = total_elements * sizeof(double);

    double *h_A = (double*)malloc(size_bytes);
    double *h_B = (double*)malloc(size_bytes);
    double *h_C = (double*)malloc(size_bytes);

    // Чтение файлов
    FILE *fA = fopen("A.txt", "r");
    FILE *fB = fopen("B.txt", "r");
    if (!fA || !fB) { printf("Ошибка: файлы A.txt или B.txt не найдены!\n"); return 1; }

    int dummy;
    fscanf(fA, "%d", &dummy); fscanf(fB, "%d", &dummy);
    for (size_t i = 0; i < total_elements; i++) fscanf(fA, "%lf", &h_A[i]);
    for (size_t i = 0; i < total_elements; i++) fscanf(fB, "%lf", &h_B[i]);
    fclose(fA); fclose(fB);

    double *d_A, *d_B, *d_C;
    cudaMalloc(&d_A, size_bytes);
    cudaMalloc(&d_B, size_bytes);
    cudaMalloc(&d_C, size_bytes);

    cudaMemcpy(d_A, h_A, size_bytes, cudaMemcpyHostToDevice);
    cudaMemcpy(d_B, h_B, size_bytes, cudaMemcpyHostToDevice);

    // Сетка 32x32 (оптимально для RTX 4050)
    dim3 threads(32, 32);
    dim3 blocks((N + 31) / 32, (N + 31) / 32);

    cudaEvent_t start, stop;
    cudaEventCreate(&start); cudaEventCreate(&stop);
    cudaEventRecord(start);

    matrixMulKernel<<<blocks, threads>>>(d_A, d_B, d_C, N);

    cudaEventRecord(stop);
    cudaEventSynchronize(stop);
    float ms = 0;
    cudaEventElapsedTime(&ms, start, stop);

    printf("N=%d | RTX 4050 | Time: %.6f sec\n", N, ms / 1000.0);

    // Забираем результат и пишем в файл для верификации
    cudaMemcpy(h_C, d_C, size_bytes, cudaMemcpyDeviceToHost);

    FILE *fC = fopen("C.txt", "w");
    if (fC) {
        fprintf(fC, "%d\n", N);
        for (size_t i = 0; i < total_elements; i++) {
            fprintf(fC, "%.4f ", h_C[i]);
            if ((i + 1) % N == 0) fprintf(fC, "\n");
        }
        fclose(fC);
    }

    cudaFree(d_A); cudaFree(d_B); cudaFree(d_C);
    free(h_A); free(h_B); free(h_C);
    return 0;
}