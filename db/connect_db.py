import mysql.connector

# Это отладочный файл для проверки установки соединения с БД
def get_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="hisamo3485043",
        database="platform"
    )
    return connection

if __name__ == "__main__":
    connection = get_connection()
    print(connection)
    connection.close()