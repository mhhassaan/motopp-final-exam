import os

class Config:
    # Use os.environ.get for SECRETS. Default is provided only for dev, not prod.
    SECRET_KEY = os.environ.get('SECRET_KEY') 
    
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

# import os
# class Config:
#     if os.environ.get('ENV') == 'prod':
#         SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@mysql:3306/motopp'
#         SECRET_KEY = '123456789'
#         SQLALCHEMY_ECHO = True

#     else:
#         SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost:3306/motopp'
#         SECRET_KEY = '123456789'
#         SQLALCHEMY_ECHO = False
