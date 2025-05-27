import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

# === ДИАГРАММА ГАНТА ===
tasks = [
    ("Анализ предметной области", 30),
    ("Техническое задание и архитектура", 30),
    ("Разработка модели и алгоритмов", 30),
    ("Реализация функционала и тестирование", 60),
    ("Подготовка базы и отладка", 30)
]

start_date = datetime(2025, 1, 1)
colors = ['tab:blue', 'tab:blue', 'tab:green', 'tab:green', 'tab:green']

fig, ax = plt.subplots(figsize=(10, 5))

for i, (task, days) in enumerate(tasks):
    start = start_date + timedelta(days=sum(t[1] for t in tasks[:i]))
    end = start + timedelta(days=days)
    ax.barh(task, (end - start).days, left=start, color=colors[i])

ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax.set_title("Диаграмма Ганта: Этапы разработки")
ax.set_xlabel("Сроки")
ax.set_ylabel("Этапы")
plt.grid(axis='x', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig("diagramma_ganta.png")
plt.show()


# === КРИВАЯ ПРОДАЖ ===
months = list(range(1, 13))
sales_per_month = [0, 0, 0, 1, 2, 0, 1, 2, 3, 0, 1, 1]
cumulative_sales = []
total = 0
for sale in sales_per_month:
    total += sale
    cumulative_sales.append(total)

plt.figure(figsize=(10, 5))
plt.plot(months, cumulative_sales, marker='o', color='steelblue', label='Накопленные подключения клиник')
plt.fill_between(months, cumulative_sales, color='steelblue', alpha=0.1)

plt.title("Кривая продаж программного модуля", fontsize=14)
plt.xlabel("Месяц")
plt.ylabel("Количество подключений")
plt.xticks(months)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()
plt.tight_layout()
plt.savefig("krivaya_prodazh.png")
plt.show()


# === КРИВАЯ ОКУПАЕМОСТИ (подписочная модель) ===

price_per_month = 30000
active_clients = []
cumulative_clients = 0

# Подсчёт активных клиентов к каждому месяцу
for sale in sales_per_month:
    cumulative_clients += sale
    active_clients.append(cumulative_clients)

monthly_revenue = [clients * price_per_month for clients in active_clients]
monthly_expenses = [40000] * 6 + [20000] * 6

balance = -324300
cumulative_profit = []
for rev, exp in zip(monthly_revenue, monthly_expenses):
    balance += rev - exp
    cumulative_profit.append(balance)

# Построение графика
plt.figure(figsize=(10, 5))
plt.plot(months, cumulative_profit, marker='o', color='forestgreen', label='Кумулятивная прибыль')
plt.axhline(0, color='red', linestyle='--', label='Точка окупаемости')

plt.title("Кривая окупаемости проекта", fontsize=14)
plt.xlabel("Месяц")
plt.ylabel("Финансовый результат (руб.)")
plt.xticks(months)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()
plt.tight_layout()
plt.savefig("krivaya_okupaemosti.png")
plt.show()
