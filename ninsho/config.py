from pydantic_settings import BaseSettings, SettingsConfigDict

import os


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(extra="allow")

    app_name: str = "ninsho"
    app_port: int = 7200
    app_num_workers: int = 1
    app_session_secret_key: str = "change-me"
    debug: bool = False

    # auth
    secret_key: str = "super-secret"

    # db
    database_url: str = "postgresql+psycopg2://user:password@localhost:5432/mydb"



current_dir = os.path.dirname(os.path.abspath(__file__))

parent_dir = os.path.dirname(current_dir)

env_file_path = os.path.join(parent_dir, ".env")

config: AppConfig = AppConfig(_env_file=env_file_path)  # type: ignore

