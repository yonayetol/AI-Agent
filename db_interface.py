from psycopg2 import connect

db = connect(
    user='postgres',
    host='localhost',
    database='Country_Flags',
    password='Miki62005046@',
    port=5432
)

def get_user_preference(user_id):
    with db.cursor() as cur:
        cur.execute("SELECT topic FROM preferences WHERE user_id = %s", (user_id,))
        result = cur.fetchall()
        return [row[0] for row in result]

def add_preference(user_id, topic):
    with db.cursor() as cur:
        cur.execute("INSERT INTO preferences (user_id, topic) VALUES (%s, %s)", (user_id, topic))
        db.commit()

def delete_preference(topic):
    with db.cursor() as cur:
        cur.execute("DELETE FROM preferences WHERE topic = %s", (topic,))
        db.commit() 