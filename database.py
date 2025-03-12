import pandas as pd
import mysql.connector
from config import DB_CONFIG


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def delete_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('DROP DATABASE weather_db')
    conn.close()

    print("Базу даних видалено.")

def check_if_db_empty(weather_file):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT EXISTS(SELECT 1 FROM weather_data)')

    if not cursor.fetchone()[0]:
        load_csv_to_db(weather_file)
        db_clean()
        conn.commit()
    
    conn.close()

def create_db():
    conn = mysql.connector.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password']
    )
    cursor = conn.cursor()
    cursor.execute('CREATE DATABASE IF NOT EXISTS weather_db')
    conn.close()

def create_tables():
    create_db()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS weather_forecasts (
        forecast_id INT AUTO_INCREMENT PRIMARY KEY,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS weather_data (
        id INT AUTO_INCREMENT PRIMARY KEY,
        forecast_id INT,
        timestamp DATETIME NOT NULL,
        temperature_real FLOAT DEFAULT NULL,
        temperature_predicted FLOAT DEFAULT NULL,
        FOREIGN KEY (forecast_id) REFERENCES weather_forecasts(forecast_id)
    )
    ''')

    cursor.execute("""
        SELECT COUNT(1) 
        FROM information_schema.statistics 
        WHERE table_name = 'weather_data' 
        AND index_name = 'idx_forecast_timestamp'
    """)

    if cursor.fetchone()[0] == 0:
        cursor.execute('CREATE INDEX idx_forecast_timestamp ON weather_data (forecast_id, timestamp)')

    conn.commit()
    conn.close()

def get_weather_data(forecast_id_1=1, start_date=1940, end_date=2004, file_name = "temp.csv", forecast_id_2=0):
    conn = get_connection()
    cursor = conn.cursor()

    if forecast_id_2 == 0:
        query = "SELECT * FROM weather_data WHERE forecast_id = %s AND timestamp >= %s AND timestamp <= %s"
        params = [forecast_id_1, start_date, end_date]

    else:
        query = '''
            SELECT 
                weather_real.timestamp, 
                weather_real.temperature_real, 
                weather_predicted.temperature_predicted
            FROM weather_data weather_real
            LEFT JOIN weather_data weather_predicted
                ON weather_real.timestamp = weather_predicted.timestamp
                AND weather_predicted.forecast_id = %s
            WHERE weather_real.forecast_id = %s
            AND weather_real.timestamp >= %s AND weather_real.timestamp <= %s
        '''

        params = [forecast_id_2, forecast_id_1, start_date, end_date]


    open(file_name, "w").close()

    weather_data_df = pd.read_sql(query, conn, params=params)

    weather_data_df.to_csv(file_name, index=False)

    cursor.close()
    conn.close()

    print("Дані успішно отримано з бази.")

def load_csv_to_db(weather_data, type = "file", start_date = 0):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('INSERT INTO weather_forecasts () VALUES ()')
    forecast_id = cursor.lastrowid

    conn.commit()

    query = """
        INSERT INTO weather_data (
            forecast_id, timestamp, temperature_real, temperature_predicted
        ) VALUES (%s, %s, %s, %s)
    """

    data = []

    if type == "file":
        df = pd.read_csv(weather_data, skiprows=9)  # 9 перших рядків це текст
        df.columns = ['timestamp', 'temperature_real']

        df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y%m%dT%H%M')
        df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')

        for _, row in df.iterrows():
            data.append((
                forecast_id, row['timestamp'], row['temperature_real'], None
            ))


    elif type == "predictions" and start_date != 0:
        df = pd.DataFrame(weather_data, columns=["temperature_predicted"])

        timestamp = pd.date_range(
            start=start_date, 
            periods=len(weather_data), 
            freq='H'
        ).strftime('%Y-%m-%d %H:%M:%S')

        df['timestamp'] = timestamp


        for _, row in df.iterrows():
            data.append((
                forecast_id, row['timestamp'], None, row['temperature_predicted']
            ))

    cursor.executemany(query, data)

    conn.commit()

    cursor.close()
    conn.close()

    print("Дані успішно завантажено в базу.")

    return forecast_id

def db_clean():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('DELETE FROM weather_data WHERE timestamp IS NULL OR (temperature_real IS NULL AND temperature_predicted IS NULL)')
        
    conn.commit()
    cursor.close()
    conn.close()

    print("Очистку завершено.")
