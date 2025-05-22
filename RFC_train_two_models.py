import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder

# === Загрузка данных ===
data = pd.read_csv("diseases.csv", delimiter=";")

# === Подготовка списка симптомов ===
all_symptoms = []
for i in range(3, data.shape[1]):
    all_symptoms += data.iloc[:, i].dropna().tolist()
all_symptoms = sorted(list(set(all_symptoms)))

# === Подготовка входных данных для обеих моделей ===
symptom_vectors = []
group_labels = []
disease_labels = []

for _, row in data.iterrows():
    symptoms = row[3:].dropna().tolist()
    symptom_vector = [1 if symptom in symptoms else 0 for symptom in all_symptoms]
    symptom_vectors.append(symptom_vector)
    group_labels.append(row["GroupName"])
    disease_labels.append(row["Name"])

X_symptoms = np.array(symptom_vectors)

# === Модель №1: Предсказание группы заболевания ===
group_clf = RandomForestClassifier(n_estimators=100, max_depth=10, class_weight="balanced", random_state=42)
group_clf.fit(X_symptoms, group_labels)

# === One-hot кодирование групп для Модели №2 ===
encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
group_encoded = encoder.fit_transform(np.array(group_labels).reshape(-1, 1))

# === Модель №2: Предсказание диагноза по симптомам + группе ===
X_combined = np.hstack([X_symptoms, group_encoded])
diagnosis_clf = RandomForestClassifier(n_estimators=200, max_depth=15, class_weight="balanced", random_state=42)
diagnosis_clf.fit(X_combined, disease_labels)

# === Сохраняем всё необходимое ===
joblib.dump(all_symptoms, "all_symptoms.pkl")
joblib.dump(group_clf, "group_model.pkl")
joblib.dump(diagnosis_clf, "diagnosis_model.pkl")
joblib.dump(encoder, "group_encoder.pkl")

print("✅ Обе модели успешно обучены и сохранены.")
