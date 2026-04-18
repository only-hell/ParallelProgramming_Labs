import matplotlib.pyplot as plt

sizes = [200, 400, 800, 1200, 1600, 2000]
b8 = [0.000105, 0.000785, 0.006211, 0.021000, 0.050300, 0.097800]
b16 = [0.000110, 0.000790, 0.006188, 0.022100, 0.046800, 0.081200]
b32 = [0.000152, 0.000860, 0.006800, 0.022600, 0.042000, 0.081000]

plt.figure(figsize=(10, 6))
plt.plot(sizes, b8, marker='o', label='Block 8x8')
plt.plot(sizes, b16, marker='s', label='Block 16x16')
plt.plot(sizes, b32, marker='^', label='Block 32x32')

plt.title('Производительность CUDA на разных конфигурациях сетки', fontsize=14)
plt.xlabel('Размер матрицы (N)', fontsize=12)
plt.ylabel('Время выполнения (сек)', fontsize=12)
plt.yscale('log')
plt.grid(True, which="both", linestyle='--', alpha=0.5)
plt.legend()

plt.savefig('graph_cuda.png', dpi=300, bbox_inches='tight')
print("График graph_cuda.png создан!")import matplotlib.pyplot as plt

sizes = [200, 400, 800, 1200, 1600, 2000]
b8 = [0.000105, 0.000785, 0.006211, 0.021000, 0.050300, 0.097800]
b16 = [0.000110, 0.000790, 0.006188, 0.022100, 0.046800, 0.081200]
b32 = [0.000152, 0.000860, 0.006800, 0.022600, 0.042000, 0.081000]

plt.figure(figsize=(10, 6))
plt.plot(sizes, b8, marker='o', label='Block 8x8')
plt.plot(sizes, b16, marker='s', label='Block 16x16')
plt.plot(sizes, b32, marker='^', label='Block 32x32')

plt.title('Производительность CUDA на разных конфигурациях сетки', fontsize=14)
plt.xlabel('Размер матрицы (N)', fontsize=12)
plt.ylabel('Время выполнения (сек)', fontsize=12)
plt.yscale('log')
plt.grid(True, which="both", linestyle='--', alpha=0.5)
plt.legend()

plt.savefig('graph_cuda.png', dpi=300, bbox_inches='tight')
print("График graph_cuda.png создан!")
