import matplotlib.pyplot as plt

sizes = [200, 400, 800, 1200, 1600, 2000]
t1 = [0.15, 1.32, 9.97, 34.05, 78.06, 174.82]
t2 = [0.04, 0.31, 2.38, 7.45, 17.28, 33.64]
t4 = [0.02, 0.16, 1.25, 3.74, 8.70, 16.91]
t8 = [0.01, 0.08, 0.65, 2.05, 4.60, 8.92]
t16 = [0.01, 0.10, 0.69, 2.13, 4.80, 9.20]

plt.figure(figsize=(10, 6))

plt.plot(sizes, t1, marker='o', label='1 процесс', linewidth=2)
plt.plot(sizes, t2, marker='s', label='2 процесса', linewidth=2)
plt.plot(sizes, t4, marker='^', label='4 процесса', linewidth=2)
plt.plot(sizes, t8, marker='d', label='8 процессов', linewidth=2)
plt.plot(sizes, t16, marker='x', linestyle='--', label='16 процессов (2 узла)', color='purple', linewidth=2)

plt.title('Производительность MPI на суперкомпьютере «Сергей Королёв»', fontsize=14)
plt.xlabel('Размер матрицы (N)', fontsize=12)
plt.ylabel('Время выполнения (сек)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()

plt.savefig('graph_supercomputer.png', dpi=300, bbox_inches='tight')
print("График для кластера создан!")