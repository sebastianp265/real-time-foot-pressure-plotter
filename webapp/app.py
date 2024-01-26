import json
import datetime
import logging
from typing import List

import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output
from config import *
import redis
import requests
import foot_custom_component as foot_custom_component

PATIENTS_DATA = []  # List of patient records
OPTIONS = []  # List of options for the dropdown menu
CACHE = None  # Redis cache object

# Try to connect to Redis
# If Redis is not running, the program will exit
try:
    CACHE = redis.Redis(host=HOST, port=PORT)
except redis.ConnectionError as connection_error:
    print(f"Redis connection error occurred:\n{connection_error}")
    exit(-1)

# Get the basic_info about patients from ISOD API
try:
    for i in IDS:
        api_response = requests.get(url=f"{BASE_URL}{i}")
        json_data = api_response.json()
        basic_info_data = {
            "id": i - 1,  # ID of the patient
            "birthdate": json_data["birthdate"],  # Birthdate of the patient
            "name": json_data["firstname"] + " " + json_data["lastname"],  # Name of the patient
            "disabled": json_data["disabled"],  # Disabled status of the patient
        }

        PATIENTS_DATA.append(basic_info_data)
except requests.exceptions.RequestException as request_exception:
    print(f"Request exception occurred:\n{request_exception}")
    exit(1)

# Create a list of options for the dropdown menu
for i in PATIENTS_DATA:
    OPTIONS.append({"label": i["name"], "value": i["id"]})

# Create the dash app with Bootstrap CSS
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


def generate_patient_basic_info_bar(patient: dict) -> dbc.Col:
    """
    Generates a bar with basic info about the patient
    """
    return dbc.Col(
        [
            html.Div(
                children=[
                    html.H3("Patient's basic information"),
                    html.Div(
                        html.Dl(
                            [
                                html.Dt("Name"),
                                html.Dd(patient["name"]),
                                html.Dt("Birthdate"),
                                html.Dd(patient["birthdate"]),
                                html.Dt("Disabled"),
                                html.Dd("Yes" if patient["disabled"] else "No"),
                            ]
                        )
                    )
                ], className="d-flex flex-column justify-content-center align-items-center"
            )
        ], className="d-flex align-items-center justify-content-center"
    )


# Create a simple navbar with a dropdown menu - patient selection
navbar = dbc.NavbarSimple(
    children=[
        html.Div(
            [
                dcc.Dropdown(
                    id="patient-dropdown",
                    options=OPTIONS,
                    placeholder="Select a patient",
                    value=0,
                    style={"min-width": "300px"}
                )
            ], className="d-flex align-items-center justify-content-between"
        )
    ],
    brand="Patient Monitor",
    brand_href="#",
    sticky="top",
)

# Create a main container for the app
main_content = dbc.Container(
    [
        dcc.Store(id="patient_id", storage_type="session", data={"id": 0}),
        html.Div(
            [
                html.Div(
                    id="patient_basic_info_container", className="d-flex align-items-stretch justify-content-center"
                ),
                foot_custom_component.FootCustomComponent(id="foot_custom_component", data="data"),
            ], className="d-flex flex-column align-items-center justify-content-center"
        ),
        dcc.Interval(id="walking_interval", interval=1 * 1000, n_intervals=0),
        dcc.Interval(id="interval", interval=3 * 1000, n_intervals=0),
        dcc.Interval(id="anomaly_interval", interval=10 * 1000, n_intervals=0),
        dbc.Col(
            [
                html.H3("Live data", className="text-center"),
                dcc.Graph(id="left_foot_sensors"),
                dcc.Graph(id="right_foot_sensors"),
                html.Hr(),
                html.H3("Anomalies", className="text-center"),
                dcc.Graph(id="left_foot_anomalies"),
                dcc.Graph(id="right_foot_anomalies"),
            ], className="border shadow pt-5"
        )
    ]
)

# Create the layout of the app
app.layout = html.Div([navbar, main_content])


@app.callback(
    Output("patient_basic_info_container", "children"),
    Output("patient_id", "data"),
    Input("patient-dropdown", "value"),
)
def change_patient(value):
    """
    Changes the patient in the app
    """
    print(value)
    patient: dict = PATIENTS_DATA[value]
    return generate_patient_basic_info_bar(patient), {"id": value}


@app.callback(
    Output("foot_custom_component", "data"),
    Input("patient_id", "data"),
    Input("walking_interval", "n_intervals"),
)
def update_walking_graph(patient_data, n):
    """
    Updates the feet graph
    """
    key: str = f"{patient_data['id'] + 1}_data"
    data = CACHE.lrange(key, -1, -1)

    return str(data[0], "utf-8")

@app.callback(
    Output("left_foot_sensors", "figure"),
    Output("right_foot_sensors", "figure"),
    Input("patient_id", "data"),
    Input("interval", "n_intervals"),
)
def update_sensors_graph(patient_data, n):
    """
    Updates the sensors graph
    """
    key: str = f"{patient_data['id'] + 1}_data"
    data: list = CACHE.lrange(key, 0, -1)

    sensors = []
    for i in SENSORS_ID:
        sensors.append(list(map(lambda x: json.loads(x)[i].get("value"), data)))
    left_foot_data = {
        "data": generate_sensors_data_list(sensors[:3], [f"Sensor {i}" for i in range(3)]),
        "layout": {"title": "Left foot sensors"},
        "frames": [],
    }
    right_foot_data = {
        "data": generate_sensors_data_list(sensors[3:], [f"Sensor {i}" for i in range(3, 6)]),
        "layout": {"title": "Right foot sensors"},
        "frames": [],
    }
    return left_foot_data, right_foot_data


@app.callback(
    Output("left_foot_anomalies", "figure"),
    Output("right_foot_anomalies", "figure"),
    Input("patient_id", "data"),
    Input("anomaly_interval", "n_intervals"),
)
def update_anomalies_graph(patient_data, n):
    """
    Updates the anomalies graph
    """
    key: str = f"{patient_data['id'] + 1}_anomaly"
    key_date_time: str = f"{patient_data['id'] + 1}_anomaly_timestamp"
    anomaly_data: list = CACHE.lrange(key, 0, -1)
    timestamps: list = CACHE.lrange(key_date_time, 0, -1)
    date_time = list(map(lambda x: datetime.datetime.fromtimestamp(int(x)), timestamps))

    sensors = []
    for i in SENSORS_ID:
        sensors.append(list(map(lambda x: json.loads(x)[i].get("value"), anomaly_data)))

    left_foot_anomalies = {
        "data": generate_sensors_data_list(sensors[:3], [f"Sensor {i}" for i in range(3)], date_time),
        "layout": {"title": "Left foot anomalies"},
        "frames": [],
    }
    right_foot_anomalies = {
        "data": generate_sensors_data_list(sensors[3:], [f"Sensor {i}" for i in range(3, 6)], date_time),
        "layout": {"title": "Right foot anomalies"},
        "frames": [],
    }
    return left_foot_anomalies, right_foot_anomalies


def generate_sensors_data_list(sensors: List[list], sensor_names: List[str], date_time: list = None) -> list:
    """
    Generates a list of traces for the sensors graph
    :param sensors: List of sensors data
    :param sensor_names: List of sensor names
    :param date_time: List of timestamps
    :return: List of traces
    """

    sensors_data = []
    for idx, value in enumerate(sensors):
        if date_time is not None:

            trace = {
                "x": date_time,
                "y": value,
                "name": sensor_names[idx],
                "type": "scatter",
                "mode": "lines+markers",
                "marker": {"size": 1},
            }
        else:
            trace = {
                "y": value,
                "name": sensor_names[idx],
                "type": "scatter",
                "mode": "lines+markers",
                "marker": {"size": 1},
            }
        sensors_data.append(trace)
    return sensors_data


logging.basicConfig(level=logging.DEBUG)
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
