from pydantic_settings import BaseSettings
import os


environment = os.getenv("ENVIRONMENT", "DEV")


if environment == "DEV":
    class Settings(BaseSettings):
        environment: str = environment
        debug: bool = True
        api_key: str = 'TEST_KEY'
        db_location: str = 'data/database.csv'
elif environment == "PROD":
    class Settings(BaseSettings):
        environment: str = environment
        debug: bool = False
        api_key: str = os.getenv("API_KEY")
        db_location: str = os.getenv("DATABASE_URL") # assume we have a real db set up for prod


settings = Settings()
