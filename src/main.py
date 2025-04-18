import requests
import pandas as pd
import json
from datetime import datetime

from config import ACCESS_TOKEN, CONTENT_TYPE, USER, PASS


def get_data():
    url = 'https://test-munidigital-core.munidigital.net/MuniDigitalCore/api/incidentes' # TESTING INCIDENTES

    TOKEN = ACCESS_TOKEN

    fecha_desde = '01/01/2025'
    fecha_hasta = datetime.today().strftime('%d/%m/%Y')

    headers = {
        "token": TOKEN,
        "Content-Type": CONTENT_TYPE
    }

    params = {
        "fecha_desde": fecha_desde,
        "fecha_hasta": fecha_hasta
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()

        if data['status'] == 'ok' and data['result']:
            df_incidentes = pd.DataFrame(data['result'])
            print("datos obtenidos correctamente")
            print(df_incidentes.head())

        elif data['status'] == 'ok' and not data['result']:
            print("No se encontraron datos")

        else:
            print("Error al obtener los datos")

    else:
        print("Error en la solicitud:", response.status_code)

def main():
    get_data()

if __name__ == '__main__':
    main()