import matplotlib.pyplot as plt

# Месяцы
months = list(range(1, 13))

# Продажи и подписка
sales_per_month = [0, 0, 0, 0, 0, 0, 4, 2, 3, 0, 1, 1]
price_per_subscription = 30000

# Активные клиенты по месяцам
active_clients = []
cumulative_clients = 0
for sale in sales_per_month:
    cumulative_clients += sale
    active_clients.append(cumulative_clients)

# Выручка = подписки * кол-во активных клиентов
revenue = [clients * price_per_subscription for clients in active_clients]

# Расходы:
# Первые 6 месяцев — инвестиционные (по 54 050 руб.), потом эксплуатационные — условно по 13 333 (всего 160 000 / 6) # или 26 666
expenses = [54050] * 6 + [26666] * 6  # более точно, чем 40/20

# Построение графика
plt.figure(figsize=(10, 6))
plt.plot(months, expenses, marker='o', label='Затраты', color='darkorange')
plt.plot(months, revenue, marker='o', label='Выручка', color='steelblue')

plt.title('Внедрение программного продукта', fontsize=14)
plt.xlabel('Месяцы')
plt.ylabel('Рубли')
plt.xticks(months)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()
plt.tight_layout()
plt.savefig("vnedrenie_programmnogo_produkta.png")
plt.show()
