import matplotlib.pyplot as plt

# Размеры матриц
sizes = [400, 800, 1200, 1600, 2000]

# Средние значения времени на GPU (твои данные в сек)
gpu_times = [0.0011, 0.0064, 0.0228, 0.0516, 0.0984]

plt.figure(figsize=(10, 6))
plt.plot(sizes, gpu_times, marker='o', linestyle='-', color='g', linewidth=2, label='NVIDIA RTX 4050')

plt.title('Производительность вычислений на GPU (CUDA)', fontsize=14)
plt.xlabel('Размер матрицы (N)', fontsize=12)
plt.ylabel('Время выполнения (сек)', fontsize=12)
plt.yscale('log') # Логарифмическая шкала лучше покажет рост на таких малых числах
plt.grid(True, which="both", linestyle='--', alpha=0.5)
plt.legend()

plt.savefig('graph_cuda.png', dpi=300, bbox_inches='tight')
print("График graph_cuda.png создан!")