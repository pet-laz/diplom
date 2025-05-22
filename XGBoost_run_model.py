import joblib
import numpy as np
import pandas as pd
from collections import Counter
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder

# Загружаем модель, симптомы и LabelEncoder
clf = joblib.load('xgb_model.pkl')
all_symptoms = joblib.load('xgb_symptoms.pkl')
label_encoder = joblib.load('label_encoder.pkl')

# Функция для предсказания болезни с обработкой NaN
def predict_disease(selected_symptoms):
    user_features = [1 if symptom in selected_symptoms else 0 for symptom in all_symptoms]
    user_features = np.array(user_features).reshape(1, -1)

    try:
        proba = clf.predict_proba(user_features)[0]
        proba = np.nan_to_num(proba, nan=0.0)
        classes = label_encoder.inverse_transform(np.arange(len(proba)))
        disease_proba = list(zip(classes, proba))
        disease_proba.sort(key=lambda x: x[1], reverse=True)

        print("\n🌟 Наиболее вероятные диагнозы:")
        for disease, probability in disease_proba[:3]:
            print(f"- {disease} (уверенность: {round(probability * 100, 2)}%)")
    except Exception as e:
        print("\n❌ Ошибка при предсказании:", e)

# Загружаем CSV
df = pd.read_csv("diseases.csv", sep=';')

disease_symptoms = {}

for _, row in df.iterrows():
    name = row['Name']
    symptoms = [str(s).strip().lower() for s in row[3:] if pd.notna(s)]
    disease_symptoms[name] = symptoms


selected_symptoms = []
rejection_count = 0
max_choices = 7
possible_diseases = list(disease_symptoms.keys())

print("👋 Введите первый симптом (например: 'кашель'):")
initial = input("🧠 Ваш выбор: ").strip().lower()
selected_symptoms.append(initial)

def filter_diseases(symptoms):
    return [d for d in possible_diseases if all(s in disease_symptoms[d] for s in symptoms)]

def get_top_symptoms(disease_list, known_symptoms, n=4):
    counter = Counter()
    for d in disease_list:
        for s in disease_symptoms[d]:
            if s not in known_symptoms:
                counter[s] += 1
    return [s for s, _ in counter.most_common(n)]

while len(selected_symptoms) < max_choices and rejection_count < 3:
    possible_diseases = filter_diseases(selected_symptoms)
    if not possible_diseases:
        print("😕 Подходящих диагнозов не найдено.")
        break

    top_suggestions = get_top_symptoms(possible_diseases, selected_symptoms)
    if not top_suggestions:
        print("🔍 Больше нет симптомов для уточнения.")
        break

    print("\n🤔 Какие из следующих симптомов вы наблюдаете?")
    for idx, s in enumerate(top_suggestions, 1):
        print(f"{idx}. {s}")
    print(f"{len(top_suggestions)+1}. Ни один из них")

    choice = input("👉 Ваш выбор (номер): ").strip()
    if choice.isdigit():
        choice = int(choice)
        if 1 <= choice <= len(top_suggestions):
            selected_symptoms.append(top_suggestions[choice - 1])
        else:
            print("🙅 Ни один симптом не подошел.")
            rejection_count += 1
    else:
        print("⚠️ Введите номер!")

print("\n📄 Выбранные симптомы:")
for symptom in selected_symptoms:
    print(f"- {symptom}")

predict_disease(selected_symptoms)
