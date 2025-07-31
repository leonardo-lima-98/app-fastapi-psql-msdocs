
class Settings():
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    GLANCES_URL: str

    TENANT_ID: str
    CLIENT_ID: str
    CLIENT_SECRET: str
    AUTHORITY: str
    JWKS_URL: str
    SCOPE: list[str]


    class Config:
        env_file = '.env'


settings = Settings()

if __name__ == '__main__':
    print(settings.model_dump_json(indent=2))
    print('Settings loaded successfully.')
