import mysql.connector

# Konfigurasi database
db_config = {
    'user': 'root',
    'password': '',
    'host': '127.0.0.1',
    'database': 'umkm_sumbar'
}
 # Koneksi ke database
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor(dictionary=True)
        
