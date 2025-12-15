import os

class Config:
    # Use os.environ.get for SECRETS. Default is provided only for dev, not prod.
    SECRET_KEY = os.environ.get('SECRET_KEY') 
    
    # --- ADDED: Redis Configuration ---
    # Reads 'REDIS_HOST' from 05-app.yaml (which is set to "redis")
    # Defaults to 'localhost' for local testing
    REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
    REDIS_URL = f"redis://{REDIS_HOST}:6379/0"
    # ----------------------------------

    if os.environ.get('ENV') == 'prod':
        # Ensure these match your K8s/Docker Service names
        db_user = os.environ.get('MYSQL_USER', 'root')
        db_pass = os.environ.get('MYSQL_PASSWORD')
        db_host = os.environ.get('MYSQL_HOST', 'mysql')
        db_name = os.environ.get('MYSQL_DATABASE', 'motopp')
        SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{db_user}:{db_pass}@{db_host}:3306/{db_name}'
        SQLALCHEMY_ECHO = False
    else:
        # Local development fallback
        SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost:3306/motopp'
        SQLALCHEMY_ECHO = True