import pyodbc
import streamlit as st

from datetime import datetime
from core.connection import connect_to_app_database

def log_action(username, user_id, action):
    log_conn = connect_to_app_database()
    if log_conn:
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor = log_conn.cursor()
            cursor.execute(
                "INSERT INTO dbo.log_people (user_id, username, action, timestamp) VALUES (?, ?, ?, ?)",
                (user_id, username, action, timestamp)
            )
            log_conn.commit()
        except pyodbc.Error as e:
            st.error(f"Error logging action: {e}")