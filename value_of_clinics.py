import matplotlib.pyplot as plt

years = list(range(2013, 2024))
# private_clinics_share = [23.4, 25.0, 26.5, 28.0, 30.0, 32.0, 34.0, 35.5, 36.5, 38.0]
private_clinics_share = [56756, 61321, 62312, 67419, 72394, 78412, 85391, 93451, 97562, 100266, 100562]
plt.figure(figsize=(10, 6))
plt.plot(years, private_clinics_share, marker='o', linestyle='-', color='blue')
plt.title('Количество частных клиник в России')
plt.xlabel('Год')
plt.ylabel('Количество')
plt.grid(True)
plt.tight_layout()
plt.show()