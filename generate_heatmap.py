import matplotlib.pyplot as plt



matrix = [[0.4,0.2, 0.8, 0.6, 0.2],
          [0.2,0.4, 0.1, 0.8, 0.6],
          [0.95,0.4, 0.2, 0.4, 0.6]
          ]

fig, ax = plt.subplots()
im = ax.imshow(matrix, cmap='hot')

for row in range(3):
    for col in range(5):
        print(col, row)
        text = ax.text(col, row, matrix[row][col], ha="center", va="center", color="w" if matrix[row][col] < 0.5 else 'black')

ax.set_xticks(range(5), labels=range(1,6))
ax.set_yticks(range(3), labels=range(1, 4))
plt.title('2-D Heat Map in Matplotlib')
ax.figure.colorbar(im)
plt.tight_layout()
fig.savefig('heatmap.png')
plt.show()