import matplotlib.pyplot as plt

sizes = [200, 400, 800, 1200, 1600, 2000]
times = [0.061, 0.315, 2.437, 9.597, 28.750, 84.517]

plt.figure(figsize=(10, 6))
plt.plot(sizes, times, marker='o', linestyle='-', color='b', linewidth=2)

plt.title('Производительность последовательного алгоритма (ЛР №1)', fontsize=14)
plt.xlabel('Размер матрицы (N)', fontsize=12)
plt.ylabel('Время выполнения (сек)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)

# Добавляем подписи значений над точками для наглядности
for i, txt in enumerate(times):
    plt.annotate(f"{txt}s", (sizes[i], times[i]), textcoords="offset points", xytext=(0,10), ha='center')

plt.savefig('Graph.png', dpi=300, bbox_inches='tight')
print("Обновленный график graph.png создан!")
