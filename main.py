import os
from dotenv import load_dotenv
from api import api
from bq_loader import bq_loader

"""En esta clase, simplemente llamamos a las funciones de las clases api y bq_loader para descargar los datos de la API y subirlos a BigQuery."""
load_dotenv()

def main():
    api_url = "https://dummyjson.com/users?limit=100"

    project_id = os.getenv("PROJECT_ID")
    dataset_id = os.getenv("DATASET_ID")
    table_id = os.getenv("TABLE_ID")

    # Descargamos los datos de la API

    api_client = api(api_url)
    df = api_client.get_data(limit=100)

    print(f"Registros descargados: {len(df)}")

    # Subimos los datos a BigQuery
    bigqueryloader = bq_loader(
        project_id,
        dataset_id,
        table_id
    )

    bigqueryloader.upload_dataframe(df)

    # Guardamos CSV localmente
    df.to_csv("output_bigquery_data.csv", index=False)

    print("CSV generado correctamente")


if __name__ == "__main__":
    main()