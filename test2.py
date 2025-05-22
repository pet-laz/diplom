import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import numpy as np

# Загружаем базу болезней
data = pd.read_csv("diseases.csv", delimiter=";")

# Составляем список всех уникальных симптомов
all_symptoms = []
for i in range(3, data.shape[1]):
    all_symptoms += data.iloc[:, i].dropna().tolist()
all_symptoms = sorted(list(set(all_symptoms)))

# Создаем обучающие данные
X = []
y = []

for idx, row in data.iterrows():
    disease_symptoms = row[3:].dropna().tolist()
    features = [1 if symptom in disease_symptoms else 0 for symptom in all_symptoms]
    X.append(features)
    y.append(row.iloc[0])

# Обучаем дерево решений
clf = DecisionTreeClassifier()
clf.fit(X, y)

# ----------- Консольное взаимодействие ------------

print("👉 Введите первый симптом вручную (например: Кашель, Боль в горле):")
first_symptom = input("Ваш симптом: ").strip()

selected_symptoms = [first_symptom]

# Убираем уже выбранные симптомы из общего списка
remaining_symptoms = [s for s in all_symptoms if s.lower() != first_symptom.lower()]

print("\n📋 Теперь выберите дополнительные симптомы:")

batch_size = 4  # сколько симптомов показывать за раз
index = 0

while index < len(remaining_symptoms):
    current_batch = remaining_symptoms[index:index+batch_size]
    for idx, symptom in enumerate(current_batch, 1):
        print(f"{idx}. {symptom}")
    print(f"{len(current_batch)+1}. НИ ОДИН ИЗ СИМПТОМОВ НЕ ПОДХОДИТ")

    user_choice = input("Ваш выбор (номер): ")

    if not user_choice.isdigit():
        print("❗ Пожалуйста, введите номер.")
        continue

    user_choice = int(user_choice)

    if 1 <= user_choice <= len(current_batch):
        chosen_symptom = current_batch[user_choice-1]
        selected_symptoms.append(chosen_symptom)
        print(f"✅ Вы выбрали: {chosen_symptom}")
    elif user_choice == len(current_batch) + 1:
        print("➡️ Переходим к следующему списку симптомов.")
    else:
        print("❗ Неверный номер. Попробуйте снова.")
        continue

    index += batch_size  # Переход к следующей группе симптомов

print("\n📄 Выбранные симптомы:")
for symptom in selected_symptoms:
    print(f"- {symptom}")

# Формируем входной вектор для предсказания
user_features = [1 if symptom in selected_symptoms else 0 for symptom in all_symptoms]
user_features = np.array(user_features).reshape(1, -1)

# Предсказываем вероятности по всем классам
proba = clf.predict_proba(user_features)[0]

# Собираем список болезней с вероятностями
disease_proba = list(zip(clf.classes_, proba))
disease_proba.sort(key=lambda x: x[1], reverse=True)  # сортируем по вероятности убыванию

# Выводим Топ-3
print("\n🌟 Наиболее вероятные болезни:")

for disease, probability in disease_proba[:3]:
    print(f"- {disease} (уверенность: {round(probability * 100, 2)}%)")
