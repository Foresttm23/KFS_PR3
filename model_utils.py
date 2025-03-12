import xgboost as xgb
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.preprocessing import StandardScaler

def save_model(model, model_file):
    model.save_model(model_file)
    print(f"Модель збережено у файл: {model_file}")

def load_model(model_file):
    model = xgb.Booster()
    model.load_model(model_file)

    print(f"Модель завантажено з файлу: {model_file}")

    return model

def split_data_train_test(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=25)

    print("Дані було розділено.")

    return X_train, X_test, y_train, y_test


def preprocess_data(weather_data_df, prediction = False):
    weather_data_df['year'] = weather_data_df['timestamp'].dt.year
    weather_data_df['year_sin'] = np.sin(2 * np.pi * weather_data_df['year'] / 20)  # для циклу в 20 років
    weather_data_df['year_cos'] = np.cos(2 * np.pi * weather_data_df['year'] / 20)

    weather_data_df['day_of_year'] = weather_data_df['timestamp'].dt.dayofyear
    weather_data_df['day_of_year_sin'] = np.sin(2 * np.pi * weather_data_df['day_of_year'] / 365)
    weather_data_df['day_of_year_cos'] = np.cos(2 * np.pi * weather_data_df['day_of_year'] / 365)


    weather_data_df['month'] = weather_data_df['timestamp'].dt.month
    weather_data_df['month_sin'] = np.sin(2 * np.pi * weather_data_df['month'] / 12)
    weather_data_df['month_cos'] = np.cos(2 * np.pi * weather_data_df['month'] / 12)

    weather_data_df['season'] = weather_data_df['month'].apply(lambda x: (x % 12 + 3) // 3)  # 0 - зима, 1 - весна, 2 - літо, 3 - осінь
    weather_data_df['season_sin'] = np.sin(2 * np.pi * weather_data_df['season'] / 4)
    weather_data_df['season_cos'] = np.cos(2 * np.pi * weather_data_df['season'] / 4)


    weather_data_df['day'] = weather_data_df['timestamp'].dt.day
    weather_data_df['day_sin'] = np.sin(2 * np.pi * weather_data_df['day'] / 7)
    weather_data_df['day_cos'] = np.cos(2 * np.pi * weather_data_df['day'] / 7)
    
    weather_data_df['days_in_month'] = weather_data_df['timestamp'].dt.days_in_month
    weather_data_df['days_to_end_of_month'] = (weather_data_df['days_in_month'] - weather_data_df['day'])


    weather_data_df['hour'] = weather_data_df['timestamp'].dt.hour
    weather_data_df['hour_sin'] = np.sin(2 * np.pi * weather_data_df['hour'] / 24)
    weather_data_df['hour_cos'] = np.cos(2 * np.pi * weather_data_df['hour'] / 24)


    X = weather_data_df.drop(columns=['timestamp', 'temperature_real', 'temperature_predicted'])

    if prediction == False:
        y = weather_data_df['temperature_real']
    else:
        weather_data_df['temperature_real'] = weather_data_df['temperature_predicted']
        y = weather_data_df['temperature_real']

    X_scaled = StandardScaler().fit_transform(X)

    print("Дані було попередньо оброблено.")

    return X_scaled, y

def format_DMatrix(X, y):
    data = xgb.DMatrix(X, y)

    print("Дані було форматовано у формат DMatrix.")

    return data