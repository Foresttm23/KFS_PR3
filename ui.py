from database import create_tables, load_csv_to_db, get_weather_data, db_clean, delete_db, check_if_db_empty
from model_training import best_params_cross_validate, train_model, predict, evaluate
from model_utils import save_model, load_model, split_data_train_test, preprocess_data, format_DMatrix
from csv_utils import read_from_csv, results_to_csv
import os


def clear_terminal():
    os.system('cls')

def check_if_model_exists(model_file):
    if os.path.exists(model_file):
        print("Завантаження моделі...")
        model = load_model(model_file)
        return model
    
    return False

def create_model(model_file, db_select, start_training_date, end_training_date):
    get_weather_data(1, start_training_date, end_training_date, db_select) # 1 - Реальні дані для навчання

    data_train = read_from_csv(db_select)

    X_train, y_train = preprocess_data(data_train)

    params = best_params_cross_validate(X_train, y_train)

    dtrain= format_DMatrix(X_train, y_train)

    model = train_model(dtrain, params)
    save_model(model, model_file)

def start_program(weather_file, model_file, db_select, prediction_file, results_file, start_training_date, end_training_date, start_testing_date, end_testing_date):
    try:
        print("Створюємо таблиці в БД...")
        create_tables()

        print("Записуємо погоду в БД, якщо вона пуста...")
        check_if_db_empty(weather_file)

        clear_terminal()

        model = check_if_model_exists(model_file)

        if model == False:
            print("Модель не знайдено. Модель буде створено автоматично...")
            create_model(model_file, db_select, start_training_date, end_training_date)
            print("Модель створено.")

        while True:
            try:
                print("\n\n\n")
                print("Виберіть дію:")
                print("Оновити дані в базі даних - 1")
                print("Прогнозувати погоду - 2")
                print("Вивести результати минулих прогнозів - 3")
                print("Вийти - 0")

                choice_menu = int(input("\n\nВведіть число: "))

                if choice_menu == 1:
                    print("Оновлення бази даних...")
                    delete_db()

                    print("Створюємо таблиці в БД...")
                    create_tables()

                    load_csv_to_db(weather_file)
                    db_clean()

                    clear_terminal()

                    print("\nБД успішно оновлено.")

                    continue

                if choice_menu == 2:
                    get_weather_data(1, start_testing_date, end_testing_date, db_select) # 1 - Реальні дані для навчання

                    data_test = read_from_csv(db_select)

                    X_test, y_test = preprocess_data(data_test)

                    dtest = format_DMatrix(X_test, y_test)

                    y_pred = predict(model, dtest)

                    last_loaded_forecast_id = load_csv_to_db(y_pred, "predictions", start_testing_date) # повертає id останнього прогнозу

                    get_weather_data(1, start_testing_date, end_testing_date, prediction_file, last_loaded_forecast_id) # Дані для порівняння в файл prediction_file

                    clear_terminal()

                    print(f"\n\n\nПрогнозування погоди записано під id: {last_loaded_forecast_id}")

                    print(f"\nРезультати порівняння збережено в {prediction_file}.")

                    continue


                if choice_menu == 3:
                    choice_forecast_id = int(input("\n\n\nВведіть id прогнозу для порівняння: "))

                    get_weather_data(1, start_testing_date, end_testing_date, prediction_file, choice_forecast_id) # Дані для порівняння в файл prediction_file

                    print(f"Результати порівняння збережено в {prediction_file}.")

                    data_temp = read_from_csv(prediction_file)

                    data_result = data_temp.drop(columns=['timestamp'])

                    result = evaluate(data_result['temperature_real'], data_result['temperature_predicted'])

                    results_to_csv(results_file, result)

                    print(f"Результати evaluate записано в {results_file}.")

                    continue

                else:
                    return
                
            except Exception as e:
                print(f"\n\n\nПомилка: {e}")

                continue

    except Exception as e:
        print(f"\n\n\nПомилка при запуску: {e}")