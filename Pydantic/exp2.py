from pprint import pprint

from pydantic_settings import BaseSettings, SettingsConfigDict


class BigQuerySettings(BaseSettings):
    project_id: str | None = None
    dataset_id: str | None = None

    model_config = SettingsConfigDict(
        env_prefix="bigquery_", extra="ignore", env_file=".env"
    )


class Settings(BaseSettings):
    bigquery: BigQuerySettings = BigQuerySettings()

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        str_strip_whitespace=True,
        extra="ignore",
    )

    # @model_validator(mode="after")
    # def validate_backend_config(self):
    #     if (
    #         self.bigquery.project_id is None
    #         or len(self.bigquery.project_id) == 0
    #         or self.bigquery.dataset_id is None
    #         or len(self.bigquery.dataset_id) == 0
    #     ):
    #         raise ValueError(
    #             "BigQuery project_id and dataset_id are required when using BigQuery backend. "
    #             "Please set BIGQUERY_PROJECT_ID and BIGQUERY_DATASET_ID environment variables."
    #         )

    #     return self


settings = Settings()
pprint(settings.model_dump(mode="json"))
