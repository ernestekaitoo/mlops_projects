import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer

def train_and_save():
    # 1. Paths
    base_path = os.path.dirname(__file__)
    data_path = os.path.join(base_path, '..', 'data', 'student_data.csv')
    transformer_dir = os.path.join(base_path, '..', 'models', 'transformers')
    model_path = os.path.join(base_path, '..', 'models', 'model.joblib')

    # 2. Load Data
    df = pd.read_csv(data_path, sep=";")
    
    # 3. Your Transformation Logic
    y = df['Target']
    X = df.drop(columns=['Target'])
    course_column = ['Course']
    numerical_columns = X.select_dtypes(include=['int64', 'float64']).columns

    # Target Encoding
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    # Feature Preprocessing (ColumnTransformer)
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_columns),
            ('course', OneHotEncoder(handle_unknown='ignore'), course_column)
        ],
        remainder='passthrough'
    )

    # 4. Split and Transform
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)
    
    X_train_processed = preprocessor.fit_transform(X_train)
    X_test_processed = preprocessor.transform(X_test)

    # 5. Train Model
    model = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1)
    model.fit(X_train_processed, y_train)

    # 6. Save Everything
    os.makedirs(transformer_dir, exist_ok=True)
    os.makedirs(os.path.dirname(model_path), exist_ok=True)

    # Save the ColumnTransformer (for X) and the LabelEncoder (for y)
    joblib.dump(preprocessor, os.path.join(transformer_dir, 'preprocessor.joblib'))
    joblib.dump(le, os.path.join(transformer_dir, 'label_encoder.joblib'))
    joblib.dump(model, model_path)

    print(f"Transformers saved to {transformer_dir}")
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    train_and_save()