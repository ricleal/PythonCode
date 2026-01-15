from pydantic_settings import BaseSettings, SettingsConfigDict


class SubModel(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="sm_")
    sb1: str = "default_sb1"


class Settings(BaseSettings):
    settings1: str = "default_settings1"
    settings2: str = "default_settings2"


class SettingsWithEnv(Settings):
    model_config = SettingsConfigDict(
        env_file=".env.test",
        env_file_encoding="utf-8",
        extra="allow",
    )
    more_settings: SubModel = SubModel()


s1 = Settings()
print(s1.model_dump())

s2 = SettingsWithEnv()
print(s2.model_dump())
