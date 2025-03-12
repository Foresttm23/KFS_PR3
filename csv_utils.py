import pandas as pd

dtype_dict = {
        "id": "int32",
        "forecast_id": "int32",
        "temperature_real": "float32",
        "temperature_predicted": "float32"
    }

def read_from_csv(file):
    return pd.read_csv(file, dtype=dtype_dict, parse_dates=["timestamp"], low_memory=False)

def results_to_csv(file_name, data):
    data_df = pd.DataFrame([data])

    open(file_name, "w").close()

    data_df.to_csv(file_name, index=False)