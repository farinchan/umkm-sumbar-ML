import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

# Konfigurasi database
db_config = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_NAME')
}
 # Koneksi ke database
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor(dictionary=True)
        
