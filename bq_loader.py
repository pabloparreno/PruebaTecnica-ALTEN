from google.cloud import bigquery
from google.api_core.exceptions import NotFound
import pandas as pd


""" Esta clase sube el DataFrame generado a BigQuery.
No es necesario crear el dataset ni la tabla previamente, se genera automáticamente """


class bq_loader:

    def __init__(self, project_id: str, dataset_id: str, table_id: str):

        self.project_id = project_id
        self.dataset_id = dataset_id
        self.table_id = table_id

        self.client = bigquery.Client(project=project_id)

    def create_dataset_if_not_exists(self):

        dataset_ref = f"{self.project_id}.{self.dataset_id}"

        try:
            self.client.get_dataset(dataset_ref)
            print(f"El dataset ya existe: {dataset_ref}")

        except NotFound:

            dataset = bigquery.Dataset(dataset_ref)
            dataset.location = "EU"

            self.client.create_dataset(dataset)

            print(f"Dataset creado correctamente: {dataset_ref}")

    def upload_dataframe(self, df: pd.DataFrame):

        if df.empty:

            print("El DataFrame está vacío. No se subirán datos.")

            return

        self.create_dataset_if_not_exists()

        table_ref = (
            f"{self.project_id}.{self.dataset_id}.{self.table_id}"
        )

        job_config = bigquery.LoadJobConfig(

            autodetect=True,

            write_disposition="WRITE_TRUNCATE"
        )

        job = self.client.load_table_from_dataframe(
            df,
            table_ref,
            job_config=job_config
        )

        job.result()

        print(
            f"Datos subidos correctamente a BigQuery: {table_ref}"
        )