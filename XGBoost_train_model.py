import pandas as pd
import numpy as np
import joblib
from xgboost import XGBClassifier
from sklearn.preprocessing import LabelEncoder

# Загружаем данные
data = pd.read_csv("diseases.csv", delimiter=";")

# Составляем список всех уникальных симптомов
all_symptoms = sorted({symptom.strip() for i in range(3, data.shape[1])
                       for symptom in data.iloc[:, i].dropna().tolist()})

# Создаём обучающие данные
X = []
y = []

for _, row in data.iterrows():
    disease_symptoms = [str(s).strip() for s in row[3:] if pd.notna(s)]
    features = [1 if symptom in disease_symptoms else 0 for symptom in all_symptoms]
    X.append(features)
    y.append(row.iloc[0])  # Название болезни

X = np.array(X)
y = np.array(y)

# Кодируем названия болезней в числа
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Обучаем XGBoost-модель
model = XGBClassifier(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=4,
    use_label_encoder=False,
    eval_metric='mlogloss',
    verbosity=0
)
model.fit(X, y_encoded)

# Сохраняем модель и вспомогательные файлы
joblib.dump(model, 'xgb_model.pkl')
joblib.dump(all_symptoms, 'xgb_symptoms.pkl')
joblib.dump(label_encoder, 'label_encoder.pkl')

print("✅ XGBoost-модель обучена и сохранена в 'xgb_model.pkl'")
print("📁 Симптомы сохранены в 'xgb_symptoms.pkl'")
print("📁 LabelEncoder сохранён в 'label_encoder.pkl'")
