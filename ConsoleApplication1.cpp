#include <iostream>
#include <fstream>
#include <vector>
#include <chrono>
#include <clocale>

using namespace std;

// Функция для чтения матрицы из файла
bool readMatrix(const string& filename, vector<double>& matrix, int& n) {
    ifstream file(filename);
    if (!file.is_open()) return false;

    file >> n; // Читаем первую строку - размерность
    matrix.resize(n * n);
    for (int i = 0; i < n * n; ++i) {
        file >> matrix[i];
    }
    file.close();
    return true;
}

// Функция для записи матрицы в файл
bool writeMatrix(const string& filename, const vector<double>& matrix, int n) {
    ofstream file(filename);
    if (!file.is_open()) return false;

    file << n << "\n"; // Пишем размерность в первую строку
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            file << matrix[i * n + j] << " ";
        }
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
        cerr << "Ошибка чтения! Сначала сгенерируйте матрицы скриптом Python." << endl;
        return 1;
    }

    if (nA != nB) {
        cerr << "Размеры матриц не совпадают!" << endl;
        return 1;
    }
    int N = nA;
    C.assign(N * N, 0.0); // Инициализируем матрицу C нулями

    cout << "Умножение матриц размером " << N << "x" << N << "..." << endl;

    // Старт замера времени
    auto start = chrono::high_resolution_clock::now();

    // Классический алгоритм перемножения (сложность O(N^3))
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j) {
            double sum = 0.0;
            for (int k = 0; k < N; ++k) {
                sum += A[i * N + k] * B[k * N + j];
            }
            C[i * N + j] = sum;
        }
    }

    // Конец замера времени
    auto end = chrono::high_resolution_clock::now();
    chrono::duration<double> duration = end - start;

    cout << "Время выполнения: " << duration.count() << " секунд." << endl;
    cout << "Объем задачи: приблизительно " << 2.0 * N * N * N << " операций." << endl;

    cout << "Запись результата в C.txt..." << endl;
    if (!writeMatrix("C.txt", C, N)) {
        cerr << "Ошибка записи файла C.txt!" << endl;
        return 1;
    }

    cout << "Успешно завершено." << endl;
    return 0;
}