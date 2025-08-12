from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings(BaseSettings):

    host : str 
    port : str
    username_db : str
    password :str
    index_name  :str
    path : str
    source_type : str = "s3"

    model_config = SettingsConfigDict(env_file=".env")


settings  = Settings()






