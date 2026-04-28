import numpy as np
import time
import sys


def generate_matrices(n, file_a='A.txt', file_b='B.txt'):
    print(f"Генерация матриц {n}x{n}...")
    # Генерируем случайные матрицы со значениями от 0 до 10
    A = np.random.rand(n, n) * 10
    B = np.random.rand(n, n) * 10

    # Сохраняем в текстовые файлы (первая строка - размер матрицы)
    with open(file_a, 'w') as f:
        f.write(f"{n}\n")
        np.savetxt(f, A, fmt='%.4f')

    with open(file_b, 'w') as f:
        f.write(f"{n}\n")
        np.savetxt(f, B, fmt='%.4f')

    print("Матрицы A.txt и B.txt успешно сгенерированы.")


def verify_result(file_a='A.txt', file_b='B.txt', file_c='C.txt'):
    print("Загрузка матриц для проверки...")
    try:
        # Пропускаем первую строку с размером при чтении
        A = np.loadtxt(file_a, skiprows=1)
        B = np.loadtxt(file_b, skiprows=1)
        C_cpp = np.loadtxt(file_c, skiprows=1)
    except FileNotFoundError:
        print("❌ Ошибка: Не найдены файлы матриц. Сначала запустите C++ программу.")
        return

    print("Вычисление эталонного результата в Python (NumPy)...")
    start = time.time()
    C_py = np.dot(A, B)
    print(f"Время умножения в Python: {time.time() - start:.4f} сек")

    # Сравниваем матрицы с допустимой погрешностью (из-за разницы типов float/double)
    if np.allclose(C_cpp, C_py, atol=1e-3):
        print("\n✅ ВЕРИФИКАЦИЯ ПРОЙДЕНА! Результаты C++ и Python совпадают.")
    else:
        print("\n❌ ОШИБКА! Результаты C++ программы неверны.")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "gen":
            size = int(sys.argv[2]) if len(sys.argv) > 2 else 400
            generate_matrices(size)
        elif sys.argv[1] == "check":
            verify_result()
    else:
        print("Использование:")
        print("  python matrix_utils.py gen 400  - генерация матриц 400x400")
        print("  python matrix_utils.py check    - проверка результата C.txt")
