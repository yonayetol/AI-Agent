import os
from dotenv import load_dotenv
from psycopg2 import connect
from typing import List

load_dotenv()  

db = connect(
    user='postgres',
    host='localhost',
    database='Country_Flags',
    password=os.getenv("DataBasePassword"),
    port=5432
)

USER_ID = 1  # Hardcode the single user ID

def get_user_preference() -> List[str]:
    """Gets the preferences for the single default user.
        
    Returns:
        A list of the user's preferred topics.
    """
    try:
        with db.cursor() as cur:
            cur.execute("SELECT topic FROM preferences WHERE user_id = %s", (USER_ID,))
            result = cur.fetchall()
            return [row[0] for row in result]
    except Exception as e:
        db.rollback()
        raise e

def add_preference(topic: str) -> str:
    """Adds a topic to the single default user's preferences.

    Args:
        topic: The topic to add to the user's list of preferences.
        
    Returns:
        A confirmation message.
    """
    try:
        with db.cursor() as cur:
            # First, check if the preference already exists to avoid errors.
            cur.execute("SELECT 1 FROM preferences WHERE user_id = %s AND topic = %s", (USER_ID, topic))
            if cur.fetchone():
                return f"Topic '{topic}' is already in your preferences."
            
            # If it doesn't exist, insert it.
            cur.execute("INSERT INTO preferences (user_id, topic) VALUES (%s, %s)", (USER_ID, topic))
            db.commit()
        return f"Added '{topic}' to preferences."
    except Exception as e:
        db.rollback()
        raise e

def delete_preference(topic: str) -> str:
    """Deletes a topic from the single default user's preferences.

    Args:
        topic: The exact topic to delete. For this to work, you may need to first
               call get_user_preference() to see the exact topic names.
        
    Returns:
        A confirmation message.
    """
    try:
        with db.cursor() as cur:
            cur.execute("DELETE FROM preferences WHERE topic = %s AND user_id = %s", (topic, USER_ID))
            deleted_count = cur.rowcount
            db.commit()
            if deleted_count > 0:
                return f"Deleted '{topic}' from preferences."
            else:
                return f"Topic '{topic}' not found in preferences."
    except Exception as e:
        db.rollback()
        raise e 