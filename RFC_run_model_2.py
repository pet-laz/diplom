import joblib
import numpy as np
import pandas as pd
from collections import Counter

# === Загрузка модели и данных ===
clf = joblib.load('trained_model.pkl')
all_symptoms = joblib.load('all_symptoms.pkl')

# Чтение CSV
df = pd.read_csv("diseases.csv", sep=';')
group_names = set(df['GroupName'].dropna().str.strip().str.lower())

# Формирование словарей:
# болезнь → [симптомы], болезнь → врач
disease_symptoms = {}
disease_doctor = {}

for _, row in df.iterrows():
    name = row['Name'].strip()
    doctor = str(row['DoctorName']).strip()
    symptoms = [str(s).strip().lower() for s in row[3:] if pd.notna(s)]
    
    disease_symptoms[name] = symptoms
    disease_doctor[name] = doctor

# === Функции ===

def filter_diseases(symptoms):
    return [d for d in disease_symptoms if all(s in disease_symptoms[d] for s in symptoms)]

def get_top_symptoms(disease_list, known_symptoms, n=4):
    counter = Counter()
    for d in disease_list:
        for s in disease_symptoms[d]:
            s_lower = s.strip().lower()
            if s_lower not in known_symptoms and s_lower not in group_names:
                counter[s_lower] += 1
    return [s for s, _ in counter.most_common(n)]

def predict_disease(selected_symptoms):
    user_features = [1 if symptom in selected_symptoms else 0 for symptom in all_symptoms]
    user_features = np.array(user_features).reshape(1, -1)

    try:
        proba = clf.predict_proba(user_features)[0]
    except ValueError as e:
        print(f"\n❌ Ошибка при предсказании: {e}")
        return

    proba = np.nan_to_num(proba, nan=0.0)
    disease_proba = sorted(zip(clf.classes_, proba), key=lambda x: x[1], reverse=True)

    print("\n🌟 Наиболее вероятные диагнозы и врачи:")
    for disease, probability in disease_proba[:3]:
        doctor = disease_doctor.get(disease, "неизвестен")
        print(f"- {disease} (уверенность: {round(probability * 100, 2)}%) — врач: {doctor}")

# === Основной цикл ===

selected_symptoms = []
rejected_symptoms = set()
rejection_count = 0
max_choices = 7

possible_diseases = list(disease_symptoms.keys())

print("\n👋 Введите первый симптом (например: 'кашель'):")
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

# === Финальный вывод ===

valid_selected = [s for s in selected_symptoms if s in all_symptoms]

if valid_selected:
    print("\n📄 Выбранные симптомы:")
    for symptom in valid_selected:
        print(f"- {symptom}")
    predict_disease(valid_selected)
else:
    print("🚫 Ни один из введённых симптомов не найден в базе. Предсказание невозможно.")
