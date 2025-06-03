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

# Настройка оси X
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

# Переворачиваем ось Y, чтобы этапы шли сверху вниз
ax.invert_yaxis()

# Подписи и оформление
ax.set_title("Диаграмма Ганта: Этапы разработки")
ax.set_xlabel("Сроки")
ax.set_ylabel("Этапы")
plt.grid(axis='x', linestyle='--', alpha=0.5)
plt.tight_layout()

# Сохраняем и показываем
plt.savefig("diagramma_ganta.png")
plt.show()


# === КРИВАЯ ПРОДАЖ ===
months = list(range(1, 13))
sales_per_month = [0, 0, 0, 0, 0, 0, 2, 2, 3, 2, 1, 1]
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
plt.ylabel("Количество продаж")
plt.xticks(months)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()
plt.tight_layout()
plt.savefig("krivaya_prodazh.png")
plt.show()


# # === КРИВАЯ ОКУПАЕМОСТИ (подписочная модель) ===

# price_per_month = 30000
# active_clients = []
# cumulative_clients = 0

# # Подсчёт активных клиентов к каждому месяцу
# for sale in sales_per_month:
#     cumulative_clients += sale
#     active_clients.append(cumulative_clients)

# monthly_revenue = [clients * price_per_month for clients in active_clients]
# # monthly_expenses = [40000] * 6 + [20000] * 6
# # Первые 6 месяцев — инвестиционные (по 54 050 руб.), потом эксплуатационные — условно по 13 333 (всего 160 000 / 6)
# monthly_expenses = [54050] * 6 + [4000] * 6  # более точно, чем 40/20

# balance = -324300
# cumulative_profit = []
# for rev, exp in zip(monthly_revenue, monthly_expenses):
#     balance += rev - exp
#     cumulative_profit.append(balance)

# # Построение графика
# plt.figure(figsize=(10, 5))
# plt.plot(months, cumulative_profit, marker='o', color='forestgreen', label='Кумулятивная прибыль')
# plt.axhline(0, color='red', linestyle='--', label='Точка окупаемости')

# plt.title("Кривая окупаемости проекта", fontsize=14)
# plt.xlabel("Месяц")
# plt.ylabel("Финансовый результат (руб.)")
# plt.xticks(months)
# plt.grid(True, linestyle='--', alpha=0.5)
# plt.legend()
# plt.tight_layout()
# plt.savefig("krivaya_okupaemosti.png")
# plt.show()

# === КРИВАЯ ОКУПАЕМОСТИ 2 (подписочная модель) ===
# Исправление длины массива месяцев (12 месяцев вместо 13)
months = list(range(1, 12 + 1))
cash_flows = [
    -88100, -87515, -86930, -86345, -85759, -85174,
    25462, 86047, 176633, 237219, 267804, 298389
]

# Перерасчёт кумулятивного денежного потока
cumulative_cash_flow = []
balance = 0
for cf in cash_flows:
    balance += cf
    cumulative_cash_flow.append(balance)

# Построение графика
plt.figure(figsize=(10, 5))
plt.plot(months, cumulative_cash_flow, marker='o', color='forestgreen', label='Кумулятивная прибыль')
plt.axhline(0, color='red', linestyle='--', label='Точка окупаемости')

plt.title("Кривая окупаемости проекта", fontsize=14)
plt.xlabel("Месяц")
plt.ylabel("Финансовый результат (руб.)")
plt.xticks(months)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()
plt.tight_layout()
plt.show()