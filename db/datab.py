import mysql.connector

def insert_data(topic, payload):
    conn = mysql.connector.connect(
        host='localhost',
        user='lbraun',
        password='LinusNoah1',
        database='flaskiot'
    )
    cursor = conn.cursor()
    sql = "INSERT INTO sensor_data (topic, payload) VALUES (%s, %s)"
    cursor.execute(sql, (topic, payload))
    conn.commit()
    cursor.close()
    conn.close()
