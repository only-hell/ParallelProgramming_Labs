import matplotlib.pyplot as plt

threads = [1, 2, 4, 8]

speedup_400 = [1.0, 1.94, 2.88, 4.00]
speedup_800 = [1.0, 2.01, 3.03, 4.31]
speedup_1200 = [1.0, 2.24, 4.88, 6.95]
speedup_1600 = [1.0, 1.98, 4.20, 4.71]
speedup_2000 = [1.0, 1.94, 3.60, 4.31]
ideal = [1, 2, 4, 8]

plt.figure(figsize=(10, 6))

plt.plot(threads, speedup_400, marker='o', label='N = 400')
plt.plot(threads, speedup_800, marker='s', label='N = 800')
plt.plot(threads, speedup_1200, marker='^', label='N = 1200', linewidth=3) # Выделяем суперлинейное
plt.plot(threads, speedup_1600, marker='d', label='N = 1600')
plt.plot(threads, speedup_2000, marker='x', label='N = 2000')

plt.plot(threads, ideal, linestyle='--', color='black', label='Идеальное ускорение')

plt.title('Зависимость ускорения от количества процессов (MPI)', fontsize=14)
plt.xlabel('Количество процессов (MPI Ranks)', fontsize=12)
plt.ylabel('Ускорение (Speedup)', fontsize=12)
plt.xticks(threads)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)

plt.savefig('speedup_mpi.png', dpi=300, bbox_inches='tight')
print("График MPI успешно сохранен!")