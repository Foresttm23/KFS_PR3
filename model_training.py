import xgboost as xgb
from xgboost import XGBRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
import numpy as np
import matplotlib.pyplot as plt

param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [3, 6, 10],
    'learning_rate': [0.5, 0.1, 0.2],
    'subsample': [0.8, 1.0],
}

boost_rounds = 350
stopping_rounds = 5

def best_params_cross_validate(X_train, y_train):
    grid_search = GridSearchCV(estimator=XGBRegressor(), param_grid=param_grid, cv=5)
    grid_search.fit(X_train, y_train)
    
    params = grid_search.best_params_

    print("Найкращі параметри було знайдено.")

    return params

def train_model(dtrain, params):
    params['eval_metric'] = 'rmse'
    
    model = xgb.train(
        params = params, 
        dtrain = dtrain, 
        num_boost_round = boost_rounds, 
        evals=[(dtrain, 'train')], 
        early_stopping_rounds = stopping_rounds
    )

    print("Модель було натреновано.")

    return model

def predict(model, dtest):
    y_pred = model.predict(dtest)

    print("Модель прогнозує...")

    return y_pred

def evaluate(real, prediction):
    mae = mean_absolute_error(real, prediction)
    r2 = r2_score(real, prediction)
    mse = mean_squared_error(real, prediction)
    rmse = np.sqrt(mse)
    smape = 100 * np.mean(2 * np.abs(real - prediction) / (np.abs(real) + np.abs(prediction)))
    mbe = np.mean(prediction - real)

    print("Результати моделі...")

    plt.figure(figsize=(10, 6))
    plt.plot(real, label='Реальні температури', color='blue', alpha=0.7)
    plt.plot(prediction, label='Прогнозовані температури', color='red', alpha=0.7)
    plt.xlabel('Час', fontsize=12)
    plt.ylabel('Температура', fontsize=12)
    plt.title('Порівняння реальних та прогнозованих температур', fontsize=14)
    plt.legend()
    plt.grid(True)
    plt.show()

    return {
        "MAE": mae,
        "RMSE": rmse,
        "SMAPE": smape,
        "MBE": mbe,
        "R²": r2
    }