import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 6))

ax.set_xlim(0, 10)
ax.set_ylim(0, 8)
ax.axis('off')

plt.title("My First Neural Network", fontsize=16)

input_layer = [(2, 2), (2, 4), (2, 6)]
hidden_layer = [(5, 1.5), (5, 3.5), (5, 4.5), (5, 6.5)]
output_layer = [(8, 3), (8, 5)]

all_neurons = input_layer + hidden_layer + output_layer

for (x, y) in all_neurons:
    circle = plt.Circle((x, y), radius=0.3, color='skyblue', ec='black', zorder=2)
    ax.add_patch(circle)

for (x1, y1) in input_layer:
    for (x2, y2) in hidden_layer:
        ax.plot([x1, x2], [y1, y2], color='gray', linewidth=0.5, zorder=1)

for (x1, y1) in hidden_layer:
    for (x2, y2) in output_layer:
        ax.plot([x1, x2], [y1, y2], color='gray', linewidth=0.5, zorder=1)

ax.text(2, 7.5, "Input Layer", ha='center', fontsize=12, fontweight='bold')
ax.text(5, 7.5, "Hidden Layer", ha='center', fontsize=12, fontweight='bold')
ax.text(8, 7.5, "Output Layer", ha='center', fontsize=12, fontweight='bold')

plt.show()
