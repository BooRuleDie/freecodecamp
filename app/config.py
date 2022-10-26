from pydantic import BaseSettings

# Performs ENV var Check
class Settings(BaseSettings):
    databaseHostName: str
    databasePort: int
    databasePassword: str
    databaseName: str
    databaseUsername: str
    secretKey: str
    Algorithm: str
    AccessTokenExpireMinute: int

settings = Settings()