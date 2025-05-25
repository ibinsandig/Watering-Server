import mysql.connector

def insert_data_flaskiot(topic, payload):
    conn = mysql.connector.connect(
        host='localhost',
        user='sflask',
        password='12345678',
        database='flask_server'
    )
    cursor = conn.cursor()
    sql = "INSERT INTO wetness (topic, payload) VALUES (%s, %s)"
    cursor.execute(sql, (topic, payload))
    conn.commit()
    cursor.close()
    conn.close()