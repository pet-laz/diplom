import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Создание рисунка и осей
fig, ax = plt.subplots(figsize=(10, 8))
ax.set_xlim(-2, 10)
ax.set_ylim(-2, 10)
ax.axis('off')

# Добавление кругов TAM, SAM, SOM
tam_circle = patches.Circle((5, 5), 4.5, edgecolor='blue', facecolor='lightblue', linewidth=2, label='TAM')
sam_circle = patches.Circle((5, 5), 3, edgecolor='green', facecolor='lightgreen', linewidth=2, label='SAM')
som_circle = patches.Circle((5, 5), 1.5, edgecolor='orange', facecolor='wheat', linewidth=2, label='SOM')

# Добавляем круги на ось
ax.add_patch(tam_circle)
ax.add_patch(sam_circle)
ax.add_patch(som_circle)

# Добавляем подписи внутрь кругов
ax.text(5, 8.7, '100 266\nклиник', ha='center', va='center', fontsize=12) # , fontweight='bold'
ax.text(5, 7, f'{int(100266*0.16)}\nклиник', ha='center', va='center', fontsize=10)
ax.text(5, 5, f'{int(100266*0.16*0.2)}\nклиник', ha='center', va='center', fontsize=9)

# Добавление текстовых блоков справа
ax.text(11, 8, 'Общий объем рынка\n3 007 980 00 рублей', va='top', fontsize=10)
ax.text(11, 5, 'Доступный объем рынка\n481 276 800  рублей', fontsize=10)
ax.text(11, 2, 'Реально достижимый объем рынка\n96 255 360 рублей', va='bottom', fontsize=10)

plt.title('Рынки TAM, SAM, SOM', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()
