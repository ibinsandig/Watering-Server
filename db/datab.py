import mysql.connector

def insert_data_flaskiot(topic, payload):
    conn = mysql.connector.connect(
        host='localhost',
        user='sflask',
        password='12345678',
        database='flask_server'
        table='wetness'
    )
    cursor = conn.cursor()
    sql = "INSERT INTO {table} (topic, payload) VALUES (%s, %s)"
    cursor.execute(sql, (topic, payload))
    conn.commit()
    cursor.close()
    conn.close()
