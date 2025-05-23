import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# Загружаем данные
data = pd.read_csv("diseases.csv", delimiter=";")

# Собираем все уникальные симптомы и группы
symptom_columns = [col for col in data.columns if col.startswith("Symptom")]
all_symptoms = []

for col in symptom_columns:
    all_symptoms += data[col].dropna().tolist()

# Добавим группы заболеваний как "псевдо-симптомы"
all_groups = data["GroupName"].unique().tolist()
all_symptoms += all_groups

# Удаляем дубликаты и сортируем
all_symptoms = sorted(list(set(all_symptoms)))

# Создаем обучающие данные
X = []
y = []

for _, row in data.iterrows():
    symptoms = row[symptom_columns].dropna().tolist()
    # Добавляем группу как "симптом"
    symptoms.append(row["GroupName"])
    features = [1 if symptom in symptoms else 0 for symptom in all_symptoms]
    X.append(features)
    y.append(row["Name"])  # Название болезни

# Обучаем модель
clf = RandomForestClassifier(
    n_estimators=200,
    max_depth=15,
    class_weight='balanced',
    random_state=42
)
clf.fit(X, y)

# Сохраняем модель и признаки
joblib.dump(clf, 'trained_model.pkl')
joblib.dump(all_symptoms, 'all_symptoms.pkl')

print("✅ Модель RandomForest успешно обучена и сохранена в 'trained_model.pkl' и 'all_symptoms.pkl'")
