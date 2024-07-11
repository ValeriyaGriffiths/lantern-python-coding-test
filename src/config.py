from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "FastAPI App"
    api_key: str
    admin_email: str
    items_per_user: int = 50


settings = Settings() 
