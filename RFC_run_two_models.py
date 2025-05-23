import joblib
import numpy as np
import pandas as pd
from collections import Counter

# === Загрузка моделей и данных ===
group_clf = joblib.load("group_model.pkl")
from sklearn.ensemble import RandomForestClassifier
all_symptoms = joblib.load("all_symptoms.pkl")
group_encoder = joblib.load("group_encoder.pkl")
df = pd.read_csv("diseases.csv", delimiter=";")

# === Подготовка вспомогательных структур ===
# Группировка диагнозов по группам
group_to_diseases = {}
disease_to_group = {}

for _, row in df.iterrows():
    group = row["GroupName"]
    disease = row["Name"]
    group_to_diseases.setdefault(group, []).append(disease)
    disease_to_group[disease] = group

# === Алгоритм подсказок ===
def filter_diseases(symptoms):
    matches = []
    for _, row in df.iterrows():
        disease = row["Name"]
        disease_symptoms = [str(s).strip().lower() for s in row[3:] if pd.notna(s)]
        if all(symptom in disease_symptoms for symptom in symptoms):
            matches.append(disease)
    return matches

def get_top_symptoms(diseases, exclude):
    counter = Counter()
    for disease in diseases:
        symptoms = df[df["Name"] == disease].iloc[0, 3:]
        symptoms = [str(s).strip().lower() for s in symptoms if pd.notna(s)]
        counter.update(s for s in symptoms if s not in exclude)
    return [s for s, _ in counter.most_common(4)]

# === Интерфейс ===
print("👋 Введите первый симптом (например: 'кашель'):")
selected_symptoms = []
rejected_symptoms = set()
max_choices = 7
rejection_count = 0

initial = input("🧠 Ваш выбор: ").strip().lower()
selected_symptoms.append(initial)

while len(selected_symptoms) < max_choices and rejection_count < 3:
    possible_diseases = filter_diseases(selected_symptoms)
    
    if not possible_diseases:
        print("😕 Подходящих диагнозов не найдено.")
        break

    already_seen = set(selected_symptoms) | rejected_symptoms
    top_suggestions = get_top_symptoms(possible_diseases, already_seen)

    if not top_suggestions:
        print("🔍 Больше нет симптомов для уточнения.")
        break

    print("\n🤔 Какие из следующих симптомов вы наблюдаете?")
    for idx, s in enumerate(top_suggestions, 1):
        print(f"{idx}. {s}")
    print(f"{len(top_suggestions) + 1}. Ни один из них")

    choice = input("👉 Ваш выбор (номер): ").strip()

    if choice.isdigit():
        choice = int(choice)
        if 1 <= choice <= len(top_suggestions):
            selected_symptoms.append(top_suggestions[choice - 1])
        else:
            print("🙅 Ни один симптом не подошел.")
            rejected_symptoms.update(top_suggestions)
            rejection_count += 1
    else:
        print("⚠️ Введите номер!")

# === Векторизация ===
feature_vector = [1 if s in selected_symptoms else 0 for s in all_symptoms]
X = np.array(feature_vector).reshape(1, -1)

# === Предсказание группы ===
predicted_group = group_clf.predict(X)[0]
print(f"\n📚 Предсказанная группа заболеваний: {predicted_group}")

# === Предсказание диагноза ===
filtered_df = df[df["GroupName"] == predicted_group]
filtered_diseases = filtered_df["Name"].tolist()

X_filtered = []
y_filtered = []

for _, row in filtered_df.iterrows():
    disease_symptoms = [str(s).strip().lower() for s in row[3:] if pd.notna(s)]
    features = [1 if s in disease_symptoms else 0 for s in all_symptoms]
    X_filtered.append(features)
    y_filtered.append(row["Name"])

if not X_filtered:
    print("❌ Не удалось найти диагноз в предсказанной группе.")
else:
    # Обучаем временную модель на подмножестве диагнозов этой группы
    temp_clf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    temp_clf.fit(X_filtered, y_filtered)
    disease_prediction = temp_clf.predict(X)[0]
    print(f"🩺 Предполагаемый диагноз: {disease_prediction}")