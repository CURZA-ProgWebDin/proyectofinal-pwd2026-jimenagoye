import os
from datetime import timedelta


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://root:root@localhost:3306/academia_final",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY",
        "cambia-esta-clave-por-una-segura-en-produccion",
    )
    # Cuánto dura el token de acceso (30 min) antes de tener que renovarlo
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        minutes=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES_MIN", "30"))
    )
    # El token de refresco dura 7 días y solo sirve para conseguir un access nuevo
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(
        days=int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES_DAYS", "7"))
    )