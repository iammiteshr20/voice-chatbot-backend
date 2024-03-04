from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Server (instead of adding these details to entrypoint, we can add here, and run within python)
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False

    base_url: str
    assemblyai_api_key: str
    eleven_labs_api_key: str

    class Config:
        env_file = ".env"

settings = Settings()
