import requests
import pandas as pd


"""Esta clase realiza la descarga de datos desde la API, devuelve un JSON con usuarios para insertar en Big Query.
Además limitamos la descarga a 100 registros. """

class api:

    def __init__(self, base_url: str):

        self.base_url = base_url

    def get_data(self, limit: int = 100) -> pd.DataFrame:

        try:

            response = requests.get(
                self.base_url,
                timeout=10
            )

            response.raise_for_status()

        except requests.exceptions.RequestException as e:

            print(f"Error conectando con la API: {e}")

            return pd.DataFrame()

        data = response.json()["users"]

        data = data[:limit]

        df = pd.DataFrame(data)

        return df