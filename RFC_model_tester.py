import joblib
import pandas as pd
import numpy as np
import random

# === Настройки ===
NUM_TESTS_PER_DISEASE = 20     # Кол-во тестов на каждую болезнь
MIN_MODIFICATIONS = 1          # Минимум изменяемых симптомов
MAX_MODIFICATIONS = 3          # Максимум изменяемых симптомов

# === Загрузка модели и данных ===
clf = joblib.load("trained_model.pkl")
all_symptoms = joblib.load("all_symptoms.pkl")
df = pd.read_csv("diseases.csv", delimiter=";")

# === Подготовка данных ===
disease_symptom_map = {}
for _, row in df.iterrows():
    disease = row["Name"]
    symptoms = [str(s).strip().lower() for s in row[3:] if pd.notna(s)]
    disease_symptom_map[disease] = symptoms

# === Тестирование ===
total_tests = 0
correct_predictions = 0
test_examples = []

for disease, original_symptoms in disease_symptom_map.items():
    for _ in range(NUM_TESTS_PER_DISEASE):
        # Сохраняем оригинальные симптомы отдельно
        saved_original = original_symptoms.copy()
        modified_symptoms = saved_original.copy()

        # Определяем количество изменений
        max_allowed_mods = min(MAX_MODIFICATIONS, len(modified_symptoms))
        if max_allowed_mods < MIN_MODIFICATIONS:
            continue  # Пропустить, если недостаточно симптомов

        num_modifications = random.randint(MIN_MODIFICATIONS, max_allowed_mods)

        # Удаление или замена симптомов
        for _ in range(num_modifications):
            if modified_symptoms:
                to_change = random.choice(modified_symptoms)
                modified_symptoms.remove(to_change)
                # 50% шанс заменить удалённый симптом на случайный другой
                if random.random() < 0.5:
                    substitute = random.choice([s for s in all_symptoms if s not in modified_symptoms])
                    modified_symptoms.append(substitute)

        # Векторизация симптомов
        features = [1 if symptom in modified_symptoms else 0 for symptom in all_symptoms]
        X = np.array(features).reshape(1, -1)

        # Предсказание
        prediction = clf.predict(X)[0]

        test_examples.append({
            'disease': disease,
            'original': saved_original,
            'modified': modified_symptoms,
            'predicted': prediction,
            'correct': prediction == disease
        })

        if prediction == disease:
            correct_predictions += 1
        total_tests += 1

# === Результат ===
accuracy = correct_predictions / total_tests * 100
print(f"\n📊 Точность модели на искажённых данных: {accuracy:.2f}% ({correct_predictions} из {total_tests})")

count_random_examples = 3

print(f"\n🔎 Примеры тестов ({count_random_examples} случайных):")
for example in random.sample(test_examples, min(count_random_examples, len(test_examples))):
    status = "✅" if example['correct'] else "❌"
    print(f"{status} {example['disease']}:")
    print(f"    Изначальные симптомы: {', '.join(example['original'])}")
    print(f"    Изменённые симптомы:  {', '.join(example['modified'])}")
    print(f"    Предсказание модели:  {example['predicted']}\n")
