Бд створюється автоматично, змінити параметри підключення в CONFIG.py

Для прогнозування використовував алгоритм Xgboost для регресії, вона будує дерева рішень та прогнозує результат відповідно до тренувальних даних. 
Попередньо підготувавши дані для навчання, змінивши timestamp на дату та додатково сформувавши синусові та косинусові значення для кращого відображення циклічності.

Програма будує прогнози відповідно до 1 значення в БД (вона на них навчається), також можна побудувати модель на основі прогнозованих значень, а не реальних, для цього треба змінити у файлі ui.py значення при виклику функції:
1. get_weather_data(1, start_training_date, end_training_date, db_select) # 1 - Реальні дані для навчання
Відповідно, щоб змінити, на чому буде тренуватись модель треба просто змінити значення на id бажаного прогнозу:
2. get_weather_data(2, ...

В такому випадку у файлі main.py змінити значення дат на відповідні, наприклад

start_training_date = "1940-09-01 00:00:00" - змінити дату на 2004

end_training_date = "2004-09-01 00:00:00" - змінити дату на 2024

start_testing_date = end_training_date - можна залишити

end_testing_date = "2024-09-01 00:00:00" - змінити дату на 2044

Це необхідно, оскільки прогноз відбувається на 20 років вперед.
