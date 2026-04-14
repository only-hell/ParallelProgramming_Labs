#include <iostream>
#include <fstream>
#include <vector>
#include <mpi.h>

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

int main(int argc, char* argv[]) {
    MPI_Init(&argc, &argv);

    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    int N = 0;
    vector<double> A, B, C;

    if (rank == 0) {
        int nB;
        if (!readMatrix("A.txt", A, N) || !readMatrix("B.txt", B, nB) || N != nB) {
            cerr << "Error: Could not read matrices A.txt and B.txt properly." << endl;
            MPI_Abort(MPI_COMM_WORLD, 1);
        }
        C.resize(N * N, 0.0);
        if (size == 1) cout << "Matrix size: " << N << "x" << N << endl;
    }

    MPI_Bcast(&N, 1, MPI_INT, 0, MPI_COMM_WORLD);

    if (N % size != 0) {
        if (rank == 0) cerr << "Error: N (" << N << ") must be divisible by the number of processes (" << size << ")." << endl;
        MPI_Finalize();
        return 1;
    }

    int rows_per_proc = N / size;
    int elements_per_proc = rows_per_proc * N;

    vector<double> subA(elements_per_proc);
    vector<double> subC(elements_per_proc, 0.0);
    if (rank != 0) B.resize(N * N);

    MPI_Barrier(MPI_COMM_WORLD);
    double start_time = MPI_Wtime();

    MPI_Scatter(A.data(), elements_per_proc, MPI_DOUBLE, subA.data(), elements_per_proc, MPI_DOUBLE, 0, MPI_COMM_WORLD);
    MPI_Bcast(B.data(), N * N, MPI_DOUBLE, 0, MPI_COMM_WORLD);

    for (int i = 0; i < rows_per_proc; ++i) {
        for (int j = 0; j < N; ++j) {
            double sum = 0.0;
            for (int k = 0; k < N; ++k) {
                sum += subA[i * N + k] * B[k * N + j];
            }
            subC[i * N + j] = sum;
        }
    }

    MPI_Gather(subC.data(), elements_per_proc, MPI_DOUBLE, C.data(), elements_per_proc, MPI_DOUBLE, 0, MPI_COMM_WORLD);

    double end_time = MPI_Wtime();

    if (rank == 0) {
        cout << "Processes: " << size << " \t| Time: " << end_time - start_time << " sec" << endl;
        writeMatrix("C.txt", C, N);
    }

    MPI_Finalize();
    return 0;
}