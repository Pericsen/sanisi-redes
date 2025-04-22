import requests
import pandas as pd
import json
from datetime import datetime

import json

with open('credentials_munidigital.json') as f:
    config = json.load(f)

ACCESS_TOKEN = config["ACCESS_TOKEN"]
CONTENT_TYPE = config["CONTENT_TYPE"]


def get_data():
    url = 'https://munidigital.com/MuniDigitalCore/api/incidentes' # TESTING INCIDENTES

    TOKEN = ACCESS_TOKEN

    fecha_desde = '01/03/2025'
    fecha_hasta = datetime.today().strftime('%d/%m/%Y')

    headers = {
        "token": TOKEN,
        "Content-Type": CONTENT_TYPE
    }

    params = {
        "fecha_desde": fecha_desde,
        "fecha_hasta": fecha_hasta
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()

        if data['status'] == 'ok' and data['result']:
            df_incidentes = pd.DataFrame(data['result'])
            print("datos obtenidos correctamente")
            print(df_incidentes.head())
            df_incidentes.to_csv('incidentes.csv', index=False)

        elif data['status'] == 'ok' and not data['result']:
            print("No se encontraron datos")

        else:
            print("Error al obtener los datos")
            print(response.status_code)
            print(response.json())

    else:
        print("Error en la solicitud:", response.status_code)

def main():
    get_data()

if __name__ == '__main__':
    main()