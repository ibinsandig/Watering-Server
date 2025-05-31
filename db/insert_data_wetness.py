import mysql.connector # type: ignore

"""Speichern der Daten in der Datenbank"""
def insert_data_wetness(topic, message):
    conn = mysql.connector.connect(
        host='localhost',
        user='sflask',
        password='12345678',
        database='flask_server'
    )
    cursor = conn.cursor()
    sql = "INSERT INTO wetness (topic, message) VALUES (%s, %s)"
    cursor.execute(sql, (topic, message))
    conn.commit()
    cursor.close()
    conn.close()