import mysql.connector # type: ignore

def insert_data_trigger(value):
    conn = mysql.connector.connect(
        host='localhost',
        user='sflask',
        password='12345678',
        database='flask_server'
    )
    cursor = conn.cursor()
    sql = "INSERT INTO trigger_values (value) VALUES (%s)"
    cursor.execute(sql, (value,))
    conn.commit()
    cursor.close()
    conn.close()