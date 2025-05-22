import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import numpy as np

# Загружаем данные
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
    y.append(row.iloc[0])  # Название болезни

# Обучаем модель Random Forest
clf = RandomForestClassifier(
    n_estimators=200,      # Кол-во деревьев
    max_depth=15,          # Максимальная глубина
    class_weight='balanced',  # Учитываем редкие болезни
    random_state=42
)
clf.fit(X, y)

# Сохраняем модель и список симптомов
joblib.dump(clf, 'trained_model.pkl')
joblib.dump(all_symptoms, 'all_symptoms.pkl')

print("✅ Модель RandomForest успешно обучена и сохранена в 'trained_model.pkl' и 'all_symptoms.pkl'")
