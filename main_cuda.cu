#include <iostream>
#include <fstream>
#include <vector>
#include <cuda_runtime.h>
#include <device_launch_parameters.h>
#include <windows.h>
#include <iomanip>

using namespace std;

bool readMatrix(const string& filename, vector<double>& matrix, int& n) {
    ifstream file(filename);
    if (!file.is_open()) return false;
    file >> n;
    matrix.resize(n * n);
    for (int i = 0; i < n * n; ++i) file >> matrix[i];
    return true;
}

bool writeMatrix(const string& filename, const vector<double>& matrix, int n) {
    ofstream file(filename);
    if (!file.is_open()) return false;
    file << n << "\n";
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) file << matrix[i * n + j] << " ";
        file << "\n";
    }
    return true;
}

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

int main() {
    SetConsoleOutputCP(1251);
    SetConsoleCP(1251);

    int nA, nB;
    vector<double> h_A, h_B;
    if (!readMatrix("A.txt", h_A, nA) || !readMatrix("B.txt", h_B, nB)) {
        cerr << "Ошибка: Сначала сгенерируйте матрицы скриптом Python!" << endl;
        return 1;
    }
    int N = nA;
    vector<double> h_C(N * N, 0.0);
    size_t size = N * N * sizeof(double);

    double* d_A, * d_B, * d_C;
    cudaMalloc(&d_A, size);
    cudaMalloc(&d_B, size);
    cudaMalloc(&d_C, size);

    cudaMemcpy(d_A, h_A.data(), size, cudaMemcpyHostToDevice);
    cudaMemcpy(d_B, h_B.data(), size, cudaMemcpyHostToDevice);

    cout << "\nGPU: NVIDIA RTX 4050 | Матрица: " << N << "x" << N << endl;
    cout << "Блок\t| Сетка\t\t| Время (сек)" << endl;
    cout << "---------------------------------------" << endl;

    int block_sizes[] = { 8, 16, 32 };
    for (int bs : block_sizes) {
        dim3 threads(bs, bs);
        dim3 blocks((N + bs - 1) / bs, (N + bs - 1) / bs);

        // Разогрев GPU
        matrixMulKernel << <blocks, threads >> > (d_A, d_B, d_C, N);
        cudaDeviceSynchronize();

        // Замер времени
        cudaEvent_t start, stop;
        cudaEventCreate(&start);
        cudaEventCreate(&stop);

        cudaEventRecord(start);
        matrixMulKernel << <blocks, threads >> > (d_A, d_B, d_C, N);
        cudaEventRecord(stop);
        cudaEventSynchronize(stop);

        float ms = 0;
        cudaEventElapsedTime(&ms, start, stop);
        cout << bs << "x" << bs << "\t| "
            << blocks.x << "x" << blocks.y << "\t| "
            << fixed << setprecision(6) << ms / 1000.0 << " сек" << endl;

        cudaEventDestroy(start);
        cudaEventDestroy(stop);
    }
    cout << "---------------------------------------\n" << endl;

    cudaMemcpy(h_C.data(), d_C, size, cudaMemcpyDeviceToHost);
    writeMatrix("C.txt", h_C, N);

    cudaFree(d_A); cudaFree(d_B); cudaFree(d_C);
    return 0;
}