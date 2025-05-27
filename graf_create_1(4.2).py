import matplotlib.pyplot as plt

# Месяцы (1 год)
months = list(range(1, 13))

# Затраты по месяцам (в рублях)
# 6 месяцев разработки: равномерные затраты, затем эксплуатационные ниже
expenses = [20000] * 6 + [13333] * 6

# Выручка по месяцам (в рублях)
# До 7-го месяца — 0, затем выручка растёт и стабилизируется
rev_exneses = []
for i in range(len(expenses)):
    rev_exneses.append(i * -1)

revenue = rev_exneses + [100000, 150000, 200000, 220000, 230000, 200000]

# Построение графика
plt.figure(figsize=(10, 6))
plt.plot(months, expenses, marker='o', label='Затраты', color='darkorange')
plt.plot(months, revenue, marker='o', label='Выручка', color='gray')

plt.title('Внедрение программного продукта', fontsize=14)
plt.xlabel('Месяцы')
plt.ylabel('Рубли')
plt.xticks(months)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()
plt.tight_layout()

# Сохранение изображения
output_path = "vnedrenie_programmnogo_produkta.png"
plt.savefig(output_path)
plt.show()