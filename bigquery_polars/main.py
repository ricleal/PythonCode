import gzip
import io
import json
import os

import polars as pl
from google.cloud import bigquery
from google.cloud.bigquery import Client, SchemaField

# Set up environment variables for authentication and project details.
# You can also hardcode these values directly in the script, e.g.,
# PROJECT_ID = "your-gcp-project-id"
# DATASET_ID = "your_dataset_id"
# TABLE_ID = "your_table_id"

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
DATASET_ID = os.environ.get("BIGQUERY_DATASET_ID")
TABLE_ID = "key_value_table"

# Ensure your GOOGLE_APPLICATION_CREDENTIALS environment variable is set.
# This points to your service account key file.
# export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"


class BigQueryParquetUploader:
    """
    A class to handle the creation of a BigQuery table,
    generation of a Polars DataFrame, and uploading the data
    using the Parquet format.
    """

    def __init__(self, project_id: str, dataset_id: str):
        """
        Initializes the BigQuery client.

        Args:
            project_id (str): The Google Cloud project ID.
            dataset_id (str): The BigQuery dataset ID.
        """
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.client = Client(project=self.project_id)
        print(f"BigQuery client initialized for project: {self.project_id}")

    def create_table(self, table_id: str) -> str:
        """
        Creates a BigQuery table with a 'key' and a 'value' field.
        The 'value' field is of type JSON.

        Args:
            table_id (str): The ID of the table to be created.

        Returns:
            str: The full path of the created table.
        """
        full_table_id = f"{self.project_id}.{self.dataset_id}.{table_id}"
        schema = [
            SchemaField("key", "STRING", mode="REQUIRED"),
            SchemaField("value", "JSON", mode="REQUIRED"),
        ]

        try:
            # First, check if the dataset exists
            dataset = bigquery.Dataset(f"{self.project_id}.{self.dataset_id}")
            self.client.get_dataset(dataset)
        except Exception:
            print(f"Dataset '{self.dataset_id}' not found. Creating it...")
            self.client.create_dataset(bigquery.Dataset(dataset))
            print(f"Dataset '{self.dataset_id}' created.")

        table = bigquery.Table(full_table_id, schema=schema)

        try:
            # Check if the table already exists.
            self.client.get_table(table)
            print(f"Table '{full_table_id}' already exists.")
        except Exception:
            print(f"Creating table '{full_table_id}'...")
            table = self.client.create_table(table)
            print(f"Table '{full_table_id}' created successfully.")

        return full_table_id

    def generate_polars_dataframe(self, num_rows: int) -> pl.DataFrame:
        """
        Generates a Polars DataFrame with a specified number of rows.
        The dataframe contains a 'key' column and a 'value' column
        with JSON-formatted strings.

        Args:
            num_rows (int): The number of rows to generate.

        Returns:
            pl.DataFrame: The generated Polars DataFrame.
        """
        print(f"Generating Polars DataFrame with {num_rows} rows...")
        data = {
            "key": [f"row_{i}" for i in range(num_rows)],
            "value": [
                json.dumps(
                    {
                        "id": i,
                        "name": f"Item {i}",
                        "details": {
                            "category": "category_A" if i % 2 == 0 else "category_B",
                            "price": i * 1.5,
                        },
                    }
                )
                for i in range(num_rows)
            ],
        }
        df = pl.DataFrame(data)
        print("DataFrame generated.")
        return df

    def upload_dataframe_ndjson(
        self, df: pl.DataFrame, table_id: str, gzip_compress: bool = True
    ):
        """Upload the DataFrame to BigQuery using newline-delimited JSON so a JSON column maps correctly.

        BigQuery currently cannot ingest a Parquet STRING column into an existing JSON field; Parquet/Avro
        writers used by Polars do not emit a JSON logical type BigQuery recognizes. Therefore we serialize
        rows as NDJSON with the value column decoded into structured JSON objects.

        Args:
            df: Polars DataFrame with columns 'key' (str) and 'value' (JSON string).
            table_id: Fully qualified BigQuery table id.
            gzip_compress: If True, compress payload in-memory with gzip (BigQuery auto-detects).
        """
        print(
            f"Uploading data to table '{table_id}' as NDJSON (gzip={gzip_compress})..."
        )

        # Convert JSON string column to actual nested structures so NDJSON lines contain objects not strings.
        df_prepared = df.with_columns(pl.col("value").str.json_decode())

        # Prepare in-memory buffer.
        raw_buffer = io.BytesIO()
        if gzip_compress:
            with gzip.GzipFile(fileobj=raw_buffer, mode="wb") as gz:
                tmp = io.BytesIO()
                df_prepared.write_ndjson(tmp)
                gz.write(tmp.getvalue())
        else:
            df_prepared.write_ndjson(raw_buffer)

        raw_buffer.seek(0)

        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
            ignore_unknown_values=False,
        )

        try:
            job = self.client.load_table_from_file(
                raw_buffer, destination=table_id, job_config=job_config
            )
            job.result()
            print(f"Data successfully uploaded. Rows inserted: {job.output_rows}")
        except Exception as e:
            print(f"NDJSON upload failed: {e}")


if __name__ == "__main__":
    # Check if necessary environment variables are set.
    if not PROJECT_ID or not DATASET_ID:
        print(
            "Please set the GCP_PROJECT_ID and BIGQUERY_DATASET_ID environment variables."
        )
    else:
        uploader = BigQueryParquetUploader(PROJECT_ID, DATASET_ID)

        # Create a unique table for this run
        full_table_id = uploader.create_table(TABLE_ID)

        # Generate a Polars DataFrame with 1000 rows.
        polars_df = uploader.generate_polars_dataframe(1000)

        # Upload the DataFrame to BigQuery using NDJSON -> JSON column.
        uploader.upload_dataframe_ndjson(polars_df, full_table_id)
