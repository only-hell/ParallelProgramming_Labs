#include <iostream>
#include <fstream>
#include <vector>
#include <omp.h>
#include <clocale>
#include <iomanip>

using namespace std;

// Функция для чтения матрицы
bool readMatrix(const string& filename, vector<double>& matrix, int& n) {
    ifstream file(filename);
    if (!file.is_open()) return false;
    file >> n;
    matrix.resize(n * n);
    for (int i = 0; i < n * n; ++i) file >> matrix[i];
    file.close();
    return true;
}

// Функция для записи матрицы
bool writeMatrix(const string& filename, const vector<double>& matrix, int n) {
    ofstream file(filename);
    if (!file.is_open()) return false;
    file << n << "\n";
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) file << matrix[i * n + j] << " ";
        file << "\n";
    }
    file.close();
    return true;
}

int main() {
    setlocale(LC_ALL, "Russian");
    int nA, nB;
    vector<double> A, B, C;

    cout << "Чтение матриц A.txt и B.txt..." << endl;
    if (!readMatrix("A.txt", A, nA) || !readMatrix("B.txt", B, nB)) {
        cerr << "Ошибка: Сначала сгенерируйте матрицы скриптом Python." << endl;
        return 1;
    }

    if (nA != nB) {
        cerr << "Ошибка: Размеры матриц не совпадают!" << endl;
        return 1;
    }
    int N = nA;
    C.assign(N * N, 0.0);

    cout << "\nУмножение матриц размером " << N << "x" << N << endl;
    cout << "--------------------------------------------------------" << endl;
    cout << "Потоки\t| Время (сек)\t| Ускорение\t| Эффективность" << endl;
    cout << "--------------------------------------------------------" << endl;

    vector<int> thread_counts = { 1, 2, 4, 8 };
    double time_1_thread = 0.0;

    // Автоматический прогон для разного числа потоков
    for (int threads : thread_counts) {
        omp_set_num_threads(threads);
        fill(C.begin(), C.end(), 0.0); // Сбрасываем матрицу C перед каждым тестом

        double start_time = omp_get_wtime(); // Таймер OpenMP

        // --- ПАРАЛЛЕЛЬНАЯ ОБЛАСТЬ ---
#pragma omp parallel for shared(A, B, C)
        for (int i = 0; i < N; ++i) {
            for (int j = 0; j < N; ++j) {
                double sum = 0.0;
                for (int k = 0; k < N; ++k) {
                    sum += A[i * N + k] * B[k * N + j];
                }
                C[i * N + j] = sum;
            }
        }

        double end_time = omp_get_wtime();
        double current_time = end_time - start_time;

        if (threads == 1) time_1_thread = current_time;

        double speedup = time_1_thread / current_time;
        double efficiency = (speedup / threads) * 100.0;

        cout << threads << "\t| "
            << fixed << setprecision(4) << current_time << " сек\t| "
            << setprecision(2) << speedup << "x\t\t| "
            << setprecision(1) << efficiency << " %" << endl;
    }
    cout << "--------------------------------------------------------" << endl;

    cout << "Запись результата 8-поточного вычисления в C.txt..." << endl;
    writeMatrix("C.txt", C, N);

    return 0;
}
