import matplotlib.pyplot as plt

# Количество потоков
threads = [1, 2, 4, 8]

# Средние значения ускорения (Speedup) из твоей таблицы
speedup_400 = [1.0, 2.11, 3.60, 3.98]
speedup_800 = [1.0, 1.94, 3.50, 4.42]
speedup_1200 = [1.0, 2.03, 3.65, 4.89]
speedup_1600 = [1.0, 2.02, 3.77, 5.73]
speedup_2000 = [1.0, 1.99, 3.84, 4.27]

# Идеальное ускорение (y = x)
ideal = [1, 2, 4, 8]

plt.figure(figsize=(10, 6))

plt.plot(threads, speedup_400, marker='o', label='N = 400')
plt.plot(threads, speedup_800, marker='s', label='N = 800')
plt.plot(threads, speedup_1200, marker='^', label='N = 1200')
plt.plot(threads, speedup_1600, marker='d', label='N = 1600')
plt.plot(threads, speedup_2000, marker='x', label='N = 2000')

# Рисуем линию идеального ускорения пунктиром
plt.plot(threads, ideal, linestyle='--', color='black', label='Идеальное ускорение')

plt.title('Зависимость ускорения от количества потоков (OpenMP)', fontsize=14)
plt.xlabel('Количество потоков', fontsize=12)
plt.ylabel('Ускорение (Speedup)', fontsize=12)
plt.xticks(threads)
plt.legend()
plt.grid(True, linestyle=':', alpha=0.7)

plt.savefig('speedup.png', dpi=300, bbox_inches='tight')
print("График успешно сохранен как speedup.png")