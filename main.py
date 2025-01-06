import streamlit as st
import sqlite3
import pandas as pd

# Establish a connection to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('/home/jeff/streamlit.sqlite')  # Replace 'your_database.db' with your desired filename

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

#Example: Create a table (if it doesn't already exist)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS items1 (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        quantity INTEGER
    )
''')

# Commit the changes (if you created a table or inserted data)
conn.commit()


# Streamlit interaction example:

# Add items to the database
st.subheader("Add Item")
item_name = st.text_input("Item Name")
item_quantity = st.number_input("Quantity", min_value=0, step=1)

if st.button("Add"):
    cursor.execute("INSERT INTO items1 (name, quantity) VALUES (?, ?)", (item_name, item_quantity))
    conn.commit()
    st.success(f"Added {item_name} to the database.")


# Display the database contents
st.subheader("Database Contents")
try:
    df = pd.read_sql_query("SELECT * FROM items1", conn)  # Use pandas for easy display
    st.dataframe(df)
except Exception as e:
    st.error(f"Error reading from database: {e}")  # Handle potential errors gracefully



# Close the connection when the app is done (important!)
conn.close() 

