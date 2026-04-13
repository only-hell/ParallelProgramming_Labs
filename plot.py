import matplotlib.pyplot as plt

# Данные из твоего эксперимента: N и среднее время в секундах
sizes = [400, 800, 1200]
times = [0.315, 2.437, 9.597]

plt.figure(figsize=(8, 5))
plt.plot(sizes, times, marker='o', linestyle='-', color='b', linewidth=2)
plt.title('Производительность последовательного алгоритма')
plt.xlabel('Размер матрицы (N)')
plt.ylabel('Время (сек)')
plt.grid(True)

plt.savefig('graph.png', dpi=300)
print('График graph.png успешно создан')
