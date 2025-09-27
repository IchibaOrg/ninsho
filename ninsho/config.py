from pydantic_settings import BaseSettings, SettingsConfigDict

import os
import boto3

env = os.getenv("ENV", "local")  # default local

def load_ssm_parameters(prefix="/ninsho/"):
    """Fetch all parameters under a given prefix and inject into os.environ."""
    ssm = boto3.client("ssm", region_name="eu-central-1")
    paginator = ssm.get_paginator("get_parameters_by_path")

    for page in paginator.paginate(Path=prefix, WithDecryption=True):
        for param in page["Parameters"]:
            key = param["Name"].replace(prefix, "")
            os.environ[key] = param["Value"]



# Only fetch from SSM if ENV=production
if env == "production":
    load_ssm_parameters("/ninsho/")


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


if env == "production":
    config = AppConfig()  # only reads from real env vars
else:
    config = AppConfig(_env_file=".env")  # type: ignore

