'''

import os

DATABASE_CONFIG = {
    'user': os.getenv('DATABASE_USER', 'root'),
    'password': os.getenv('DATABASE_PASSWORD', 'admin'),
    'host': os.getenv('DATABASE_HOST', 'mysql-db'),  # Nome do serviço do banco no docker-compose.yml
    'database': os.getenv('DATABASE_NAME', 'projetog2'),
    'port': os.getenv('DATABASE_PORT', 3306),
}
'''