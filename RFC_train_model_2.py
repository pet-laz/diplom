from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)
import seaborn as sns
import matplotlib.pyplot as plt

def split_dataset(input_file, test_size=0.2):
    # Загрузка расширенного датасета
    df = pd.read_csv(input_file, sep=';', encoding='utf-8')
    
    # Преобразуем симптомы в бинарные признаки
    all_symptoms = []
    for _, row in df.iterrows():
        symptoms = [str(s).strip() for s in row[3:] if pd.notna(s) and str(s).strip() != '']
        for s in symptoms:
            if s not in all_symptoms:
                all_symptoms.append(s)
    
    # Сортируем для единообразия
    all_symptoms = sorted(all_symptoms)
    # Создаем бинарную матрицу симптомов
    X = []
    y = []
    for _, row in df.iterrows():
        symptoms =  [s for s in row.iloc[3:] if pd.notna(s)]
        x_row = [1 if symptom in symptoms else 0 for symptom in all_symptoms]
        X.append(x_row)
        y.append(row['Name'])
    
    # Стратифицированное разделение с сохранением распределения классов
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=test_size,
        stratify=y,
        random_state=42
    )
    
    return X_train, X_test, y_train, y_test, all_symptoms

def evaluate_model(model, X_test, y_test):
    # Предсказания модели
    y_pred = model.predict(X_test)
    
    # Вычисление метрик
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted')
    recall = recall_score(y_test, y_pred, average='weighted')
    f1 = f1_score(y_test, y_pred, average='weighted')
    
    print("\n📊 Основные метрики классификации:")
    print(f"Accuracy (точность): {accuracy:.4f}")
    print(f"Precision (точность): {precision:.4f}")
    print(f"Recall (полнота): {recall:.4f}")
    print(f"F1-score: {f1:.4f}")
    
    # Подробный отчет по классам
    print("\n📋 Детальный отчет по классам:")
    print(classification_report(y_test, y_pred))
    
    # Визуализация матрицы ошибок
    plt.figure(figsize=(10, 8))
    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title('Матрица ошибок')
    plt.xlabel('Предсказанные классы')
    plt.ylabel('Истинные классы')
    plt.show()

# Загрузка и подготовка данных
X_train, X_test, y_train, y_test, all_symptoms = split_dataset("expanded_dataset.csv", 0.3)

# Обучение модели
clf = RandomForestClassifier(
    n_estimators=200,
    max_depth=30,
    class_weight='balanced',
    random_state=42
)
clf.fit(X_train, y_train)

# Оценка модели
evaluate_model(clf, X_test, y_test)

# Сохранение модели и признаков
joblib.dump(clf, 'trained_model.pkl')
joblib.dump(all_symptoms, 'all_symptoms.pkl')

print("\n✅ Модель RandomForest успешно обучена и сохранена в 'trained_model.pkl' и 'all_symptoms.pkl'")
