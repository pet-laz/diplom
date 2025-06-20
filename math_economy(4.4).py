import numpy as np

# Данные по месяцам (начиная с 1 месяца до 12)
# Доходы (Rt) — берем из строки 9 таблицы: "Поток доходов"
# Rt = np.array([45500, 45500, 45500, 45500, 45500, 45500, 315500, 423500, 531500, 558500, 558500, 504500])
Rt = np.array([54050,54050,54050,84050,	144050,144050,174050,234050,324050,324050,354050,384050])

# Расходы (Zt) — берем из строки 21 таблицы: "Поток расходов"
Zt = np.array([144824, 143940, 143538, 142882, 142032, 141537, 56210, 55661, 54953, 54016, 53498, 52731])

# Дисконтная ставка (годовая 18%) -> месячная ставка
E = 0.18 / 12  # 0.015

# Чистый дисконтированный доход (ЧДД)
t = np.arange(1, 13)
NPV = np.sum((Rt - Zt) / (1 + E) ** t)

# Объем инвестиций (сумма всех инвестиционных расходов — строка 12)
Inv = np.sum([91000] * 6)  # 6 месяцев по 91 000

# Индекс доходности (ИД)
PI = NPV / Inv

# Срок окупаемости: приближенно, ищем когда накопленный дисконтированный поток становится >= инвестиции
cumulative_cashflow = 0
payback_period = 0
for i in range(12):
    cashflow = (Rt[i] - Zt[i]) / (1 + E) ** (i + 1)
    cumulative_cashflow += cashflow
    if cumulative_cashflow >= Inv:
        payback_period = i + 1
        break

print(NPV, PI, payback_period)


#######============ VND =============##########
import numpy as np
from scipy.optimize import newton

# Данные по периодам (12 месяцев)
Rt = [45500, 45500, 45500, 45500, 45500, 45500, 315500, 423500, 531500, 558500, 558500, 504500]  # Доходы
Zt = [91000, 91000, 91000, 91000, 91000, 91000, 6500, 6500, 6500, 6500, 6500, 6500]  # Расходы

# Функция NPV (чистый дисконтированный доход) при заданной ставке E
def npv(E):
    return sum((Rt[t] - Zt[t]) / (1 + E) ** (t + 1) for t in range(12))

# Используем метод Ньютона для поиска E, при котором NPV = 0 (это и будет ВНД)
initial_guess = 0.3  # начальное приближение (30%)
irr = newton(npv, initial_guess)

# Преобразуем в проценты
irr_percent = irr * 100
print(irr_percent)
