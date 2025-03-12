from ui import start_program

weather_file = "weather_real.csv"
model_file = "model.json"
db_select = "db_select.csv"
prediction_file = "predictions.csv"
results_file = "results.csv"


start_training_date = "1940-09-01 00:00:00"
end_training_date = "2004-09-01 00:00:00"

start_testing_date = end_training_date
end_testing_date = "2024-09-01 00:00:00"

if __name__ == "__main__":
    print("Запуск...")
    start_program(weather_file, model_file, db_select, prediction_file, results_file, start_training_date, end_training_date, start_testing_date, end_testing_date)
